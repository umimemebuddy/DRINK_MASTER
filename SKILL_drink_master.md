---
name: drink-master
description: 饮品大师系统 - 50K配方风味智能。风味图谱(L1)+风格迁移(L2)+语义搜索(L3)+库存创造(L4)+数据清洗(L5)
category: cocktail
trigger: 用户提到"调酒"、"风味"、"配方"、"鸡尾酒"、"style migration"、"库存创造"、"craft"、"风格迁移"
---

# 🥃 DRINK MASTER v4.0 — 饮品大师系统技能

## Overview

基于 **49,375条真实配方** 的风味智能系统。提供 5 层能力：

| 层级 | 能力 | 命令 |
|------|------|------|
| **L1** | 🧠 风味关联图谱 | `python3 drink_master.py l1 gin` |
| **L2** | 🎨 风格迁移 | `python3 drink_master_v4.py migrate 金酒 tiki` |
| **L3** | 🔍 语义搜索 | `python3 drink_master.py search "烟熏味的金酒不要柠檬"` |
| **L4** | 🍸 库存创造 | `python3 drink_master_v4.py craft "朗姆:35ml,柠檬:半个"` |
| **L5** | 🧹 数据清洗 | `python3 drink_master_v4.py l5-clean` |

**仓库位置**: `~/Desktop/DRINK_MASTER_v4.0/` (打包版本)
**系统文件**: `~/Desktop/drink_master.py` (v3.0) + `~/Desktop/drink_master_v4.py` (v4.0)
**备份位置**: `~/Desktop/备份和系统文件/`

---

## L1: 风味关联图谱 — Flavor Graph

### 核心原理

Jaccard 相似度算法 → 量化 "灵魂伴侣" 程度：

```
similarity(A, B) = cooccurrence(A, B) / (count(A) + count(B) - cooccurrence(A, B))
```

从50K配方中**自动构建**共现矩阵（105+活跃风味词），支持中英文。

### 使用

```bash
python3 drink_master.py l1 gin
python3 drink_master.py l1 金酒
```

### 输出示例

```
🏆 灵魂伴侣 (按向量相似度排序):
  lemon        相似度 0.213  ████████    (共现 515次)
  vermouth     相似度 0.207  ████████    (共现 367次)
  orange       相似度 0.147  █████        (共现 467次)

🎨 风味画像:
  citrus       0.21 ▓▓▓▓▓▓
  liqueur      0.21 ▓▓▓▓▓▓
  sweetener    0.13 ▓▓▓

🆕 风味盲区 (从未搭配但高频的原料):
  irish cream  (共现 49次)  ← 金酒从来没和百利甜搭配过！
```

### 风味词库（L4）

```bash
python3 drink_master.py l4-vocab
```

- **178个**基础风味词（中英文）
- **161个**已在数据库中匹配（91%覆盖率）
- 自动发现新候选风味词

**风味类别**（16类）：
`spirit, liqueur, citrus, fruit, herb, spice, sweetener, bitter, dairy, fizzy, savory, floral, tropical, nut, tea, other`

---

## L2: 风格迁移 — Style Migration

### 可用风格（从数据中自动学习）

| 风格 | 数据库支撑 | 典型基酒 | 特征 |
|------|:---------:|---------|------|
| 🏝️ **tiki** 提基风 | 5,389条 | rum | orgeat+pineapple+复杂酸甜 |
| 🚫 **prohibition** 禁酒令风 | 398条 | gin, whiskey | 重酸甜+香料+苦精 |
| 🇯🇵 **japanese** 日式调酒 | 647条 | whiskey, gin | 极简+精准+yuzu |
| 📕 **classic** 经典风 | 6,407条 | 任意 | 老式结构+时间检验 |
| 🧪 **modern** 现代风 | 2,723条 | 任意 | 非常规原料+创意 |
| 🍋 **sour_family** 酸酒家族 | 17,658条 | 任意 | 万能框架 |

### 使用

```bash
# 查看所有风格
python3 drink_master_v4.py styles

# 风格迁移：用Tiki手法做威士忌
python3 drink_master_v4.py migrate 威士忌 tiki

# 禁酒令风金酒
python3 drink_master_v4.py migrate gin prohibition
```

### 输出示例

```
  🍸 🏝️ 提基风 (Tiki) 威士忌
  风格: 🏝️ 提基风 | 杯具: tiki | ABV: 18%-22%
  • 45ml 威士忌
  • 22ml lime juice
  • 22ml pineapple juice
  • 15ml orgeat
  • 15ml orange curacao
  👨‍🍳 Shake all with crushed ice.
  🌿 Mint sprig + edible flower + paper umbrella
  💡 基酒 '威士忌' 的热带演绎
```

---

## L3: 语义搜索 — Semantic Search

### 使用

```bash
python3 drink_master.py search "烟熏味的金酒不要柠檬"
python3 drink_master.py search "清爽的朗姆热带风"
python3 drink_master.py search "creamy vodka with coffee"
```

### 支持的自然语言意图

| 意图 | 关键词 | 触发条件 |
|------|--------|---------|
| 基酒 | gin/金酒/vodka/伏特加/rum/朗姆/whiskey/威士忌 | 中英文自动识别 |
| 风味 | 烟熏/甜/酸/苦/花香/草本/热带/creamy/refreshing | 映射到SQL条件 |
| 排除 | 不要XX/without XX/不含XX | NOT LIKE 过滤 |
| 杯型 | highball/martini/coupe/老式 | 返回不过滤 |

---

## L4: 库存感知创造 — Inventory Craft

### 使用

```bash
python3 drink_master_v4.py craft "朗姆酒:35ml,柠檬:半个,蜂蜜:15ml"
python3 drink_master_v4.py craft "gin:45ml,lime:30ml,syrup:15ml"
python3 drink_master_v4.py craft "陈年朗姆:35ml,黄柠:半个"
```

### 自动识别功能

- **基酒**: 中英文自动匹配（朗姆酒→rum, 陈年朗姆→rum, 金酒→gin）
- **同义词**: 黄柠→柠檬, 青柠→lime, 鲜奶油→cream
- **数量**: 半个柠檬→15ml, 1oz→30ml
- **结构推断**: 有酸+有甜→Sour，只有甜→Old Fashioned，只有基酒→Highball

### 输出示例

```
🍸 L3 库存感知创造
库存: 陈年朗姆:35ml,黄柠:半个,蜂蜜:10ml

📋 库存解析:
  基酒: rum (35.0ml)
  酸: 柠檬(15.0ml)
  甜: 蜂蜜(10.0ml)

🍸 定制配方
  Sour 变体 | Coupe | ABV 约28%
  • 35.0ml rum
  • 15.0ml 柠檬
  • 10.0ml 蜂蜜
  👨‍🍳 Shake with ice for 15 seconds.
  💡 酸甜平衡型 — 经典结构，容易入口
```

---

## L5: 数据清洗 — Data Cleanup

### 使用

```bash
python3 drink_master_v4.py l5-clean
```

### 清洗内容

1. 删除垃圾条目：索引页、目录、致谢、版权声明
2. 修复缺配料条目：从 `method` 或 `full_content` 填充
3. 删除条件：名称<3字符、INDEX/GLOSSARY/introduction/conclusion/copyright/license 类

---

## 📦 备份与恢复

### 备份文件夹位置

`~/Desktop/备份和系统文件/`

### 关键备份文件

| 文件 | 说明 | 大小 |
|------|------|:----:|
| `BRAIN_cocktail_backup_2026-06-25.duckdb` | 最新全量数据备份 | 62MB |
| `drink_master_v4.py` | 系统主程序（v4.0） | 22KB |
| `drink_master.py` | 系统主程序（v3.0） | 16KB |

### 恢复流程

```bash
# 如果数据库损坏，从备份恢复
cp ~/Desktop/备份和系统文件/BRAIN_cocktail_backup_2026-06-25.duckdb ~/Desktop/nini-duckdb-mcp/nini.duckdb
```

---

## 📞 联系方式

- **Telegram**: [@Yyuzuz](https://t.me/Yyuzuz)
- **X / Twitter**: [@DommeByte](https://x.com/DommeByte)
- **Website**: [memebuddy.uk](https://memebuddy.uk)

---

## 🧠 已知局限

1. **L1 风味图谱** 需要先运行构建共现矩阵（首次使用自动构建，约30秒）
2. **L3 语义搜索** 的 `ingredients` 字段包含部分描述性文本，搜索结果可能含噪音
3. **在线库** 比 DuckDB 多 ~2,000 条（同步产生的重复），不影响搜索功能
4. L5 清洗后缺配料的条目不会完全为0，但会大幅减少

---

## 📋 快速参考卡片

```bash
# 风味分析
python3 drink_master.py l1 金酒

# 风格迁移
python3 drink_master_v4.py migrate 威士忌 tiki

# 语义搜索
python3 drink_master.py search "烟熏味的金酒不要柠檬"

# 库存创造
python3 drink_master_v4.py craft "朗姆:35ml,柠檬:半个"

# 数据清洗
python3 drink_master_v4.py l5-clean

# 查看风格
python3 drink_master_v4.py styles

# 查看词库
python3 drink_master.py l4-vocab

# 重建风味数据
python3 drink_master.py rebuild
```
