# Visuals

一个以动态可视化为核心特色的 IT 在线学习平台，提供直观易懂、丰富多元的学习内容。

<img width="1528" height="1351" alt="Image" src="https://github.com/user-attachments/assets/f3842819-b00c-43c5-91ad-1338bc4a0a5a" />

## 项目简介

Visuals 致力于通过可视化的方式，让复杂的计算机科学概念变得简单易懂。从计算机组成原理到AI人工智能等这一系列基础理论到高级架构的全面知识体系，全部使用可视化的动态交互、以及图表网页的方式，帮助开发者深入理解技术原理。

## 知识体系

### 计算机理论基础
- 📊 **数据结构与算法** - 排序、搜索、链表、树等核心算法 ...
- 💻 **计算机组成原理** - 运算器、存储器、总线系统、多核处理器 ...
- 🖥️ **操作系统** - 进程管理、文件系统、内存管理、系统调用 ...
- 🌐 **计算机网络** - 物理层到应用层协议、DNS、HTTP、TCP/IP ...
- 🏗️ **软件工程** - 设计模式、架构设计、项目实践 ...
- 🤖 **人工智能** - 大模型理论、Prompt Engineering、Agent 应用 ...
- 🔐 **密码学** - 对称加密、非对称加密、数字签名 ...
- ⚙️ **编译原理** - 词法分析、语法分析、代码生成 ...
- 🐍 **编程语言** - 静态/动态类型、语言特性对比 ...

### 技术体系
- 🗄️ **数据库系统** - MySQL、Redis、Elasticsearch 核心原理 ...
- 🔌 **第三方对接** - 支付系统、认证授权、API 对接 ...
- 💼 **业务设计** - OTA 升级、订单履约、营销活动 ...
- 📊 **大数据系统** - Hadoop、Spark、Flink、数据湖 ...
- 🔌 **物联网设计** - MQTT 协议、物联网通信 ...
- 🎮 **游戏设计** - Flash 技术、游戏引擎原理 ...

### 架构设计
- 🪢 **分布式系统** - CAP 理论、Raft 算法、分布式事务 ...
- 🛡️ **高可用系统** - 负载均衡、故障转移、限流降级 ...
- 🔥 **高并发系统** - 锁设计、池化技术、缓存设计、消息队列 ...
- ☁️ **云服务架构** - Nginx、上云、带宽、SLB、WAF、CDN ...

## 项目结构

```
visuals/
├── index.html                          # 首页
├── algorithm/                          # 数据结构与算法
├── artificial-intelligence/            # 人工智能
├── bigdata-system/                     # 大数据系统
├── business-design/                    # 业务设计
├── cloud-architecture/                 # 云服务架构
├── compiler-principles/                # 编译原理
├── computer-composition/               # 计算机组成原理
├── computer-network/                   # 计算机网络
├── container/                          # 容器技术
├── cryptography/                       # 密码学
├── database-system/                    # 数据库系统
├── distributed-system/                 # 分布式系统
├── game-design/                        # 游戏设计
├── high-availability/                  # 高可用系统
├── high-concurrency/                   # 高并发系统
├── iot-design/                         # 物联网设计
├── operating-system/                   # 操作系统
├── programming-language/               # 编程语言
├── software-engineering/               # 软件工程
├── third-party-integration/            # 第三方对接
├── assets/                             # 公共资源
└── check_html_link.sh                  # HTML 链接检查脚本
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
- 支持多级目录结构（如 `algorithm/trees/binary_tree.html` 会检查 `algorithm/index.html`）
- 用颜色标记检查结果（绿色=已链接，红色=未链接，黄色=跳过）
- 显示统计摘要：总计、已链接、未链接数量

**检查规则：**

- `game-design/flash-technology-explained.html` → 检查 `game-design/index.html`
- `algorithm/trees/binary_tree_traversal.html` → 检查 `algorithm/index.html`
- `high-concurrency/kafka/kafka-partition-explained.html` → 检查 `high-concurrency/index.html`

## 贡献指南

1. 新增内容时，请在对应板块的目录下创建 HTML 文件
2. 确保在上级 `index.html` 中添加新页面的链接卡片
3. 使用 `./check_html_link.sh` 检查链接是否完整
4. 保持页面风格与现有设计一致

## License

© 2026 Visuals
