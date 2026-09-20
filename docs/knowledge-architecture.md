# Visuals 知识体系架构规范

> 本文定义 Visuals 的知识分类、目录、跨学科关联与学习路线规则。它优先于临时的文件收纳习惯，是新增和重构知识内容时的统一依据。

## 1. 设计目标

Visuals 是个人技术知识体系的可视化载体。每个知识页面应同时具备：

1. **可定位**：知道它属于哪个稳定知识领域；
2. **可理解**：一个页面聚焦一个明确学习目标；
3. **可连接**：与前置、后续和跨学科知识建立关系；
4. **可学习**：目录支持检索，页面通过关联链接表达必要的前置与后续知识；
5. **可维护**：新增内容不会持续制造分类债务。

## 2. 顶层知识地图

```text
Visuals
├── 计算机科学基础（computer-foundations/）
│   ├── 算法、组成原理、操作系统、网络、编译
│   ├── 密码学与安全基础、拓扑学
├── 编程与程序（programming-and-programs/）
│   ├── 编程语言与运行时
│   ├── Go 语言与运行时（golang/）
│   └── Go 工程实践（go/）
├── 数据与智能（首页视觉分组）
│   ├── 数据库系统（database-system/）
│   ├── 大数据系统（bigdata-system/）
│   └── 人工智能（artificial-intelligence/）
├── 系统工程（system-engineering/）
│   ├── 软件工程（software-engineering/）
│   ├── 分布式系统（distributed-system/）
│   ├── 云服务架构（cloud-architecture/）
│   └── 高性能、高并发、高可用（high-performance-concurrency-availability/）
└── 学习与考试（learning-and-exams/）
    └── 考研（kaoyan/）
```

首页标题是视觉分组，不强制新增物理目录；各知识主题仍保留在其稳定的 canonical 路径中。

## 3. 唯一主归属

### 3.1 当前过渡目录

目录重构期间，物理文件可能暂时保留在原路径，而由新的主题索引提供 canonical home。过渡入口必须明确说明知识归属，并在迁移完成后删除旧入口与过渡规则。

当前 Go 内容统一位于 `programming-and-programs/go/` 与 `programming-and-programs/golang/`：前者覆盖框架、服务治理和工程实践，后者覆盖语言与运行时。`programming-and-programs/index.html` 通过“Go 工程实践”入口连接前者；不要为多学科访问复制叶子页面，其他学科仅建立链接到 canonical 页面。

每个叶子知识页必须有一个 **canonical home**。当一个主题可从多个领域理解时，以“该页最主要回答的问题”决定其主归属；其他领域通过相关知识卡片链接到该页面，而不是复制内容。

| 主要问题 | 主归属 |
| --- | --- |
| 数据结构、协议、OS、硬件、基础安全原理 | `computer-foundations/` |
| 编程语言、运行时、内存、并发语义与语言工程实践 | `programming-and-programs/` |
| 数据存储、查询、缓存、索引、检索、数据扩展 | `database-system/` |
| 数仓、湖仓、批/流处理、分析查询、数据治理 | `bigdata-system/` |
| 软件架构、设计模式、接口集成、身份认证、业务系统 | `system-engineering/software-engineering/` |
| 一致性、共识、协调、消息、RPC、分布式事务、微服务治理 | `system-engineering/distributed-system/` |
| 云网络、计算资源、容器编排、云产品、上云迁移 | `system-engineering/cloud-architecture/` |
| 吞吐、延迟、容量、并发模型、资源池、性能调优 | `system-engineering/high-performance-concurrency-availability/high-concurrency/` |
| SLO、故障、容灾、恢复、过载保护、流量保护 | `system-engineering/high-performance-concurrency-availability/high-availability/` |
| 业务状态机、资金链路、规则、领域模型、行业方案 | `system-engineering/software-engineering/business-design/` |
| LLM、RAG、Agent、推理服务、AI 应用工程 | `artificial-intelligence/` |
| 考试大纲、刷题、复习资料、学习计划 | `learning-and-exams/kaoyan/` |

### 示例

- 通用限流算法的主归属是 `high-availability/traffic-protection/`；高并发、分布式、云网关和 AI 服务仅建立不同语境下的关联入口。
- 异地多活的主归属是高可用；云架构页面解释云上实现条件和基础设施选型。
- Redis 的数据结构和持久化属于数据库系统；业务系统中只解释其在订单、秒杀等场景中的使用。

## 4. 目录、页面、路线与关联的职责

| 机制 | 回答的问题 | 规则 |
| --- | --- | --- |
| 目录 | 知识属于哪里？ | 以对象、问题域或机制命名，保持稳定 |
| 叶子页 | 一个知识点如何理解？ | 一页一个清晰学习目标 |
| 跨学科卡片 | 它与什么相关？ | 链接 canonical 页面，不复制主体内容 |

同一 URL 不得在同一索引页中以不同标题重复登记。多个互补页面可以同属一个目录，但卡片需要清晰区分：总览、原理、机制、实践或案例。

## 5. 目录与文件命名

- 新目录与新文件统一使用小写 `kebab-case`。
- 展示标题可以使用中文、缩写、英文和 Emoji；路径不使用大小写混排、下划线或中文文件名。
- 常规目录深度最多三级：`领域 / 稳定分类 / 产品或机制`。
- 当一个目录中叶子页达到约 8–12 篇，并且可以按稳定子主题划分时，才创建下一层目录。
- `overview`、`guide`、`practice`、`reference` 是入口或内容类型，不是“杂项”目录；每个页面仍应有明确主题。

## 6. 页面类型

新知识页和索引卡片逐步采用以下类型之一：

- `foundation`：建立基本概念和全局地图；
- `principle`：解释本质、理论或设计取舍；
- `mechanism`：拆解内部流程、状态和实现机制；
- `implementation`：展示代码、配置或落地步骤；
- `practice`：面向工程场景的方案与操作；
- `case-study`：围绕一个业务或故障案例复盘；
- `reference`：速查、公式、命令或对照资料。

## 7. 索引与路由约定

- 学科 `index.html` 通过 `data-topic-tree` 和 `topic-group[data-path]` 声明目录树；过渡期内 `data-path` 可以表达比物理目录更细的语义层级，但同一学科中每个路径只对应一个明确主题，物理迁移完成后应与真实路径收敛。
- 叶子页必须在其所在目录或某一祖先目录的 `index.html` 中有卡片入口。
- 仅在物理迁移尚未完成时，canonical 学科入口可声明 `data-canonical-prefix`；该入口或其下属知识地图必须为前缀下每个页面提供精确链接，不能只用前缀掩盖缺失入口。
- 索引页若加载 `assets/card-link-router.js`，`<html>` 必须声明正确的 `data-app-root`；非 `index.html` 的卡片会路由到 `container.html`，并携带来源索引，使容器中的“返回”能精确回到当前目录。
- 跨学科卡片使用 `(跨学科)` 分组，并明确它们是外部 canonical 页面。

## 8. 新增内容流程

1. 写下该页最主要要回答的问题；
2. 使用“唯一主归属”表确定 canonical home；
3. 创建小写 kebab-case 路径的叶子 HTML；
4. 在 canonical 索引登记一张清晰卡片；
5. 必要时，在相关学科新增跨学科引用卡片；
6. 必要时在相关知识页补充前置、后续或跨学科关联；
7. 运行校验：

```bash
bash check_html_link.sh
bash check_safe.sh
```

## 9. 学习关联

不维护独立的学习路线页。目录树负责“查找与定位”；知识页通过前置知识、后续阅读和跨学科关联表达“下一步学什么”。新增关联时应链接到 canonical 页面，避免复制同一主题或维护并行导航。
