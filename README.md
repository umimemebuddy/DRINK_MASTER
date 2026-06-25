<p align="center">
  <img src="https://img.shields.io/badge/version-4.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/status-active-success?style=for-the-badge" alt="Status">
</p>

<h1 align="center">🥃 DRINK MASTER v4.0</h1>
<h3 align="center">AI 驱动的智能调酒大师 — 风味探索 · 风格迁移 · 库存创造</h3>

<p align="center">
  <em>"不只是配方数据库，而是你的 AI 调酒顾问。"</em>
</p>

---

## 📖 项目简介

**DRINK MASTER** 是一个基于大数据与风味科学的人工智能调酒系统。它不是一个简单的配方查询工具，而是一个拥有 **风味理解能力** 的智能调酒助手——能分析基酒的风味关联、将经典风格迁移到任意基酒、甚至根据你手头的库存实时创造全新配方。

> 🧠 内核：风味共现矩阵 + 向量相似度 + 风格特征引擎  
> 📊 数据：海量鸡尾酒配方数据库  
> 🎨 风格：提基风 / 禁酒令风 / 日式 / 经典 / 现代 / 酸酒家族

---

## ✨ 核心功能

### 🔬 L1 — 风味关联图谱 (Flavor Graph)
通过 **Jaccard 共现矩阵** 构建风味相似度网络，发现任意基酒的「灵魂伴侣」原料。

```
python drink_master_v3.py l1 gin
```

输出：
- 🏆 灵魂伴侣：按向量相似度排序的最佳搭配
- 🎨 风味画像：基酒在各类风味维度上的得分雷达图
- 🆕 风味盲区：高频但从未搭配的创新机会

### 🎨 L2 — 风格迁移炼金术 (Style Alchemy)
将 6 大经典调酒风格的「风味 DNA」迁移到任意基酒上。

| 风格 | 特征 | 代表 |
|------|------|------|
| 🏝️ **提基风** | 复杂酸甜 × 热带香料 | Mai Tai, Zombie |
| 🚫 **禁酒令风** | 重甜重酸掩盖劣酒 | Bee's Knees, Last Word |
| 🇯🇵 **日式** | 极简精准，突显本质 | Hard Shake 技法 |
| 📕 **经典风** | 时间验证的结构 | Old Fashioned, Martini |
| 🧪 **现代风** | 创意混搭 × 非常规 | Fat-Washed, Clarified |
| 🍋 **酸酒家族** | 基酒+柑橘+甜=万能 | Daiquiri, Whiskey Sour |

```python
python drink_master_v4.py migrate 金酒 tiki
# → 🏝️ 提基风金酒：金酒 + 青柠汁 + 菠萝汁 + orgeat + 橙皮利口酒
```

### 🧪 L3 — 库存感知创造 (Inventory Craft)
**你冰箱里有什么，就能调什么。** 输入原料清单，AI 自动识别基酒、分类配料、生成最优配方。

```python
python drink_master_v4.py craft 朗姆酒:35ml,柠檬:半个,蜂蜜:15ml
# → 🍸 Sour 变体：智能匹配酸甜比，输出完整配方
```

### 🔍 L4 — 语义搜索 (Semantic Search)
用自然语言描述你想喝的味道：

```python
python drink_master_v3.py search 烟熏味的金酒不要柠檬
# → 自动解析：基酒=金酒 | 风味=烟熏 | 排除=柠檬
# → 返回 Top 10 匹配配方
```

### 📚 L5 — 风味词库 & 数据清洗
- **自动提取** 数据库中所有高频风味原料，构建 15 类风味词库
- **智能清洗** 自动检测并修复脏数据、补全缺失配料

---

## 🏗️ 系统架构

```
                    ┌──────────────────────┐
                    │   用户输入 / CLI       │
                    └──────────┬───────────┘
                               │
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │  L1 风味图谱  │   │ L2 风格迁移  │   │ L3 库存创造  │
    │  共现矩阵     │   │ 风格特征引擎  │   │ 原料解析器    │
    │  Jaccard相似度│   │ Profile匹配  │   │ 配方生成器    │
    └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
           │                  │                   │
           └──────────────────┼───────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  DuckDB 配方数据库 │
                    │  (cocktail_recipes)│
                    └──────────────────┘
                              │
           ┌──────────────────┼───────────────────┐
           ▼                  ▼                   ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ L4 语义搜索  │  │ L5 数据清洗  │  │ 风味词库     │
    │ NLP意图解析  │  │ 脏数据检测   │  │ 15类 × N词   │
    └──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🚀 快速开始

### 环境要求

- **Python** ≥ 3.8
- **DuckDB** MCP Server 运行在 `http://127.0.0.1:8766`
- 鸡尾酒配方数据库 (`cocktail_recipes` 表)

### 安装

```bash
git clone https://github.com/YOUR_USERNAME/DRINK_MASTER.git
cd DRINK_MASTER
pip install -r requirements.txt  # 如有额外依赖
```

### 基础用法

```bash
# 查看所有可用风格
python drink_master_v4.py styles

# 风味图谱分析
python drink_master_v3.py l1 威士忌

# 风格迁移创造
python drink_master_v4.py migrate 龙舌兰 japanese

# 库存感知创造
python drink_master_v4.py craft "朗姆酒:45ml, 青柠:1个, 薄荷:5片, 糖浆:15ml"

# 自然语言搜索
python drink_master_v3.py search 清爽的夏日金酒饮品

# 数据清洗
python drink_master_v4.py l5-clean
```

---

## 📂 项目结构

```
DRINK_MASTER_v4.0/
├── drink_master_v3.py    # 核心引擎：L1风味图谱 + L4语义搜索 + L5风味词库
├── drink_master_v4.py    # 升级模块：L2风格迁移 + L3库存创造 + L5数据清洗
├── README.md             # 项目介绍（你在这里！）
└── LICENSE               # MIT 开源协议
```

---

## 🎯 设计哲学

| 原则 | 说明 |
|------|------|
| **数据驱动** | 一切风味关联都从真实配方数据中学习，不依赖主观判断 |
| **风格可迁移** | 调酒风格不是死板的配方列表，而是可量化的风味特征向量 |
| **库存优先** | 不要求你买特殊原料——有什么调什么 |
| **中英双语** | 支持中文自然语言查询和中文原料识别 |

---

## 🔮 路线图

- [x] L1 风味关联图谱（共现矩阵 + 向量相似度）
- [x] L2 风格迁移炼金术（6 大经典风格）
- [x] L3 库存感知创造（智能原料解析）
- [x] L4 自然语言语义搜索
- [x] L5 风味词库 + 数据清洗
- [ ] 🖥️ Web UI 界面
- [ ] 📱 移动端适配
- [ ] 🧠 LLM 增强配方生成
- [ ] 📸 拍照识别库存原料
- [ ] 🌐 社区配方共享

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！无论是新功能、bug 修复还是文档改进。

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<p align="center">
  <sub>Made with 🍸 and ❤️ by Drink Masters</sub>
</p>
