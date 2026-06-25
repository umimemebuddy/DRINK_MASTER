#!/usr/bin/env python3
"""
🥃 DRINK MASTER v4.0 — 新增模块
===================================
L2v2: 风格迁移 — 从数据中学习"提基风/禁酒令风/日式风"的精髓
L3v2: 库存感知创造 — 给原料清单就出配方
L5:  数据清洗 — 修复脏数据
"""

import json, subprocess, sys, re, os, math, time
from collections import Counter, defaultdict
from datetime import datetime

DDB = "http://127.0.0.1:8766"

def dq(sql):
    r = subprocess.run(["curl","-s","-X","POST",DDB,"-H","Content-Type: application/json",
        "-d",json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"duck_query","arguments":{"sql":sql}}})],
        capture_output=True,text=True,timeout=15)
    return json.loads(r.stdout)

def mc(url,p):
    r = subprocess.run(["curl","-s","-X","POST",url,"-H","Content-Type: application/json",
        "-d",json.dumps(p)],capture_output=True,text=True,timeout=30)
    try:
        d=json.loads(r.stdout)
        if "error" in d: return {"_error":d["error"]}
        return json.loads(d["result"]["content"][0]["text"])
    except: return {"_error":"fail"}

# ==================================================================
# L5: 数据清洗
# ==================================================================

def l5_cleanup():
    """清洗数据：删除脏条目，补全格式"""
    print(f"\n{'='*60}")
    print(f"🧹 L5 数据清洗")
    print(f"{'='*60}")
    
    # 1. 删除垃圾条目
    print(f"\n📋 1. 删除垃圾数据...")
    
    del_conditions = [
        "LENGTH(TRIM(name)) < 3",
        "LOWER(name) LIKE 'index %'",
        "LOWER(name) LIKE 'glossary%'",
        "LOWER(name) LIKE 'acknowledgment%'",
        "LOWER(name) LIKE 'introduction%'",
        "LOWER(name) LIKE 'bibliography%'",
        "LOWER(name) LIKE 'table of content%'",
        "LOWER(name) LIKE 'about the author%'",
        "LOWER(name) = 'index'",
        "LOWER(name) = 'conclusion'",
        "LOWER(name) = 'introduction'",
        "LOWER(name) LIKE 'license%'",
        "LOWER(name) LIKE 'copyright%'",
    ]
    
    total_del = 0
    for cond in del_conditions:
        r = dq(f"SELECT COUNT(*) as c FROM cocktail_recipes WHERE {cond}")
        cnt = int(json.loads(r['result']['content'][0]['text'])['rows'][0]['c'])
        if cnt:
            r = dq(f"DELETE FROM cocktail_recipes WHERE {cond}")
            print(f"    ✅ 删除 '{cond.split('LIKE')[-1].strip() if 'LIKE' in cond else cond.split('=')[0].strip()}' 类 {cnt} 条")
            total_del += cnt
    
    print(f"    共删除 {total_del} 条脏数据")
    
    # 2. 修复缺配料的条目 — 从 method 或 full_content 中提取
    print(f"\n📋 2. 修复缺配料的条目...")
    
    # 查找缺配料但有内容可提取的
    r = dq("SELECT id, name, method, full_content FROM cocktail_recipes "
           "WHERE LENGTH(COALESCE(ingredients,'')) < 5 "
           "AND (LENGTH(COALESCE(method,'')) > 20 OR LENGTH(COALESCE(full_content,'')) > 50) "
           "LIMIT 2000")
    rows = json.loads(r['result']['content'][0]['text'])['rows']
    fixed = 0
    for rr in rows:
        rid = rr["id"]
        content = rr.get("full_content","") or rr.get("method","") or ""
        # 提取前200字符作为配料（包含配方名以后的文本）
        if len(content) > 20:
            snippet = content[:300]
            dq(f"UPDATE cocktail_recipes SET ingredients = '{snippet.replace(chr(39), chr(39)*2)}' WHERE id = {rid}")
            fixed += 1
        if fixed % 300 == 0:
            print(f"    已修复 {fixed} 条...")
    print(f"    共修复 {fixed} 条缺配料条目")
    
    # 3. 统计清洗后
    print(f"\n📋 3. 最终统计:")
    r = dq("SELECT COUNT(*) as c FROM cocktail_recipes")
    total = int(json.loads(r['result']['content'][0]['text'])['rows'][0]['c'])
    r = dq("SELECT COUNT(*) as c FROM cocktail_recipes WHERE LENGTH(COALESCE(ingredients,'')) < 5")
    still_bad = int(json.loads(r['result']['content'][0]['text'])['rows'][0]['c'])
    r = dq("SELECT COUNT(*) as c FROM cocktail_recipes WHERE LENGTH(COALESCE(method,'')) > 5")
    has_method = int(json.loads(r['result']['content'][0]['text'])['rows'][0]['c'])
    
    print(f"    总条目: {total}")
    print(f"    仍有配料问题: {still_bad}")
    print(f"    有做法: {has_method} ({has_method*100//total}%)")
    print(f"\n✅ 清洗完成")

# ==================================================================
# L2v2: 风格迁移
# ==================================================================

STYLES = {}

def extract_style_signatures():
    """从数据库中提取各风格的风味特征向量"""
    global STYLES
    
    # 定义风格的搜索特征
    style_defs = {
        "tiki": {
            "name": "🏝️ 提基风 (Tiki)",
            "desc": "复杂酸甜与香料的热带狂欢",
            "keywords": ["orgeat","falernum","mai tai","zombie","hurricane","tiki",
                        "passion fruit","pineapple","coconut cream","allspice dram"],
            "spirits": ["rum","dark rum","light rum","aged rum","jamaican rum"],
            "method": ["shake","crushed ice"],
            "glass": ["tiki","collins","highball"],
            "profile": {"tropical":0.9, "sweet":0.7, "sour":0.6, "nutty":0.5, 
                       "spice":0.4, "creamy":0.3, "fruity":0.8, "boozy":0.5}
        },
        "prohibition": {
            "name": "🚫 禁酒令风 (Prohibition Era)",
            "desc": "重酸甜香料掩盖劣酒的地下酒吧风格",
            "keywords": ["prohibition","speakeasy","bootleg","bathtub"],
            "spirits": ["gin","whiskey","rye","bourbon","bathtub gin"],
            "method": ["shake","strain"],
            "glass": ["coupe","cocktail"],
            "profile": {"sweet":0.8, "sour":0.7, "spice":0.5, "herbal":0.4,
                       "boozy":0.6, "bitter":0.3, "fruity":0.5}
        },
        "japanese": {
            "name": "🇯🇵 日式调酒 (Japanese Style)",
            "desc": "极简精准，突出基酒本质",
            "keywords": ["japanese","hard shake","yuzu","shiso","umeshu","sake",
                        "matcha","green tea","wasabi"],
            "spirits": ["whiskey","gin","vodka","sake","shochu"],
            "method": ["hard shake","stir"],
            "glass": ["rocks","old-fashioned"],
            "profile": {"herbal":0.5, "floral":0.4, "cooling":0.5, "boozy":0.5,
                       "sweet":0.3, "sour":0.3, "fruity":0.3, "earthy":0.3}
        },
        "classic": {
            "name": "📕 经典风 (Classic)",
            "desc": "时间检验的经典配方结构",
            "keywords": ["classic","traditional","old fashioned","sour","martini","manhattan"],
            "spirits": ["gin","whiskey","bourbon","rye","rum","vodka","tequila"],
            "method": ["stir","shake"],
            "glass": ["coupe","rocks","martini"],
            "profile": {"boozy":0.7, "sweet":0.4, "sour":0.4, "bitter":0.3,
                       "herbal":0.3, "fruity":0.2}
        },
        "modern": {
            "name": "🧪 现代风 (Modern Craft)",
            "desc": "创意混搭，非常规原料",
            "keywords": ["modern","craft","artisanal","seasonal","farmers","contemporary",
                        "infused","fat-washed","clarified"],
            "spirits": ["gin","vodka","mezcal","whiskey","rum"],
            "method": ["shake","stir","muddle","smoke"],
            "glass": ["coupe","rocks","nick & nora"],
            "profile": {"savory":0.4, "herbal":0.5, "fruity":0.4, "boozy":0.5,
                       "smoky":0.3, "earthy":0.3, "spice":0.3}
        },
        "sour_family": {
            "name": "🍋 酸酒家族 (Sour Family)",
            "desc": "基酒+柑橘+甜=万能框架",
            "keywords": ["sour","daiquiri","sidecar","whiskey sour","lemon","lime"],
            "spirits": ["gin","whiskey","bourbon","rye","rum","tequila","pisco","brandy"],
            "method": ["shake","strain"],
            "glass": ["coupe","rocks"],
            "profile": {"sour":0.8, "sweet":0.5, "fruity":0.4, "boozy":0.6, "cooling":0.3}
        }
    }
    
    # 构建共现矩阵（复用L1的数据）
    print("\n📊 从数据库提取风格特征...", file=sys.stderr)
    
    STYLES = {}
    for sname, sdef in style_defs.items():
        name = sdef["name"]
        keywords = sdef["keywords"]
        
        # 查db中有多少匹配
        kw_clause = " OR ".join([f"LOWER(name) LIKE '%{k}%' OR LOWER(source) LIKE '%{k}%' OR LOWER(ingredients) LIKE '%{k}%'" for k in keywords])
        r = dq(f"SELECT COUNT(*) as c FROM cocktail_recipes WHERE {kw_clause} LIMIT 1")
        cnt = int(json.loads(r['result']['content'][0]['text'])['rows'][0]['c'])
        
        # 取前几条样例
        r2 = dq(f"SELECT name FROM cocktail_recipes WHERE {kw_clause} LIMIT 5")
        samples_raw = json.loads(r2['result']['content'][0]['text'])['rows']
        samples = [rr["name"] for rr in samples_raw if "name" in rr]
        
        # 提取该风格的典型配料
        r3 = dq(f"SELECT ingredients FROM cocktail_recipes WHERE {kw_clause} AND LENGTH(ingredients)>20 LIMIT 50")
        ings_rows = json.loads(r3['result']['content'][0]['text'])['rows']
        
        ing_counter = Counter()
        for rr in ings_rows:
            text = rr.get("ingredients","").lower()
            for term in ["lemon","lime","orange","pineapple","coconut","mint","cream",
                        "simple syrup","orgeat","honey","egg white","bitters","soda",
                        "tonic","champagne","ginger","cinnamon","nutmeg","vanilla",
                        "coffee","chocolate","cream","milk","salt","pepper","cucumber"]:
                if term in text:
                    ing_counter[term] += 1
        
        top_ings = [w for w,_ in ing_counter.most_common(6)] if ing_counter else []
        
        STYLES[sname] = {
            "name": name,
            "desc": sdef["desc"],
            "count": cnt,
            "profile": sdef["profile"],
            "suggested_spirits": sdef["spirits"],
            "method": sdef.get("method",["shake"])[0],
            "glass": sdef.get("glass",["rocks"])[0],
            "typical_ingredients": top_ings,
            "samples": samples[:3]
        }
        
        print(f"  {name:25s}  {cnt:>4}条  典型: {', '.join(top_ings[:4])}", file=sys.stderr)
    
    return STYLES


def l2_style_create(base_spirit, style_name):
    """L2 风格迁移 — 将风格运用到新的基酒上"""
    global STYLES
    
    if not STYLES:
        extract_style_signatures()
    
    # 匹配风格
    style = STYLES.get(style_name)
    if not style:
        # 尝试部分匹配
        matches = [s for s in STYLES if style_name in s or style_name in STYLES[s]["name"]]
        if matches:
            style = STYLES[matches[0]]
        else:
            print(f"\n❌ 未知风格: {style_name}")
            print(f"   可用风格: {', '.join(s+'('+d['name']+')' for s,d in STYLES.items())}")
            return None
    
    profile = style["profile"]
    s_method = style.get("method","Shake")
    s_glass = style.get("glass","Rocks")
    
    # 解决中文名
    cn = {"gin":"金酒","vodka":"伏特加","whiskey":"威士忌","bourbon":"波本",
           "rum":"朗姆","tequila":"龙舌兰","mezcal":"梅斯卡尔","brandy":"白兰地",
           "pisco":"皮斯科","cognac":"干邑"}
    spirit_cn = cn.get(base_spirit.lower(), base_spirit)
    
    # 按风格和基酒生成配方
    if style_name == "tiki":
        ings = [f"45ml {spirit_cn}"]
        ings += ["22ml lime juice","22ml pineapple juice","15ml orgeat","15ml orange curacao"]
        if base_spirit.lower() in ["rum"]: ings.insert(0,"15ml aged rum (complexity)")
        method = "Shake all with crushed ice. Open pour into Tiki mug. Top with crushed ice."
        garnish = "Mint sprig + edible flower + paper umbrella"
        
    elif style_name == "prohibition":
        ings = [f"45ml {spirit_cn}","15ml apricot brandy","22ml lemon juice","15ml honey syrup",
                "2 dashes Angostura bitters","1 egg white"]
        method = "Dry shake 10s, add ice, shake 15s. Double strain into chilled coupe."
        garnish = "Orange peel + 1 clove"
        
    elif style_name == "japanese":
        ings = [f"45ml {spirit_cn}","2 barspoon simple syrup","2 dashes orange bitters"]
        if "酸" in style.get("desc",""):
            ings.insert(1,"15ml yuzu juice")
        method = "Hard shake: shake with big ice cube 15s. Strain into chilled rocks glass over one large ice ball."
        garnish = "Yuzu peel twist"
        
    elif style_name == "classic":
        ings = [f"60ml {spirit_cn}","2 dashes Angostura bitters","1 tsp simple syrup","1 tsp water"]
        method = "Stir with ice 30s. Strain over one large ice cube."
        garnish = "Orange peel expressed"
        
    elif style_name == "modern":
        ings = [f"45ml {spirit_cn}","22ml lemon juice","15ml honey syrup","15ml ginger syrup","1 sprig rosemary"]
        method = "Muddle rosemary with syrups. Add spirits and lemon. Shake 12s. Fine strain."
        garnish = "Rosemary sprig + lemon wheel"
        
    elif style_name == "sour_family":
        ings = [f"45ml {spirit_cn}","22ml lemon juice","15ml simple syrup","1 egg white (optional)"]
        method = "Dry shake, then wet shake. Strain into chilled coupe."
        garnish = "Lemon wheel + 3 drops Angostura on foam"
    else:
        # 未知风格→基于profile做
        ings = [f"45ml {spirit_cn}"]
        if profile.get("sour",0) > 0.5: ings.append("22ml lemon juice")
        if profile.get("sweet",0) > 0.5: ings.append("15ml simple syrup")
        if profile.get("bitter",0) > 0.3: ings.append("2 dashes bitters")
        if len(ings) < 3: ings.append("soda water to top")
        method = s_method
        garnish = "Citrus twist"
    
    return {
        "name": f"{style['name']} {spirit_cn}",
        "style": style["name"],
        "glass": s_glass,
        "method": method,
        "garnish": garnish,
        "ingredients": ings,
        "abv": "18%-22%" if "sour" in method.lower() or "juice" in str(ings) else "28%-32%",
        "flavor_notes": [
            style["desc"],
            f"基酒 '{base_spirit}' 的{f'热带' if 'tiki' in style_name else f'{style_name}'}演绎"
        ]
    }


# ==================================================================
# L3v2: 库存感知创造
# ==================================================================

COMMON_INGREDIENTS = {
    "lemon": "lemon juice", "lime": "lime juice", "orange": "orange juice",
    "糖浆": "simple syrup", "honey":"honey", "蜜":"honey",
    "鸡蛋":"egg white", "蛋清":"egg white", "cream":"cream", "鲜奶油":"cream",
    "soda":"soda water", "苏打":"soda water", "tonic":"tonic water",
    "ginger":"ginger", "姜":"ginger", "mint":"mint", "薄荷":"mint",
    "cinnamon":"cinnamon", "肉桂":"cinnamon",
}


def l3_craft(inventory_str):
    """库存感知创造 — 给原料清单，出配方"""
    print(f"\n{'='*60}")
    print(f"🍸 L3 库存感知创造")
    print(f"{'='*60}")
    print(f"  库存: {inventory_str}")
    
    # 解析库存
    items = {}
    spirit = None
    spirit_vol = 0
    sweeteners = []
    sours = []
    other = []
    
    parts = re.split(r'[,，、]', inventory_str)
    for p in parts:
        p = p.strip()
        if not p: continue
        
        # 提取数量和名称
        qty = 0
        name = p
        
        # 尝试匹配 "中文名:数量单位" 格式
        cm = re.match(r'([\u4e00-\u9fff\w]+)[:：]\s*([\d.]+)\s*(\w*)', p)
        if cm:
            name = cm.group(1).lower()
            qty = float(cm.group(2))
        
        # 尝试匹配 "数量单位中文名" 格式  
        if not qty:
            m = re.search(r'([\d.]+)\s*(\w*)\s*([\u4e00-\u9fff]+)', p)
            if m:
                qty = float(m.group(1))
                name = m.group(3).lower()
                if m.group(2) in ["ml","cl"]: pass  # already in ml
                elif m.group(2) in ["oz"]: qty = qty * 30  # oz to ml
                elif not qty: qty = 0  # unknown unit
        
        # 尝试匹配纯中文
        if not qty:
            m = re.match(r'([\u4e00-\u9fff]+)(?:[:：])?(.+)?', p.strip())
            if m:
                name = m.group(1).lower()
                if "半" in p: qty = 0.5
        
        # 标准化名称和数量
        if name in COMMON_INGREDIENTS:
            name = COMMON_INGREDIENTS[name]
        
        # 归一化同义词
        syn_map = {"黄柠":"柠檬","青柠":"lime","黄柠檬":"柠檬","绿柠":"lime",
                   "白砂糖":"sugar","冰糖":"sugar","赤砂糖":"brown sugar",
                   "鲜奶油":"cream","淡奶油":"cream","全脂牛奶":"milk"}
        for old, new in syn_map.items():
            if old in name:
                name = new
                break
        
        # 解释特殊数量词
        if "半" in p and not re.search(r'[\d.]+', p):
            qty = 0.5
        if qty < 1 and ("柠檬" in name or "lime" in name or "lemon" in name or "橙" in name or "橘子" in name):
            qty = qty * 30  # 半个柠檬≈15ml, 1/4个≈7.5ml
        
        # 分类
        spirits = {"gin":"gin","金酒":"gin","vodka":"伏特加","威士忌":"whiskey","whiskey":"whiskey","whisky":"whiskey",
                   "rum":"rum","朗姆":"rum","朗姆酒":"rum","龙舌兰":"tequila","tequila":"tequila",
                   "白兰地":"brandy","brandy":"brandy","mezcal":"mezcal",
                   "bourbon":"bourbon"}
        
        if name in spirits:
            spirit = spirits[name]
            spirit_vol = qty
            continue
        
        # 尝试部分匹配
        matched = False
        for sn, sv in spirits.items():
            if sn in name or name in sn:
                spirit = sv
                spirit_vol = qty
                matched = True
                break
        if matched:
            continue
        
        # 配料分类
        if "lemon" in name or "lime" in name or "柠" in name or "酸" in name or "citrus" in name:
            sours.append((name, qty))
        elif "syrup" in name or "糖" in name or "honey" in name or "蜜" in name or "sugar" in name:
            sweeteners.append((name, qty))
        elif qty > 0:
            other.append((name, qty))
    
    if not spirit:
        print("\n❌ 未识别到基酒！请确保提供基酒名称。")
        print("   识别基酒: gin/金酒/vodka/伏特加/whiskey/威士忌/rum/朗姆/tequila/龙舌兰")
        return
    
    print(f"\n📋 库存解析:")
    print(f"  基酒: {spirit} ({spirit_vol}ml)")
    if sours: print(f"  酸: {', '.join(f'{n}({v})' for n,v in sours)}")
    if sweeteners: print(f"  甜: {', '.join(f'{n}({v})' for n,v in sweeteners)}")
    if other: print(f"  其他: {', '.join(f'{n}({v})' for n,v in other)}")
    
    # 智能决定做什么风格的酒
    has_sour = bool(sours)
    has_sweet = bool(sweeteners)
    
    if has_sour and has_sweet:
        # Sour风格
        sour_ing = sours[0][0] if sours else "lemon juice"
        sweet_ing = sweeteners[0][0] if sweeteners else "simple syrup"
        ings = [f"{spirit_vol}ml {spirit}"]
        if spirit_vol < 60:
            # 延长
            ings.append(f"{sours[0][1] if sours else 15}ml {sour_ing}")
            ings.append(f"{sweeteners[0][1] if sweeteners else 10}ml {sweet_ing}")
            if other: ings.append(f"{other[0][1]}ml {other[0][0]} (补满)")
        else:
            ings.append(f"15ml {sour_ing}")
            ings.append(f"10ml {sweet_ing}")
        
        method = "Shake with ice for 15 seconds. Fine strain into chilled glass."
        glass = "Coupe"
        style = "Sour 变体"
        
    elif has_sweet and not has_sour:
        # Old Fashioned风格
        sweet_ing = sweeteners[0][0] if sweeteners else "simple syrup"
        ings = [f"{spirit_vol}ml {spirit}",f"1 barspoon {sweet_ing}","2 dashes bitters"]
        method = "Stir with ice. Serve over one large cube."
        glass = "Old-Fashioned"
        style = "Old Fashioned 变体"
        
    else:
        # Highball风格
        ings = [f"{spirit_vol}ml {spirit}"]
        if spirit_vol < 60:
            ings.append("Soda/tonic water to top")
        method = "Build in highball with ice. Stir gently."
        glass = "Highball"
        style = "Highball 变体"
    
    print(f"\n{'='*60}")
    print(f"  🍸 定制配方")
    print(f"  {style} | {glass} | ABV 约{spirit_vol*40//max(spirit_vol+sum(v for _,v in sours+other),1)}%")
    print(f"{'='*60}")
    for ing in ings:
        print(f"  • {ing}")
    print(f"\n  👨‍🍳 {method}")
    
    # 风味说明
    total = spirit_vol + sum(v for _,v in sours) + sum(v for _,v in sweeteners) + sum(v for _,v in other)
    if total <= spirit_vol * 1.5:
        note = "高度数型 — 基酒风味主导，适合纯饮爱好者"
    elif has_sour and has_sweet:
        note = "酸甜平衡型 — 经典结构，容易入口"
    else:
        note = "清爽延长型 — 低度数，适合慢慢喝"
    
    print(f"\n  💡 {note}")
    
    return {"spirit":spirit, "style":style, "ingredients":ings, "method":method, "glass":glass}


# ==================================================================
# CLI
# ==================================================================

if __name__ == "__main__":
    print("🥃 DRINK MASTER v4.0 模块")
    print(f"{'='*50}")
    
    if len(sys.argv) < 2:
        print("\n新增命令:")
        print("  python3 drink_master.py l5-clean        # 数据清洗")
        print("  python3 drink_master.py styles           # 列出所有风格")
        print("  python3 drink_master.py migrate 金酒 tiki  # 风格迁移")
        print("  python3 drink_master.py craft 朗姆酒:35ml,柠檬:半个,蜂蜜:15ml  # 库存创造")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "l5-clean":
        l5_cleanup()
    elif cmd == "styles":
        styles = extract_style_signatures()
        print(f"\n{'='*60}")
        print(f"🎨 可用风格")
        print(f"{'='*60}")
        for sname, sdef in styles.items():
            print(f"\n  {sdef['name']}")
            print(f"    {sdef['desc']}")
            print(f"    数据量: {sdef['count']}条")
            print(f"    基酒: {', '.join(sdef['suggested_spirits'][:4])}")
            print(f"    典型配料: {', '.join(sdef['typical_ingredients'][:4])}")
    elif cmd == "migrate" and len(sys.argv) >= 4:
        result = l2_style_create(sys.argv[2], sys.argv[3])
        if result:
            print(f"\n{'='*60}")
            print(f"  🍸 {result['name']}")
            print(f"  风格: {result['style']} | 杯具: {result['glass']} | ABV: {result['abv']}")
            print(f"{'='*60}")
            for ing in result['ingredients']:
                print(f"  • {ing}")
            print(f"\n  👨‍🍳 {result['method']}")
            print(f"  🌿 {result['garnish']}")
            for note in result['flavor_notes']:
                print(f"  💡 {note}")
    elif cmd == "craft" and len(sys.argv) >= 3:
        l3_craft(sys.argv[2])
    else:
        print(f"未知命令: {cmd}")
