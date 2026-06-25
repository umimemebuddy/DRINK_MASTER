#!/usr/bin/env python3
"""
🥃 DRINK MASTER v3.0 — 饮品大师升级版
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
L1: 风味关联图谱 ← 升级: 共现矩阵 → 向量相似度
L2: 风味炼金术 ← 保留: 7种结构 + 情绪注入
L3: 语义搜索 ← 新增: 自然语言配方检索
L4: 风味词库 ← 新增: 自动从数据提取高频原料
"""

import json, subprocess, math, sys, re, os
from collections import Counter, defaultdict
from datetime import datetime

DDB = "http://127.0.0.1:8766"
DATA_DIR = os.path.expanduser("~/.drink_master")
os.makedirs(DATA_DIR, exist_ok=True)
VOCAB_FILE = os.path.join(DATA_DIR, "flavor_vocab.json")
COOCCUR_FILE = os.path.join(DATA_DIR, "cooccur_matrix.json")

CACHE_TTL = 86400  # 1 day

def dq(sql):
    r = subprocess.run(["curl","-s","-X","POST",DDB,"-H","Content-Type: application/json",
        "-d",json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"duck_query","arguments":{"sql":sql}}})],
        capture_output=True,text=True,timeout=15)
    return json.loads(r.stdout)

# ==================================================================
# L4: 风味词库 — 自动提取 & 智能扩充
# ==================================================================

# 基础风味词（手动精调，不可替代）
BASE_VOCAB = {
    "spirit": ["gin","vodka","whiskey","whisky","bourbon","rye","scotch",
               "rum","tequila","mezcal","brandy","cognac","pisco","cachaça",
               "sake","soju"],
    "liqueur": ["campari","aperol","vermouth","amaro","fernet","chartreuse",
                "absinthe","cointreau","triple sec","grand marnier","maraschino",
                "schnapps","baileys","kahlua","amaretto","frangelico","sambuca",
                "ouzo","pastis","st. germain","curacao","midori"],
    "citrus": ["lemon","lime","orange","grapefruit","yuzu","kumquat","bergamot","tangerine"],
    "fruit": ["apple","pear","peach","apricot","cherry","raspberry","strawberry",
              "blueberry","blackberry","cranberry","pineapple","mango","passion fruit",
              "coconut","banana","lychee","watermelon","melon","fig","plum","grape",
              "kiwi","guava","papaya","pomegranate","rhubarb"],
    "herb": ["mint","basil","rosemary","thyme","sage","lavender","chamomile",
             "elderflower","hibiscus","jasmine","rose","lemongrass","cilantro",
             "dill","fennel","anise","tarragon","oregano","bay leaf"],
    "spice": ["cinnamon","clove","nutmeg","cardamom","star anise","pepper",
              "chili","jalapeño","wasabi","ginger","turmeric","vanilla",
              "cacao","chocolate","coffee","matcha","chai","allspice"],
    "sweetener": ["sugar","honey","maple syrup","agave","simple syrup",
                  "orgeat","falernum","grenadine","coconut cream","demerara",
                  "brown sugar","molasses","caramel"],
    "bitter": ["angostura bitters","orange bitters","peychauds","campari",
               "fernet","amaro","suze","cynar","underberg","jagermeister"],
    "dairy": ["cream","milk","egg white","butter","yogurt","coconut milk",
              "almond milk","oat milk","half and half","irish cream"],
    "fizzy": ["soda water","tonic water","club soda","champagne","prosecco",
              "sparkling wine","cava","ginger ale","ginger beer","coke","cola"],
    "savory": ["olive","tomato","celery","cucumber","beet","carrot",
               "mushroom","truffle","soy sauce","sesame","miso","sea salt",
               "bacon","smoke","tabasco","worcestershire"],
    "floral": ["rose","lavender","violet","chamomile","elderflower","jasmine","hibiscus"],
    "tropical": ["coconut","pineapple","mango","passion fruit","guava","lychee","tamarind"],
    "nut": ["almond","walnut","hazelnut","pecan","coconut","orgeat","sesame","peanut"],
    "tea": ["green tea","black tea","chai","matcha","oolong","earl grey","chamomile tea"],
    "other": ["cucumber","celery","ginger","mint","egg white","cream","olive","cherry"]
}

# 收集所有风味词
ALL_FLAVOR_TERMS = set()
for terms in BASE_VOCAB.values():
    for t in terms:
        ALL_FLAVOR_TERMS.add(t.lower())

def build_vocab(force=False):
    """从数据库自动提取高频原料，扩充风味词库"""
    cache = VOCAB_FILE
    if os.path.exists(cache) and not force:
        age = (time.time() - os.path.getmtime(cache))
        if age < CACHE_TTL:
            return json.load(open(cache))
    
    # 统计DB中所有原料行中出现的风味词
    known_words = Counter()
    offset = 0
    while offset < 50000:
        r = dq(f"SELECT ingredients FROM cocktail_recipes WHERE LENGTH(ingredients)>5 LIMIT 2000 OFFSET {offset}")
        rows = json.loads(r['result']['content'][0]['text'])['rows']
        if not rows: break
        for rr in rows:
            text = rr.get("ingredients","").lower()
            for term in ALL_FLAVOR_TERMS:
                if term in text:
                    known_words[term] += 1
        offset += 2000
    
    # 统计高频非风味词（可能的新风味原料）
    raw_counts = Counter()
    offset = 0
    while offset < 20000:
        r = dq(f"SELECT ingredients FROM cocktail_recipes LIMIT 500 OFFSET {offset}")
        rows = json.loads(r['result']['content'][0]['text'])['rows']
        if not rows: break
        for rr in rows:
            text = rr.get("ingredients","").lower()
            # 提取冒号、逗号后的词 和 单位后的词
            candidates = re.findall(r'(?:after|oz|ml|cl|dash|tsp|tbsp|cup)\s*[\-–]?\s*([\w\s]{2,30}?)(?:\s*\||\s*$|\s*\n)', text)
            for c in candidates:
                c = c.strip().strip('.').strip()
                if c and len(c) > 2 and not any(d in c for d in "0123456789"):
                    raw_counts[c] += 1
        offset += 500
    
    # 找出出现10+次且不在基础词汇中的原料
    new_terms = {w:c for w,c in raw_counts.items() if c >= 10 and w not in ALL_FLAVOR_TERMS}
    
    vocab = {
        "known": {w:c for w,c in known_words.most_common()},
        "new_candidates": dict(sorted(new_terms.items(), key=lambda x:-x[1])[:50]),
        "total_recipes_analyzed": len(known_words),
        "built_at": datetime.now().isoformat()
    }
    
    with open(cache, "w") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
    
    return vocab

def show_vocab():
    """展示风味词库统计"""
    vocab = build_vocab()
    print(f"\n📊 风味词库状态")
    print(f"  {'='*40}")
    print(f"  基础风味词: {len(ALL_FLAVOR_TERMS)} 个")
    print(f"  已匹配到DB: {len(vocab['known'])} 个")
    print(f"  新候选词: {len(vocab['new_candidates'])} 个")
    
    print(f"\n  风味类别:")
    for cat, terms in sorted(BASE_VOCAB.items()):
        cnt = sum(1 for t in terms if vocab['known'].get(t,0) > 0)
        print(f"    {cat:12s}: {cnt}/{len(terms)} 个活跃")
    
    if vocab['new_candidates']:
        print(f"\n  🆕 建议新增的风味原料:")
        for w,c in list(vocab['new_candidates'].items())[:15]:
            print(f"    {w:25s} {c}次")

# ==================================================================
# L1: 风味关联图谱 — 共现矩阵 → 向量相似度
# ==================================================================

def build_cooccur_matrix(force=False):
    """构建风味共现矩阵"""
    cache = COOCCUR_FILE
    if os.path.exists(cache) and not force:
        age = time.time() - os.path.getmtime(cache)
        if age < CACHE_TTL:
            return json.load(open(cache))
    
    # 只使用活跃的风味词
    vocab = build_vocab()
    active = {w for w,c in vocab['known'].items() if c >= 10}
    
    print(f"  用 {len(active)} 个活跃风味词构建矩阵...", file=sys.stderr)
    
    cooccur = defaultdict(lambda: defaultdict(int))
    counts = Counter()
    
    offset = 0
    while offset < 50000:
        r = dq(f"SELECT ingredients FROM cocktail_recipes WHERE LENGTH(ingredients)>5 LIMIT 2000 OFFSET {offset}")
        rows = json.loads(r['result']['content'][0]['text'])['rows']
        if not rows: break
        for rr in rows:
            text = rr.get("ingredients","").lower()
            found = [w for w in active if w in text]
            for w in found:
                counts[w] += 1
            for i in range(len(found)):
                for j in range(i+1, len(found)):
                    cooccur[found[i]][found[j]] += 1
                    cooccur[found[j]][found[i]] += 1
        offset += 2000
    
    # 计算标准化相似度 (Jaccard)
    sim_matrix = {}
    for a in cooccur:
        sim_matrix[a] = {}
        for b in cooccur[a]:
            denom = counts[a] + counts[b] - cooccur[a][b]
            if denom > 0:
                sim_matrix[a][b] = round(cooccur[a][b] / max(denom, 1), 4)
    
    result = {"matrix": sim_matrix, "counts": dict(counts), "total_words": len(counts)}
    
    with open(cache, "w") as f:
        json.dump(result, f, ensure_ascii=False)
    
    return result

def l1_flavor_graph(base):
    """L1 升级版: 风味关联图谱 + 向量推荐"""
    global time
    import time
    
    eng = base.lower().strip()
    cn_map = {"gin":"gin","金酒":"gin","伏特加":"vodka","威士忌":"whiskey","whisky":"whiskey",
              "朗姆":"rum","朗姆酒":"rum","龙舌兰":"tequila","白兰地":"brandy",
              "干邑":"cognac","梅斯卡尔":"mezcal","波本":"bourbon","黑麦":"rye"}
    eng = cn_map.get(eng, eng)
    
    print(f"\n{'='*60}")
    print(f" L1 风味关联图谱: {base}")
    print(f"{'='*60}")
    
    data = build_cooccur_matrix()
    matrix = data["matrix"]
    counts = data["counts"]
    
    if eng not in matrix:
        print(f"\n❌ 数据库中缺少 '{eng}' 的足够数据")
        return
    
    total = counts.get(eng, 0)
    print(f"\n📊 基酒出现 {total} 次")
    print(f"  风味关联词: {len(matrix.get(eng, {}))} 个")
    
    # 按 Jaccard 相似度排序的灵魂伴侣
    pairs = sorted(matrix[eng].items(), key=lambda x: -x[1])
    
    print(f"\n🏆 灵魂伴侣 (按向量相似度排序):")
    for ing, sim in pairs[:12]:
        cnt = counts.get(ing, 0)
        bar = "█" * int(sim * 40)
        print(f"  {ing:25s} 相似度 {sim:.3f}  {bar:40s}  (共现 {cnt}次)")
    
    # 风味类别画像
    print(f"\n🎨 风味画像:")
    cat_scores = defaultdict(float)
    for ing, sim in pairs:
        for cat, terms in BASE_VOCAB.items():
            if ing in terms:
                cat_scores[cat] = max(cat_scores[cat], sim)
    for cat, score in sorted(cat_scores.items(), key=lambda x:-x[1])[:8]:
        bar = "▓" * int(score * 30)
        print(f"  {cat:12s} {score:.2f} {bar}")
    
    # 风味盲区（相似度极低的原料）
    all_terms = set()
    for terms in BASE_VOCAB.values():
        all_terms.update(terms)
    
    blind = [(t, matrix[eng].get(t, 0)) for t in all_terms 
             if t != eng and t not in matrix.get(eng, {}) and t in counts]
    
    print(f"\n🆕 风味盲区 (从未搭配但高频的原料):")
    for ing, _ in sorted(blind, key=lambda x: -counts.get(x[0],0))[:8]:
        print(f"  {ing:25s} (高频原料, 共现 {counts.get(ing,0)}次)")
    
    return pairs

# ==================================================================
# L3: 语义搜索
# ==================================================================

def l3_search(query):
    """自然语言配方搜索"""
    print(f"\n{'='*60}")
    print(f"🔍 搜索: {query}")
    print(f"{'='*60}")
    
    q = query.lower()
    
    # 提取基酒
    spirits = {"gin":"gin","金酒":"gin","伏特加":"vodka","威士忌":"whiskey","bourbon":"bourbon",
               "rum":"rum","朗姆":"rum","龙舌兰":"tequila","mezcal":"mezcal","brandy":"brandy",
               "白兰地":"brandy","pisco":"pisco","cognac":"cognac","威士忌":"whiskey"}
    target_spirit = None
    for cn, en in spirits.items():
        if cn in q:
            target_spirit = en
            break
    
    # 提取风味偏好（正向）
    likes = []
    flavor_keywords = {
        "烟熏":"smoky","smoky":"smoky","甜":"sweet","sweet":"sweet","酸":"sour","sour":"sour",
        "苦":"bitter","bitter":"bitter","辣":"spicy","spicy":"spicy","清爽":"refreshing",
        "refreshing":"refreshing","花香":"floral","floral":"floral","热带":"tropical",
        "tropical":"tropical","草本":"herbal","herbal":"herbal","creamy":"creamy","奶油":"creamy",
        "果味":"fruity","fruity":"fruity","气泡":"fizzy","fizzy":"fizzy",
        "forest":"herbal","森林":"herbal","earthy":"earthy","泥土":"earthy"
    }
    for kw, val in flavor_keywords.items():
        if kw in q:
            likes.append(val)
    
    # 提取排除项
    dislikes = []
    neg_patterns = re.findall(r'不要([\w]+)|不要\s+([\w]+)|没[\w]+|不含([\w]+)|without\s+([\w]+)', q)
    for groups in neg_patterns:
        for g in groups:
            if g: dislikes.append(g.lower())
    
    # 提取杯型/场景
    glasses = {"highball":"highball","rock":"rocks","old-fashioned":"old-fashioned",
               "马天尼":"martini","马丁尼":"martini","coupe":"coupe"}
    target_glass = None
    for g, val in glasses.items():
        if g in q: target_glass = val
    
    print(f"\n📋 搜索意图解析:")
    if target_spirit: print(f"  基酒: {target_spirit}")
    if likes: print(f"  风味: {', '.join(likes)}")
    if dislikes: print(f"  排除: {', '.join(dislikes)}")
    
    # 构建SQL
    sql = "SELECT name, source, ingredients, method FROM cocktail_recipes WHERE 1=1"
    sql += " AND LENGTH(ingredients) > 20 AND LENGTH(ingredients) < 2000"
    if target_spirit:
        sql += f" AND (LOWER(ingredients) LIKE '%{target_spirit}%' OR LOWER(name) LIKE '%{target_spirit}%')"
    for like in likes[:3]:
        if like == "refreshing":
            sql += " AND (LOWER(ingredients) LIKE '%lime%' OR LOWER(ingredients) LIKE '%lemon%' OR LOWER(ingredients) LIKE '%mint%' OR LOWER(ingredients) LIKE '%cucumber%')"
        elif like == "fizzy":
            sql += " AND (LOWER(ingredients) LIKE '%soda%' OR LOWER(ingredients) LIKE '%tonic%' OR LOWER(ingredients) LIKE '%champagne%' OR LOWER(ingredients) LIKE '%prosecco%')"
        elif like == "smoky":
            sql += " AND (LOWER(ingredients) LIKE '%mezcal%' OR LOWER(ingredients) LIKE '%smoky%' OR LOWER(ingredients) LIKE '%scotch%' OR LOWER(ingredients) LIKE '%islay%')"
        elif like == "herbal":
            sql += " AND (LOWER(ingredients) LIKE '%mint%' OR LOWER(ingredients) LIKE '%basil%' OR LOWER(ingredients) LIKE '%herbal%' OR LOWER(ingredients) LIKE '%chartreuse%' OR LOWER(ingredients) LIKE '%absinthe%')"
        else:
            sql += f" AND LOWER(ingredients) LIKE '%{like}%'"
    for dislike in dislikes[:3]:
        sql += f" AND LOWER(ingredients) NOT LIKE '%{dislike}%'"
    
    sql += " ORDER BY LENGTH(ingredients) DESC LIMIT 10"
    
    r = dq(sql)
    rows = json.loads(r['result']['content'][0]['text'])['rows']
    
    if not rows:
        print(f"\n❌ 未找到匹配配方。试试放松条件。")
        return
    
    print(f"\n🏆 Top {len(rows)} 推荐:")
    for i, rr in enumerate(rows, 1):
        name = rr.get("name","").strip()[:35]
        src = rr.get("source","").strip()[:25]
        ings = rr.get("ingredients","")[:80].replace("\n",", ")
        print(f"\n  {i}. {name}")
        print(f"     📖 {src}")
        print(f"     🧪 {ings}...")

# ==================================================================
# CLI
# ==================================================================

if __name__ == "__main__":
    print("🥃 DRINK MASTER v3.0 — 风味关联图谱 + 语义搜索")
    print(f"{'='*50}")
    
    if len(sys.argv) < 2:
        print("\n用法:")
        print("  python3 drink_master.py l4-vocab        # 查看风味词库统计")
        print("  python3 drink_master.py l1 gin          # L1 风味关联图谱")
        print("  python3 drink_master.py l1 金酒          # 支持中文")
        print("  python3 drink_master.py search 烟熏味的金酒不要柠檬  # 语义搜索")
        print("  python3 drink_master.py rebuild          # 重新构建风味数据")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "l4-vocab":
        import time; show_vocab()
    elif cmd == "rebuild":
        import time
        print("重新构建风味词库...")
        build_vocab(force=True)
        print("重新构建共现矩阵...")
        build_cooccur_matrix(force=True)
        print("✅ 完成")
    elif cmd == "l1" and len(sys.argv) >= 3:
        l1_flavor_graph(sys.argv[2])
    elif cmd == "search" and len(sys.argv) >= 3:
        l3_search(" ".join(sys.argv[2:]))
    elif cmd == "l3":
        # Alias
        l3_search(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else "")
    else:
        print(f"未知命令: {cmd}")
