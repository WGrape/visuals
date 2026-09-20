# Visuals 知识目录迁移蓝图

> 本文是目录重构的执行台账。每一批开始前确认范围，结束后更新状态、索引和校验结果。除非另有记录，所有移动均保留页面内容，使用 `git mv` 并同步更新链接。

## 当前工作区保护项

| 范围 | 当前状态 | 处理原则 |
| --- | --- | --- |
| `cloud-architecture/` | 已有目录迁移中的删除、新增路径与索引修改 | 先验证现有迁移；不还原、不覆盖 |
| `distributed-system/` | 已有目录迁移中的删除、新增路径与索引修改 | 先验证现有迁移；不还原、不覆盖 |

## 批次总览

| 批次 | 范围 | 状态 |
| --- | --- | --- |
| 1 | 治理文档、首页与 CST 学习入口 | 已完成 |
| 2 | 计算机网络按层次收敛 | 已完成 |
| 3 | Go：语言原理与后端工程拆分 | 已完成 |
| 4 | 数据库分类收敛和重复卡片清理 | 已完成 |
| 5 | 大数据目标目录和学习路线 | 已完成 |
| 6 | 云架构/分布式在途迁移验证与边界收敛 | 已完成 |
| 7 | 高并发/高可用 canonical 页面和跨学科入口 | 已完成 |
| 8 | AI、业务与行业系统收敛 | 已完成 |
| 9 | 学习路线和全仓审计 | 已完成（`check_safe.sh` 待运行） |

## 1. 导航与基础入口

| 当前 | 目标 | 动作 | 原因 |
| --- | --- | --- | --- |
| 根首页直接列出大量 CST 子学科，同时有 `cst/index.html` | 首页进入“计算机科学基础”，CST 页展开具体学科 | 调整导航层级 | 避免首页和 CST 平行重复目录 |
| 各学科目录 | 由目录树呈现分类与学习入口 | 不再维护独立学习路线页 | 单独路线页与目录树重复，且不能提升实际浏览效率 |
| 密码学只包含 Base64 页面 | 标示为安全基础建设中，明确 Base64 是编码 | 调整展示语义 | 避免形成错误概念 |

## 2. 计算机网络

目标：按协议层次组织，并将端到端流程、排障、安全作为独立问题域。

```text
computer-network/
├── application-layer/{dns,http,https,realtime-communication}/
├── transport-layer/{tcp,udp}/
├── network-layer/{ip,routing,icmp,nat}/
├── link-layer/{arp,ethernet}/
├── end-to-end-flow/
├── troubleshooting/
└── security/
```

| 当前 | 目标 | 动作 | 原因 |
| --- | --- | --- | --- |
| `ip/` 中含 ARP、ICMP 页面，另有 `ARP/`、`ICMP/` | `link-layer/arp/` 与 `network-layer/icmp/` | 合并索引入口、选择 canonical 页面 | 当前分类重复且大小写不一致 |
| `post/` | `application-layer/http/` | 合并 | POST 是 HTTP 请求语义，不是独立协议域 |
| `tcp-udp/` | `transport-layer/{tcp,udp}/` | 分拆 | 便于 TCP/UDP 页面持续扩展 |
| `web-flow/` | `end-to-end-flow/` | 改名 | 描述跨层请求流程 |
| `packet-capture/` | `troubleshooting/packet-capture/` | 归类 | 抓包是排障工具 |
| `attack/` | `security/` | 改名 | 更清晰的安全问题域 |

## 3. Go：语言与工程

| 当前 | 目标 | 动作 | 原因 |
| --- | --- | --- | --- |
| Go 内容同时包含 runtime、Gin、go-zero、部署、OTel | 统一放入顶层编程语言目录，并由 `go/` 与 `golang/` 区分工程实践和语言运行时 | 已完成 | Go 的工程实践依附于语言生态，避免重复维护独立后端工程入口 |
| Go 内存模型、调度器、GC、Goroutine | `programming-and-programs/golang/` | 已收敛 | 属于语言/运行时 |
| Gin、go-zero、项目目录、服务治理、模型、配置、部署、观测 | `programming-and-programs/go/` | 已收敛 | 属于 Go 语言生态的工程实践 |

目标：

```text
programming-and-programs/
├── golang/                              # Go 语言与运行时页面
└── go/                                  # 框架、项目结构、治理、数据、观测与交付页面
```

## 4. 数据库

| 当前 | 目标 | 动作 | 原因 |
| --- | --- | --- | --- |
| `relational/mysql/engines/database-normal-forms.html` | `relational/concepts/data-modeling/` | 移动 | 范式不是 MySQL 存储引擎 |
| PostgreSQL/MySQL 对比位于 `engines/` | `relational/concepts/comparison/` | 移动 | 属于关系型数据库选型 |
| `db_partition_vs_sharding.html` 位于 MySQL 查询 | `data-scaling/` | 移动 | 分区、分片、读写分离是扩展架构 |
| 同一 URL 多次出现在索引卡片 | 单一清晰卡片 | 清理重复登记 | 防止把一页误识为多个知识点 |

目标：

```text
database-system/
├── overview/
├── relational/
│   ├── concepts/{data-modeling,comparison}/
│   ├── mysql/{architecture,indexes,query,transaction,locks,memory,storage,replication,availability}/
│   └── sqlite/
├── cache-and-kv/redis/
├── search-and-retrieval/
└── data-scaling/{partitioning,sharding,read-write-splitting}/
```

## 5. 大数据

| 当前 | 目标 | 动作 | 原因 |
| --- | --- | --- | --- |
| 多张卡片指向 `overview/bigdata-concepts.html` 的不同锚点 | 保留总览页面，明确其为地图页 | 不拆页，只调整索引语义 | 当前内容尚未形成多个独立专题 |
| 缺少可扩展目录 | `data-warehouse/`、`data-lakehouse/`、`batch-computing/`、`stream-processing/`、`query-engines/`、`data-platform/` | 创建目录/入口 | 为 Hadoop、Spark、Flink、CDC、Iceberg 等后续内容预留稳定位置 |

## 6. 分布式、云原生、性能与可靠性

| 内容 | Canonical home | 其他主题的职责 |
| --- | --- | --- |
| 通用限流算法 | `high-availability/traffic-protection/` | 高并发、分布式、云网关、AI 服务按场景引用 |
| 异地多活 | 高可用 | 云架构解释云上实现条件 |
| API Gateway | 分布式微服务治理 | 云架构解释设施/部署职责 |
| Nginx、SLB | 云架构计算/网络 | 高并发和微服务解释使用场景 |
| Kafka/MQ | 分布式消息 | 大数据解释流数据管道用途 |

边界：

```text
high-concurrency/   性能与容量
high-availability/  可靠性与恢复
distributed-system/ 多节点协调与治理
cloud-architecture/ 云上基础设施
```

## 7. AI

| 当前 | 目标 | 动作 |
| --- | --- | --- |
| 展示名称“人工智能”，实际内容集中于 LLM/Agent/RAG/工程 | “大语言模型与 AI 工程” | 调整展示名称 |
| `vibe-coding/` | `ai-development/` | 已完成迁移 |
| Prompt、Context、Function Calling、推理 | `model-llm/` | 收敛 |
| RAG、Agent、MCP、Serving、Evaluation | `ai-engineering/` | 收敛 |
| Harness、Claude Code、OpenClaw、Vibe Coding | `ai-development/` | 收敛 |

传统机器学习、深度学习、视觉、强化学习未来放入独立 `foundations/`，不混入现有 LLM 工程树。

## 8. 业务与行业系统

| 当前 | 目标 | 动作 | 原因 |
| --- | --- | --- | --- |
| 订单、支付 | `business-systems/transaction/` | 移动 | 交易领域 |
| 优惠券、秒杀、广告 | `business-systems/marketing/` | 移动 | 营销领域 |
| 推荐、消息中心 | `business-systems/content/` | 移动 | 内容与触达领域 |
| IoT、MQTT、OTA | `industry-systems/iot-and-device/` | 移动 | 设备平台 |
| Flash | `industry-systems/game-and-media/` | 移动 | 游戏/多媒体技术 |
| Redis 热点数据 | 高并发缓存热点 | 已移动，并在业务系统保留跨学科引用 | 本质是缓存性能问题 |

## 9. 首页与物理目录收敛

首页标题用于视觉分组，不强制为每个标题新增物理目录。`数据与智能` 下的三个主题继续作为仓库一级目录，保持原有稳定路径。

```text
computer-foundations/              # 计算机科学基础
├── computer-algorithm/
├── computer-compiler-principles/
├── computer-composition/
├── computer-network/
├── computer-operating-system/
├── computer-cryptography/
├── computer-topology/
├── programming-and-programs/

database-system/                   # 数据与智能：首页卡片
bigdata-system/                    # 数据与智能：首页卡片
artificial-intelligence/           # 数据与智能：首页卡片

system-engineering/                # 系统工程
├── software-engineering/
├── distributed-system/
├── cloud-architecture/
└── high-performance-concurrency-availability/

learning-and-exams/                # 学习与考试
└── kaoyan/
```

不维护各学科的独立 `learning-path.html`。学习入口由学科索引的左侧目录树和各知识卡片承担：目录树负责定位与分类，卡片直接进入对应的知识页面；后续如需表达前置关系，应在具体知识页或稳定专题页中增加关联链接，而不是新增一套并行路线页面。

## 每批校验

```bash
git diff --check
bash check_html_link.sh
bash check_safe.sh
```

同时核对：变更索引的 href、`data-path`、`data-app-root`；旧路径引用；重复 canonical URL；本地目录树、卡片路由、容器返回、跨学科链接。

> 已完成：全仓索引可发现性校验、`git diff --check`、旧路径引用与 topic-tree 路由接入审计。知识卡片通过 `container.html?page=...&from=...` 在新标签页打开；`from` 只接受仓库内的 `index.html` 路径，使容器“返回”可精确回到打开卡片的来源目录，同时保留旧链接的一级学科回退。`check_safe.sh` 因 CLI 安全分类服务暂时不可用尚未实际执行；在该服务恢复后仍应补跑一次，以完成本地 `href` / `src` 与敏感信息扫描。
