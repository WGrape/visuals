# Visuals

一个以动态可视化为核心特色的 IT 在线学习平台，提供直观易懂、丰富多元的学习内容。

<img width="1528" height="1351" alt="Visuals 知识地图" src="https://github.com/user-attachments/assets/f3842819-b00c-43c5-91ad-1338bc4a0a5a" />

## 项目简介

Visuals 通过交互页面与可视化内容讲解计算机科学、编程、数据库、人工智能、系统工程和考试知识。

## 知识目录

目录同时是网站导航与知识分类。知识内容至少采用四级物理目录；复杂主题可以继续增加第五、第六级，不必强行压平：

```text
visuals/
├── index.html                                  # 全站入口
├── cst/                                        # 一级：计算机科学
│   └── computer-algorithm/                     # 二级：学科，必须有 index.html
│       ├── index.html
│       └── 08-heaps/                           # 三级：带序号的章节
│           ├── 00-overview/                    # 四级：章节概览专题
│           │   └── heaps.html
│           └── 02-max-heaps/                   # 四级：专题课程
│               └── max-heap.html
├── artificial-intelligence/
├── database-system/                            # 包括 bigdata-system 与 localcache
├── learning-and-exams/
├── programming-and-programs/                   # 包括 golang、python 等
├── system-engineering/
├── assets/                                     # 公共样式、目录树和路由脚本
├── check_knowledge_hierarchy.py               # 实体目录深度与编号
├── check_topic_tree.py                        # 目录树和卡片所属目录
├── check_html_link.sh                         # 页面是否被索引引用
└── check_safe.sh                              # 本地坏链与敏感内容
```

- 每个二级学科都必须有 `index.html` 和至少一个三级章节；**每个三级章节（包括尚无课程的占位章节）都必须带序号并包含至少一个四级专题目录**。课程 HTML、Markdown 不直接存放在二级或三级目录；概览课程可以放在 `00-overview/`。三级 `index.html` 仅作为有需要的导航入口，不代替四级知识内容。
- 四级目录要表达真实的知识边界，例如基础概念、检索策略、评估与优化；同一主题较复杂时继续细分。**不能用与上级同义的目录凑满四层**；当课程标题已经有独立章节（如数学的行列式、矩阵）时，继续设置第五级专题，不把章节只留在文件名里。单篇课程也可以构成真实专题，不按文章数量强行合并。暂时无课程的专题用 `.gitkeep` 保留实体目录，不为凑层级新增虚构课程页面。
- 每篇课程只有一个主要归属：通用原理放在概念专题，具体产品实现放在产品专题，跨主题的比较归共同上位专题；其他学习路径通过正文或说明性链接关联，不复制课程、也不把跨目录卡片塞入错误的 `data-path`。独立的历史与数学知识不放进“其他”兜底学科。
- 空占位可以保留在文件系统中用于规划，但不添加没有课程卡片的 `topic-group`，不让它在正式目录树里显示为可学习专题；完全没有课程的学科入口应明确标注“建设中”。
- 学科页的 `data-path` 必须与真实目录一致；一个分组的课程卡片应位于它声明的目录中。含 `assets/card-link-router.js` 的索引应设置与自身目录深度一致的 `<html data-app-root="…">`，并为新课程添加可见的索引卡片。
- 移动文章时同时修正卡片、文章互链、资源路径、返回链接和跨学科链接。静态站点不会自动转发旧 URL；目录迁移后原直达书签可能失效。2026-09-30 的课程与索引旧→新路径见 [`docs/knowledge-relocations.json`](docs/knowledge-relocations.json)，用于更新外部引用，**不是**站点重定向规则。

## 本地运行

直接打开 `index.html`，或在仓库根目录运行：

```bash
python3 -m http.server 8000
```

浏览器访问 <http://localhost:8000/>。发布到 `/visuals/` 路径时，普通课程卡片会通过 `container.html` 打开。

## 新增内容与验证

1. 确认学科入口和三级编号章节，按实际知识分类选择四级或更深的专题目录。
2. 添加课程与相关索引卡片，校验 `data-path`、相对路径和 `data-app-root`。
3. 在仓库根目录运行：

```bash
python3 -B check_knowledge_hierarchy.py
python3 -B check_topic_tree.py
bash check_html_link.sh
bash check_safe.sh
```

第一项会提醒尚未填充的占位目录，只有结构错误会使其失败；其余检查分别验证目录树、链接可发现性和本地坏链。检查器不会扫描 `.claude`、`.git` 等工具目录。

## License

© 2026 Visuals
