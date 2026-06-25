<p align="center">
  <img src="https://img.shields.io/badge/version-4.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/status-active-success?style=for-the-badge" alt="Status">
</p>

<h1 align="center">🥃 DRINK MASTER v4.0</h1>
<h3 align="center">AI 智能调酒大师 · AI-Powered Cocktail Master</h3>
<h4 align="center">风味探索 · 风格迁移 · 库存创造 &nbsp;|&nbsp; Flavor Graph · Style Alchemy · Inventory Craft</h4>

<p align="center">
  <em>"不只是配方数据库，而是你的 AI 调酒顾问。"</em>
  <br>
  <sub>"More than a recipe database — your AI mixology consultant."</sub>
</p>

<p align="center">
  <a href="https://memebuddy.uk/"><img src="https://img.shields.io/badge/🌐_Website-memebuddy.uk-8A2BE2?style=for-the-badge" alt="Website"></a>
  <a href="https://x.com/DommeByte"><img src="https://img.shields.io/badge/X_(Twitter)-@DommeByte-000000?style=for-the-badge&logo=x" alt="X"></a>
  <a href="https://t.me/Yyuzuz"><img src="https://img.shields.io/badge/Telegram-@Yyuzuz-26A5E4?style=for-the-badge&logo=telegram" alt="Telegram"></a>
</p>

---

<p align="center">
  <a href="#-项目简介--about">📖 简介</a> &nbsp;·&nbsp;
  <a href="#-核心功能--features">✨ 功能</a> &nbsp;·&nbsp;
  <a href="#-系统架构--architecture">🏗️ 架构</a> &nbsp;·&nbsp;
  <a href="#-快速开始--quick-start">🚀 开始</a> &nbsp;·&nbsp;
  <a href="#-路线图--roadmap">🔮 路线图</a>
</p>

---

## 📖 项目简介 | About

**DRINK MASTER** 是一个基于大数据与风味科学的人工智能调酒系统。它不是一个简单的配方查询工具，而是一个拥有 **风味理解能力** 的智能调酒助手——能分析基酒的风味关联、将经典风格迁移到任意基酒、甚至根据你手头的库存实时创造全新配方。

**DRINK MASTER** is what happens when you cross a mad scientist's flavor lab with a master bartender's instinct — and then give it an AI brain. 🧠🍸

It doesn't just *look up* recipes. It **understands flavor** at a molecular level. Feed it a spirit, and it maps out its entire flavor universe — every ingredient it's ever touched, every combination humanity has dared to try. Tell it you're in a *Tiki mood but only have Gin*, and it rewires the DNA of a Mai Tai into something entirely new. Staring at a near-empty fridge? Just type what you've got — that half lemon, that dusty bottle of rum, that questionable honey — and watch it conjure a legit cocktail out of thin air.

This is not a recipe book. This is a **cocktail oracle** powered by co-occurrence matrices, Jaccard similarity, and a massive database of real-world drink recipes. It's part data scientist, part bartender, and 100% ready to make you look like a genius at your next party.

> 🧠 **内核 / Core**：风味共现矩阵 + 向量相似度 + 风格特征引擎  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Flavor Co-occurrence Matrix + Vector Similarity + Style Signature Engine  
> 📊 **数据 / Data**：海量鸡尾酒配方数据库 · Massive Cocktail Recipe Database  
> 🎨 **风格 / Styles**：提基 / 禁酒令 / 日式 / 经典 / 现代 / 酸酒家族  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tiki / Prohibition / Japanese / Classic / Modern / Sour Family

---

## ✨ 核心功能 | Features

### 🔬 L1 — 风味关联图谱 · Flavor Graph

通过 **Jaccard 共现矩阵** 构建风味相似度网络，发现任意基酒的「灵魂伴侣」原料。

Builds a flavor similarity network via **Jaccard co-occurrence matrix** to discover the "soulmates" of any base spirit.

```
python drink_master_v3.py l1 gin
```

输出 / Output：
- 🏆 **灵魂伴侣 / Soulmates**：按向量相似度排序的最佳搭配 · Best pairings ranked by vector similarity
- 🎨 **风味画像 / Flavor Profile**：基酒在各风味维度上的得分雷达图 · Radar chart across flavor dimensions
- 🆕 **风味盲区 / Blind Spots**：高频但从未搭配的创新机会 · High-frequency yet unexplored combinations

---

### 🎨 L2 — 风格迁移炼金术 · Style Alchemy

将 6 大经典调酒风格的「风味 DNA」迁移到任意基酒上。

Transplants the "flavor DNA" of 6 classic cocktail styles onto any base spirit.

| 风格 Style | 特征 Characteristics | 代表 Examples |
|:-----------|:---------------------|:--------------|
| 🏝️ **提基风 · Tiki** | 复杂酸甜 × 热带香料 · Complex sweet-sour × Tropical spice | Mai Tai, Zombie |
| 🚫 **禁酒令风 · Prohibition** | 重甜重酸掩盖劣酒 · Heavy sweet & sour to mask rough spirits | Bee's Knees, Last Word |
| 🇯🇵 **日式 · Japanese** | 极简精准，突显本质 · Minimalist precision, spirit-forward | Hard Shake technique |
| 📕 **经典风 · Classic** | 时间验证的结构 · Time-tested structures | Old Fashioned, Martini |
| 🧪 **现代风 · Modern** | 创意混搭 × 非常规 · Creative fusion × Unconventional | Fat-Washed, Clarified |
| 🍋 **酸酒家族 · Sour Family** | 基酒+柑橘+甜=万能 · Spirit + Citrus + Sweet = Universal | Daiquiri, Whiskey Sour |

```python
python drink_master_v4.py migrate 金酒 tiki
# → 🏝️ Tiki-style Gin: Gin + Lime + Pineapple + Orgeat + Orange Curacao
```

---

### 🧪 L3 — 库存感知创造 · Inventory Craft

**你冰箱里有什么，就能调什么。** 输入原料清单，AI 自动识别基酒、分类配料、生成最优配方。

**What's in your fridge is what you drink.** Input your inventory, and the AI auto-identifies spirits, classifies ingredients, and generates the optimal recipe.

```python
python drink_master_v4.py craft 朗姆酒:35ml,柠檬:半个,蜂蜜:15ml
# → 🍸 Sour variant: Intelligently matches sweet-sour ratio, outputs complete recipe
```

---

### 🔍 L4 — 语义搜索 · Semantic Search

用自然语言描述你想喝的味道。Describe your desired drink in natural language.

```python
python drink_master_v3.py search 烟熏味的金酒不要柠檬
# → Auto-parsed: Spirit=Gin | Flavor=Smoky | Exclude=Lemon
# → Returns Top 10 matching recipes
```

---

### 📚 L5 — 风味词库 & 数据清洗 · Flavor Lexicon & Data Cleaning

- **自动提取 / Auto-extract** 数据库中所有高频风味原料，构建 15 类风味词库 · Builds a 15-category flavor lexicon from high-frequency ingredients
- **智能清洗 / Smart Clean** 自动检测并修复脏数据、补全缺失配料 · Detects and repairs dirty data, fills missing ingredients

---

## 🏗️ 系统架构 | Architecture

```
                    ┌──────────────────────────┐
                    │   用户输入 / User Input    │
                    │        (CLI / API)        │
                    └────────────┬─────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │  L1 风味图谱  │     │ L2 风格迁移  │     │ L3 库存创造  │
    │  Flavor Graph │     │Style Alchemy │     │Inventory Craft│
    │  共现矩阵     │     │ 风格特征引擎  │     │ 原料解析器    │
    │  Jaccard Sim  │     │ Profile Match│     │ Recipe Gen    │
    └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
           │                    │                     │
           └────────────────────┼─────────────────────┘
                                ▼
                    ┌──────────────────────────┐
                    │   DuckDB 配方数据库       │
                    │   Recipe Database         │
                    │   (cocktail_recipes)      │
                    └────────────┬─────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │ L4 语义搜索  │     │ L5 数据清洗  │     │  风味词库    │
    │Semantic Search│    │ Data Cleanup │     │Flavor Lexicon│
    │ NLP意图解析  │     │ 脏数据检测   │     │ 15类 × N词   │
    └──────────────┘     └──────────────┘     └──────────────┘
```

---

## 🚀 快速开始 | Quick Start

### 环境要求 · Requirements

- **Python** ≥ 3.8
- **DuckDB** MCP Server running at `http://127.0.0.1:8766`
- Cocktail recipe database (`cocktail_recipes` table)

### 安装 · Installation

```bash
git clone https://github.com/umimemebuddy/DRINK_MASTER.git
cd DRINK_MASTER
pip install -r requirements.txt  # if extra dependencies exist
```

### 基础用法 · Basic Usage

```bash
# 查看所有可用风格 / List all available styles
python drink_master_v4.py styles

# 风味图谱分析 / Flavor graph analysis
python drink_master_v3.py l1 威士忌

# 风格迁移创造 / Style migration creation
python drink_master_v4.py migrate 龙舌兰 japanese

# 库存感知创造 / Inventory-aware creation
python drink_master_v4.py craft "朗姆酒:45ml, 青柠:1个, 薄荷:5片, 糖浆:15ml"

# 自然语言搜索 / Natural language search
python drink_master_v3.py search 清爽的夏日金酒饮品

# 数据清洗 / Data cleanup
python drink_master_v4.py l5-clean
```

---

## 📂 项目结构 | Project Structure

```
DRINK_MASTER_v4.0/
├── drink_master_v3.py    # 核心引擎 / Core: L1图谱 + L4搜索 + 词库
├── drink_master_v4.py    # 升级模块 / Upgrade: L2风格 + L3库存 + L5清洗
├── README.md             # 项目介绍 / You're reading it!
├── LICENSE               # MIT 开源协议 / MIT License
└── .gitignore
```

---

## 🎯 设计哲学 | Design Philosophy

| 原则 / Principle | 说明 / Description |
|:-----------------|:-------------------|
| **数据驱动 · Data-Driven** | 一切风味关联都从真实配方数据中学习，不依赖主观判断 · All flavor associations learned from real recipe data, not subjective opinions |
| **风格可迁移 · Style Transferable** | 调酒风格不是死板的配方列表，而是可量化的风味特征向量 · Cocktail styles are not rigid lists but quantifiable flavor vectors |
| **库存优先 · Inventory-First** | 不要求你买特殊原料——有什么调什么 · No need to buy special ingredients — use what you have |
| **中英双语 · Bilingual** | 支持中文自然语言查询和中文原料识别 · Supports Chinese natural language queries & ingredient recognition |

---

## 🔮 路线图 | Roadmap

- [x] L1 风味关联图谱 · Flavor Graph (Co-occurrence Matrix + Vector Similarity)
- [x] L2 风格迁移炼金术 · Style Alchemy (6 Classic Styles)
- [x] L3 库存感知创造 · Inventory Craft (Smart Ingredient Parser)
- [x] L4 自然语言语义搜索 · Semantic Search (NLP Intent Parsing)
- [x] L5 风味词库 + 数据清洗 · Flavor Lexicon + Data Cleanup
- [ ] 🖥️ Web UI 界面 · Web Interface
- [ ] 📱 移动端适配 · Mobile Adaptation
- [ ] 🧠 LLM 增强配方生成 · LLM-Enhanced Recipe Generation
- [ ] 📸 拍照识别库存原料 · Photo Ingredient Recognition
- [ ] 🌐 社区配方共享 · Community Recipe Sharing

---

## 🌐 联系作者 | Connect

| 平台 / Platform | 链接 / Link |
|:----------------|:------------|
| 🌍 **Website** | [memebuddy.uk](https://memebuddy.uk/) |
| 𝕏 **X (Twitter)** | [@DommeByte](https://x.com/DommeByte) |
| 📬 **Telegram** | [@Yyuzuz](https://t.me/Yyuzuz) |

---

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！无论是新功能、bug 修复还是文档改进。

Issues and Pull Requests are welcome! Whether it's new features, bug fixes, or documentation improvements.

---

## 📄 开源协议 | License

本项目基于 [MIT License](LICENSE) 开源。This project is open-sourced under the [MIT License](LICENSE).

---

<p align="center">
  <sub>Made with 🍸 and ❤️ by <a href="https://memebuddy.uk/">Drink Masters</a></sub>
  <br>
  <sub>Cheers! 🥂 干杯!</sub>
</p>
