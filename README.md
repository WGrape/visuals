# Visuals

一个以动态可视化为核心特色的 IT 在线学习平台，提供直观易懂、丰富多元的学习内容。

<img width="1528" height="1351" alt="Image" src="https://github.com/user-attachments/assets/f3842819-b00c-43c5-91ad-1338bc4a0a5a" />

## 项目简介

Visuals 致力于通过可视化的方式，让复杂的计算机科学概念变得简单易懂。从计算机组成原理到AI人工智能等这一系列基础理论到高级架构的全面知识体系，全部使用可视化的动态交互、以及图表网页的方式，帮助开发者深入理解技术原理。

## 知识体系

目录既是网站导航，也是知识分类。首页按知识主题展示卡片；目录层级以实际知识边界为准，不为视觉分组额外增加物理目录。

1. **计算机科学基础**：算法、组成原理、操作系统、网络、编译与密码学。
2. **编程与程序**：编程语言、运行时、Go / Python 与工程实践。
3. **数据库系统**：数据建模、存储、查询、缓存、检索与扩展。
4. **大数据系统**：数仓、湖仓、批流处理、查询引擎与数据平台。
5. **人工智能**：模型、生命周期、大语言模型、AI 工程与 AI 开发。
6. **系统工程**：软件工程、分布式系统、云服务架构，以及高性能、高并发、高可用。

完整的分类原则、命名规则和新增内容流程见 [知识架构治理](docs/knowledge-architecture.md)；正在执行的目录调整及迁移清单见 [知识迁移蓝图](docs/knowledge-migration-blueprint.md)。

## 项目结构

```
visuals/
├── index.html                    # 全站首页：一级目录标题、二级目录卡片
├── computer-foundations/         # 计算机科学基础
│   ├── computer-algorithm/
│   ├── computer-network/
│   ├── computer-operating-system/
├── programming-and-programs/     # 编程与程序
│   ├── golang/                   # Go 语言与运行时
│   └── go/                       # Go 工程实践
├── database-system/              # 数据库系统
├── bigdata-system/               # 大数据系统
├── artificial-intelligence/      # 人工智能
├── system-engineering/           # 系统工程
│   ├── software-engineering/
│   ├── distributed-system/
│   ├── cloud-architecture/
│   └── high-performance-concurrency-availability/
├── learning-and-exams/           # 学习与考试
│   └── kaoyan/
├── assets/                       # 公共样式、目录树和路由脚本
├── docs/                         # 知识体系治理与迁移文档
├── check_html_link.sh            # HTML 链接检查脚本
└── check_safe.sh                 # 本地链接与敏感信息检查脚本
```

## 本地运行

直接用浏览器打开 `index.html` 即可，或者启动本地 HTTP 服务器：

```bash
# Python 3
python3 -m http.server 8000

# 然后访问 http://localhost:8000
```

## 开发工具

### check_html_link.sh

用于检查每个 HTML 文件是否被正确链接到对应的上级 `index.html` 文件中，防止新增页面遗漏添加链接。

**使用方式：**

```bash
bash ./check_html_link.sh

# 或者添加执行权限（首次使用）后直接执行
chmod +x check_html_link.sh
./check_html_link.sh
```

**功能说明：**

- 自动遍历项目中所有 HTML 文件
- 检查文件是否在对应的上级 `index.html` 中有链接引用
- 支持多级目录结构，并沿祖先目录查找可发现该页面的 `index.html`
- 用颜色标记检查结果（绿色=已链接，红色=未链接，黄色=跳过）
- 显示统计摘要：总计、已链接、未链接数量

**检查规则：**

- `computer-foundations/computer-algorithm/data-structures/trees/binary_tree_traversal.html` → 由其祖先目录中的索引发现
- `system-engineering/high-performance-concurrency-availability/high-concurrency/kafka/kafka-partition-explained.html` → 由对应领域索引发现

## 贡献指南

1. 新增内容时，请在对应板块的目录下创建 HTML 文件
2. 确保在上级 `index.html` 中添加新页面的链接卡片
3. 使用 `./check_html_link.sh` 检查链接是否完整
4. 保持页面风格与现有设计一致

## License

© 2026 Visuals
