# Visuals

一个以动态可视化为核心特色的 IT 在线学习平台，提供直观易懂、丰富多元的学习内容。

<img width="1528" height="1351" alt="Visuals 知识地图" src="https://github.com/user-attachments/assets/f3842819-b00c-43c5-91ad-1338bc4a0a5a" />

## 项目简介

Visuals 用交互式页面与图解讲解人工智能、系统工程、数据库系统、计算机科学、编程与程序。

| 指标 | 数量 |
| --- | --- |
| 一级知识域 | 5 |
| 二级学科 / 三级章节 / 四级专题 | 24 / 150 / 395（另有 67 个五级、15 个六级目录） |
| 课程 | 740 篇，最深 6 级 |
| 索引页 | 35 |

一句话概括约定：**目录即导航，物理目录的层级就是知识的层级。**

目录：[知识目录](#知识目录) · [内容组织规则](#内容组织规则) · [技术实现](#技术实现) · [本地运行](#本地运行) · [新增内容与验证](#新增内容与验证)

## 知识目录

### 1. 目录层级就是知识层级

目录同时是网站导航与知识分类：**物理目录的层级就是知识结构的层级**，不允许把分类压进文件名，也不允许用卡片分组假装出目录。

| 层级 | 含义 | 强制约定 | 例子 |
| --- | --- | --- | --- |
| **一级** | **知识的根结构**（知识域） | 固定 5 个，见下方映射表 | `artificial-intelligence/`（人工智能） |
| **二级** | 该知识域下的**二级分类**（学科） | **必须有 `index.html`**；下面只能放三级目录，**不能直接放课程** | `model-llm/`（大模型） |
| **三级** | 分类下的**章节** | **必须以两位序号开头**（`00-`、`01-`、`02-`…）；下面必须是四级专题目录，**不能直接放课程** | `model-llm/02-principle/`（原理） |
| **四级** | 章节下的**专题** | 真正承载课程（`.html` / `.md`）的第一层 | `02-principle/02-decoding/`（解码与采样） |
| **五级+** | 专题继续细分 | 需要就继续加，不必强行压平 | `nosql/03-column-family/hbase/01-data-model/` |

**从二级分类目录开始，往下的所有子目录都属于这个分类自己的子结构。** 二级目录有两重身份：它既是该分类的导航入口（`index.html`），也是它下面「三级章节 → 四级专题 → 五级细分」这棵知识树的根。要知道某个分类有哪些内容，查这个二级目录的子树即可。

### 2. 为什么至少四级

`一级（知识域） → 二级（学科分类） → 三级（章节） → 四级（专题）` 这四层是**下限**而不是目标。

很多知识分类只给三层根本分不开：学科下面要先切出章节（如 MySQL 的架构 / 索引 / 事务 / 锁），章节下面还要再切成专题（索引下面还有 B+ 树 / 覆盖索引 / 前缀索引）。三层装不下，就会退化成"一个目录塞几十篇平铺文章"，既没法导航也看不出知识脉络。

所以规则是：**至少四级；复杂主题继续加第五、第六级**。当前仓库最深已到 6 级。

### 3. 一级知识结构 → 二级分类

| 一级目录（知识根结构） | 二级分类 |
| --- | --- |
| `artificial-intelligence/`（人工智能） | `ai-engineering`、`model-basic`、`model-lifecycle`、`model-llm`、`speech-and-audio` |
| `system-engineering/`（系统工程） | `cloud-architecture`、`distributed-system`、`high-performance-concurrency-availability`、`software-engineering` |
| `database-system/`（数据库系统） | `bigdata-system`、`localcache`、`nosql`、`relational`、`vectordb` |
| `cst/`（计算机科学） | `computer-algorithm`、`computer-composition`、`computer-history`、`computer-mathematics`、`computer-network`、`computer-operating-system` |
| `programming-and-programs/`（编程与程序） | `build-program`、`golang`、`python`、`runtime-mechanisms` |

一级目录固定为上述 5 个，顺序与首页知识地图一致（人工智能 → 系统工程 → 数据库系统 → 计算机科学基础 → 编程与程序）；`assets/`、`docs/` 是资源与文档目录，不参与知识层级。

### 4. 目录结构示例

```text
visuals/
├── index.html                                  # 全站入口
├── artificial-intelligence/                    # 一级：知识根结构（人工智能）
│   └── model-llm/                              # 二级：该根下的分类，必须有 index.html
│       ├── index.html                          # 二级分类的导航入口
│       └── 02-principle/                       # 三级：带序号的章节
│           ├── 01-scaling-laws/                # 四级：专题
│           │   └── scaling-laws.html           # 课程只落到四级或更深
│           └── 02-decoding/
│               └── sampling-decoding.html
├── cst/                                        # 一级：计算机科学
│   └── computer-algorithm/                     # 二级：学科分类
│       ├── index.html
│       └── 08-heaps/                           # 三级：章节
│           ├── 00-overview/                    # 四级：章节概览专题
│           │   └── heaps.html
│           └── 02-max-heaps/                   # 四级：专题课程
│               └── max-heap.html
├── database-system/                            # 一级（示例五级细分）
│   └── nosql/                                  # 二级
│       └── 03-column-family/                   # 三级
│           └── hbase/                          # 四级
│               └── 01-data-model/              # 五级
├── programming-and-programs/
├── system-engineering/
├── assets/                                     # 公共样式、目录树和路由脚本
├── docs/                                       # 课程迁移路径等参考数据
├── check_knowledge_hierarchy.py               # 目录深度与编号
├── check_topic_tree.py                        # 目录树和卡片所属目录
├── check_html_link.sh                         # 页面是否被索引引用
└── check_safe.sh                              # 本地坏链与敏感内容
```

## 内容组织规则

**目录**

- **新增内容时先定位再落地**：先确定属于 5 个一级知识根结构中的哪一个，再确定该根下的二级分类，然后在学科里选三级编号章节，最后落到四级或更深的专题目录。**不要新建一级目录**，也不要为了放一篇课程而在二级目录里新开一个与现有学科平行的目录。
- 每个二级学科都必须有 `index.html` 和至少一个三级章节；**每个三级章节（包括尚无课程的占位章节）都必须带序号并包含至少一个四级专题目录**。课程 HTML、Markdown 不直接存放在二级或三级目录；概览课程可以放在 `00-overview/`。三级 `index.html` 仅作为有需要的导航入口，不代替四级知识内容。
- 四级目录要表达真实的知识边界，例如基础概念、检索策略、评估与优化；同一主题较复杂时继续细分。**不能用与上级同义的目录凑满四层**；当课程标题已经有独立章节（如数学的行列式、矩阵）时，继续设置第五级专题，不把章节只留在文件名里。单篇课程也可以构成真实专题，不按文章数量强行合并。暂时无课程的专题用 `.gitkeep` 保留实体目录，不为凑层级新增虚构课程页面。

**课程归属**

- 每篇课程只有一个主要归属：通用原理放在概念专题，具体产品实现放在产品专题，跨主题的比较归共同上位专题；其他学习路径通过正文或说明性链接关联，不复制课程、也不把跨目录卡片塞入错误的 `data-path`。独立的历史与数学知识不放进"其他"兜底学科。
- 空占位可以保留在文件系统中用于规划，但不添加没有课程卡片的 `topic-group`，不让它在正式目录树里显示为可学习专题；完全没有课程的学科入口应明确标注"建设中"。

**索引与链接**

- 学科页的 `data-path` 必须与真实目录一致；一个分组的课程卡片应位于它声明的目录中。含 `assets/card-link-router.js` 的索引应设置与自身目录深度一致的 `<html data-app-root="…">`，并为新课程添加可见的索引卡片。
- 移动文章时同时修正卡片、文章互链、资源路径、返回链接和跨学科链接。静态站点不会自动转发旧 URL；目录迁移后原直达书签可能失效。2026-09-30 的课程与索引旧→新路径见 [`docs/knowledge-relocations.json`](docs/knowledge-relocations.json)，用于更新外部引用，**不是**站点重定向规则。

## 技术实现

纯静态站点，无构建、无依赖安装。课程页面自包含（内联样式与 SVG 图解），索引页复用 `assets/` 下的公共脚本：

| 文件 | 作用 |
| --- | --- |
| `common.css` | 索引页与卡片的基础样式 |
| `topic-tree.js` / `topic-tree.css` | 按 `data-path` 自动推导并渲染左侧知识目录树 |
| `card-link-router.js` | 课程卡片路由；用 `<html data-app-root="…">` 声明相对深度 |
| `binary-rain.js` | 首页 canvas 背景动效 |
| `mathjax/` | 数学公式渲染（当前无页面引用，保留备用） |
| `container.html` | 发布到子路径（如 `/visuals/`）时承载课程页面的外壳 |

## 本地运行

课程页面自包含（内联样式与 SVG 图解），**直接打开 `index.html` 即可完整浏览**——站内脚本不依赖 `fetch`，也没有必须经 HTTP 才能加载的资源。

如需以服务方式访问（例如配合 `container.html` 的子路径发布），在仓库根目录运行：

```bash
python3 -m http.server 8000
```

浏览器访问 <http://localhost:8000/>。发布到 `/visuals/` 路径时，普通课程卡片会通过 `container.html` 打开。

## 新增内容与验证

1. 按层级定位：一级知识根结构 → 二级分类（学科，确认有 `index.html`）→ 三级编号章节 → 四级或更深的专题目录。课程只落在四级及更深目录。
2. 添加课程与相关索引卡片，校验 `data-path`、相对路径和 `data-app-root`。
3. 在仓库根目录运行：

```bash
python3 -B check_knowledge_hierarchy.py
python3 -B check_topic_tree.py
bash check_html_link.sh
bash check_safe.sh
```

| 脚本 | 检查什么 | 什么情况会失败 |
| --- | --- | --- |
| `check_knowledge_hierarchy.py` | 目录深度、三级编号、二级 `index.html`、课程是否越级存放 | **结构错误**；占位目录只提醒不失败 |
| `check_topic_tree.py` | `data-path` 与真实目录、卡片所属目录、断链、重复入口 | 目录树与内容对不上 |
| `check_html_link.sh` | 每个页面是否被可达索引以卡片引用 | 存在未链接页面 |
| `check_safe.sh` | HTML 内部坏链、混入的非 HTML 文件、疑似密钥 | 坏链或敏感信息 |

检查器不会扫描 `.claude`、`.git` 等工具目录。当前基线：结构错误 0、目录树问题 0、未链接 0（42 个占位提醒属正常规划）。

## License

© 2026 Visuals
