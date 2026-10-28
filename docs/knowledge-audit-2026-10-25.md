# 知识库综合体检报告与补缺记录（2026-10-25）

对全站做了一次"知识分层 / 内容厚度 / 干瘪度 / 干货充足度 / 常用性覆盖"的体检，并把发现的问题全部落地修完。本文记录**方法、结论、已修项与剩余建议**，供后续迭代对照。

---

## 一、体检结论总览

| 维度 | 结论 | 证据 |
| --- | --- | --- |
| 知识分层 | **健康** | 层级校验 0 错；31 学科 / 205 章 / 1398 课程（拆分前） |
| 内容厚度 | **健康** | 单文件目录 637 个（占叶子 68%），但中位 23 KB，85% ≥ 15 KB，无 < 5 KB 的干瘪页 |
| 干货充足度 | **达标** | 干货分最低 25.0，< 25 已清零 |
| 常用性覆盖 | **本轮补齐** | 新增 6 个主流技术深度页（见第三节） |
| 结构完整性 | **本轮修复** | 清 2 个缺陷 + 16 个页面的标题结构（见第二、四节） |

**一句话结论**：不存在"知识干瘪"，真正的短板是**主流技术缺少专页**和**大页缺少可导航的标题结构**，本轮已全部处理。

---

## 二、结构性缺陷（已修复）

### 1. 幽灵空目录（零宽字符）
- 问题：存在一个带 `U+200C`（零宽非连接符）的目录 `architecture‌-design`，肉眼与 `ls` 均无法与正常目录区分，内容为空、引用为 0。
- 处理：定位后直接删除。
- 教训：目录名异常优先怀疑不可见字符，用 Python `os.listdir` + `repr()` 比对，不要只看终端输出。

### 2. 混放违规：目录同时含子目录与松散 HTML
- 问题：`database-system/relational-db/02-mysql/03-query/` 下同时存在子目录 `01-explain/` 和 2 个松散 HTML，违反"目录不得同时含子目录与知识 HTML"。
- 处理：
  1. 新建 `02-join-and-anti-patterns/`，把 `mysql-join-principles.html`、`mysql-query-anti-patterns.html` 移入；
  2. 重写 15 个引用方的 href；
  3. 修 `relational-db/index.html` 的 `data-path` 分组：删除空占位 `<section>`，父层改为由子 `data-path` 自动派生，并按编号把 `01-explain` 排在 `02-join-and-anti-patterns` 之前。

### 3. 冗余嵌套壳（上一轮）
- 折叠 11 处"父目录仅含 1 个子目录、且内仅 1 篇 HTML"的冗余壳（原计划 12 处，`06-evaluation` 因会违反"三级须含四级子目录"而回退）。

### 4. 非法嵌套标题（既有缺陷）
- `thread-architecture-fullstack.html` 中 4 处 `<h2>` 包裹 `<div><h3>…</h3></div>`，属于非法嵌套。
- 处理：外层改为 `<div class="layer-header">`，内层标题升为 `<h2>`，保留 `.stack-layer .layer-icon` / `.subtitle` 等后代选择器继续生效。

### 5. 游离闭合标签（既有缺陷）
- `pydantic-guide.html` 的 SVG `<text>` 内混入一个游离 `</span>`（偏移 24940），导致 span 长期不配平。
- 处理：删除该游离标签。

---

## 三、常用性缺口补齐（新增 6 页）

审计时先做"按名查重"，避免与既有对比页重复。结果：

| 主题 | 既有情况 | 本轮动作 |
| --- | --- | --- |
| 分布式 ID | **已有** `distributed-id.html`（27 KB，覆盖雪花/UUID/号段/时钟回拨） | 不重复建设，标记为已覆盖 |
| 消息队列对比 | **已有** `mq-comparison.html`（RabbitMQ/RocketMQ/Kafka） | 只补缺的产品专页 |
| 数据湖格式 | **已有** `table-format-comparison.html`（Iceberg/Hudi/Delta） | 只补缺的格式专页 |

**真正缺失**的是"对比页有、但单个产品/格式没有专页"。据此新增 6 个深度页：

### 消息队列（architecture-design/distributed-architecture/03-messaging/）
| 页面 | 路径 | 要点 |
| --- | --- | --- |
| RabbitMQ 深度解析 | `04-rabbitmq/rabbitmq.html` | AMQP 模型、四种 Exchange、发布确认、死信、事务链路选型 |
| RocketMQ 深度解析 | `05-rocketmq/rocketmq.html` | NameServer/Broker、CommitLog、事务消息与回查、死信 |
| Pulsar 深度解析 | `06-pulsar/pulsar.html` | 无状态 Broker + BookKeeper、四种订阅、多租户、分层存储 |

### 数据湖格式（system-engineering/bigdata-system/03-data-storage/04-data-lake/）
| 页面 | 路径 | 要点 |
| --- | --- | --- |
| Apache Iceberg 深度解析 | `iceberg.html` | 三层元数据、隐藏分区、模式/分区演进、时间旅行、工程化坑 |
| Apache Hudi 深度解析 | `hudi.html` | Timeline、COW/MOR、索引与增量查询、CDC 入湖 |
| Apache Paimon 深度解析 | `paimon.html` | LSM 表、主键/追加表、changelog 产出、流式数仓 |

6 页均为单文件自包含（内联 CSS/JS、内联 SVG 图解），并已分别注册进 `distributed-architecture/index.html` 与 `bigdata-system/index.html`。

**组内互链**：三篇 MQ 页与三篇湖格式页各自在"相关阅读"区块中互挂卡片（RabbitMQ ↔ RocketMQ ↔ Pulsar、Iceberg ↔ Hudi ↔ Paimon），形成组内闭环导航，本地链接 0 失效。

---

## 四、超大页拆分与标题结构补全

### 1. 拆分 `computer-history.html`（468 KB / 980 行）

原页含 8 个 `<section class="chapter">`，单页过重。按无损原则拆为 7 页，全部保留原 `<head>` 样式：

| 产出页 | 内容 | 体积 |
| --- | --- | --- |
| `computer-history.html` | 保留总览（timeline + 总结 + 导航网格） | 22 KB |
| `turing-machine.html` | 图灵机 | 26 KB |
| `vacuum-tube-era.html` | 真空管时代（SVG 图形密集，本身体量最大） | 422 KB |
| `eniac.html` | ENIAC | 27 KB |
| `von-neumann-architecture.html` | 冯·诺依曼架构 | 28 KB |
| `transistor-era.html` | 晶体管时代 | 26 KB |
| `modern-computer.html` | 现代计算机 | 13 KB |

9 个页面（含原有 2 篇）已全部注册进 `cst/computer-basic/index.html` 的同一 `data-path` 分组，总览页也逐条链接到 6 个子页。

**踩坑**：拆分脚本沿用了原页的 `<title>`，导致 6 个子页标题全部重复为"计算机发展史 —— 从图灵机到现代计算机"，被层级校验判为"课程 title 重复"（6 处）。虽然各页的 `<h1>`/`<h2>` 本就各不相同，仍需把 `<title>` 逐页改写为各自的 h1 才通过校验。**拆页时 `<title>` 必须一并重写，不能只改正文标题。**

### 2. 给"大体积低标题数"页面补语义标题结构

问题形态：这些页面用 `<div class="card-title">` / `<span class="phase-title">` 等**语义为空的 div/span 充当标题**，导致体积巨大却没有一个 h2/h3，既不可导航也不利于可访问性。

处理方式：把承载标题语义的 `div`/`span` 就地升级为 `<h2>`/`<h3>`（**保留原有 class，保证样式选择器继续命中**），并在 CSS 规则中补 `margin-top: 0`（规则已有 `margin-bottom` 时）或 `margin: 0`（原本无 margin 时），避免默认外边距撑开版式。

共处理 16 个页面，累计新增/提升 **约 190 个语义标题**：

| 页面 | h2 变化 | h3 变化 |
| --- | --- | --- |
| `sqlite-tutorial.html`（91 KB） | 0 → 3 | 0 → 17 |
| `network-attacks.html`（79 KB） | 1 → 6 | 0 → 16 |
| `mq-guide.html`（82 KB） | 1 → 11 | 31 → 58 |
| `mysql-locks-cheatsheet.html`（61 KB） | 1 → 15 | 9 |
| `mysql-storage-formats.html`（64 KB） | 1 → 16 | 3 |
| `interpreter-vs-compiler.html`（67 KB） | 1 → 6 | 18 |
| `fulltext-search.html`（63 KB） | 1 → 7 | 27 |
| `pydantic-guide.html`（66 KB） | 1 → 11 | 11 |
| `openai-anthropic-gemini-api-formats.html`（82 KB） | 2 → 12 | 9 |
| `memory-allocators.html`（65 KB） | 1 → 9 | 4 |
| `event-loop-explained.html`（70 KB） | 1 → 12 | 8 |
| `distributed-resilience-patterns.html`（68 KB） | 1 → 6 | 3 |
| `redis-ecommerce-architecture.html`（59 KB） | 1 → 9 | 17 |
| `redis-ae-event-loop.html`（58 KB） | 1 → 9 | 19 |
| `redis-data-types-source.html`（63 KB） | 1 → 6 | 0 → 5 |
| `thread-architecture-fullstack.html` | 修非法嵌套，h2 6 → 10 | 4 |

**结果**：> 60 KB 且 h2 ≤ 2 的页面从 **18 个降到 1 个**；全局非法嵌套标题 **0 处**；所有改动文件 div/span/h1/h2/h3 标签 **100% 配平**。

---

## 五、过程中的坑与经验（可复用）

1. **非贪婪匹配的块边界陷阱**：`<div class="X">(.*?)</div>` 在块内含嵌套 `<div>` 时会把内层 `</div>` 当成块结束，导致结构错乱。正确做法是先确认"块内无嵌套 div"，或改用计数配对的方式取块。
2. **CSS 覆盖陷阱**：给标题类补 `margin: 0` 会**覆盖**原有的 `margin-bottom: 8px/16px`，把设计好的间距抹掉。正确做法是分区处理——已有 `margin-bottom` 时只补 `margin-top: 0`，原无 margin 时才补 `margin: 0`。
3. **后代选择器陷阱**：`.layer-name h3` 这类选择器说明 `layer-name` 是**容器**而非标题本身。把它升级成 `<h2>` 会造出 `<h2><h3></h3></h2>` 的非法嵌套。升级前必须先 grep 该 class 在 CSS 中的使用形态。
4. **配平口径**：把 `<div>` 转成 `<span>` 会让"div 开标签数 − 闭标签数"天然变化，校验脚本必须把这个转换量计入，否则会误判并回滚正确的改动。
5. **标题候选扫描技巧**：用 `class` 名含 `title|heading|hd|caption|name` 的元素作为候选，先统计数量、再检查块内是否有嵌套 `div`，能安全批量定位可升级的伪标题。

---

## 六、剩余建议（未处理，供排期）

| 项 | 说明 |
| --- | --- |
| `network-protocols-full.html`（111 KB） | h2 仅 2，但已有 13 个真实 h3（OSI 各层），且 `.layer-name h3` 依赖后代选择器为每层着色，不宜强升 h2。若要改善，建议按"协议族"增设外层 h2 容器 |
| `vacuum-tube-era.html`（422 KB） | 拆分后仍偏大，因其 SVG 图形密集；如需继续拆，建议按"器件 / 机型 / 影响"再切 |
| Service Mesh 落地 | istio / envoy 仍无专页 |
| 熔断限流 | `circuit-breaker` 仅 1 篇、`rate-limit` 7 篇，相对其常用性偏薄 |

---

## 七、本轮校验结果（全绿）

| 校验 | 结果 |
| --- | --- |
| `check_html_link.sh` | 总计 1447，**已链接 1447，未链接 0** |
| `check_knowledge_hierarchy.py` | 31 学科 / 205 章 / 1416 课程，**结构错误 0**，占位提醒 0 |
| `check_topic_tree.py` | 问题索引页 **0 个** |
| 标签配平（本轮 17 个改动页） | div / span / h1 / h2 / h3 **100% 配平** |
| 非法嵌套标题（全站） | **0 处** |
| 新页面本地链接 | 6 页全部 **0 失效** |

> 注：链接脚本统计 1447，与 `find` 总数 1449 相差 2，差异来自根 `index.html` 与 `container.html`（脚本统计口径不含这两者），属已知口径差异。

## 八、当前规模

- HTML 总数 **1449**（内容页 1417 + index 32）
- 分布：cst 345 / database-system 292 / programming-and-programs 222 / architecture-design 212 / artificial-intelligence 186 / system-engineering 159
