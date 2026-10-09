# 优化后目录结构（补齐 NN- 序号，最小改动方案）

> **历史迁移草案（2026-10-08）**：此文件记录当时的规划，括号中的旧目录说明不代表当前仍待迁移。实际目录以仓库文件树为准；本轮核查与剩余的语义归属问题见 [知识结构核查](knowledge-structure-audit.md)。

> 规则：只给**真正不带 `NN-` 前缀**的目录补序号；已带 `00-`/`NN-` 的目录（含 `00-overview` 概览约定）一律保留。
> L3 序号断档用「后续目录整体下移」消除。括号内 `(原: xxx)` 表示该目录将被改名。

## artificial-intelligence/

  model-audio/
    01-tts/
      01-speech-synthesis-markup/
    02-asr/
      01-speech-recognition-basics/
  model-basic/
    00-neural-networks/
      01-training-basics/
      02-generalization/
      03-architecture-evolution/
    01-embedding/
      01-embedding-foundations/
    02-transformer/
      01-architecture/
      02-attention/
      03-components/
      04-inference/
    03-scaling/
      01-model-capacity/
    04-limits/
      01-memory-limits/
      02-hallucination/
    05-synthesis-and-review/
      01-self-assessment/
      02-paradigm-comparison/
  model-image/
    00-overview/
      01-image-model-overview/
    01-foundations/
      01-image-representation/
      02-image-formats-and-codecs/
    02-image-understanding/
      01-image-classification/
      02-object-detection/
      03-image-segmentation/
      04-ocr/
    03-image-generation/
      01-diffusion-models/
      02-text-to-image/
      03-gan/
    04-image-editing/
      01-inpainting/
      02-super-resolution/
      03-style-transfer/
    05-multimodal-vision/
      01-vision-language-model/
      02-visual-question-answering/
    06-evaluation-and-safety/
      01-generation-metrics/
      02-watermark-and-forensics/
  model-llm/
    01-development/
      01-history/
    02-principle/
      01-scaling-laws/
      02-decoding/
    03-token/
      01-tokenization/
    04-context/
      01-window-and-length/
      02-context-engineering/
      03-model-specifications/
    05-prompt/
      01-in-context-learning/
      02-prompting-methods/
      03-structured-output/
    06-thinking/
      01-reasoning-foundations/
      02-reasoning-techniques/
    07-planning/
      01-planning-basics/
      02-planning-methods/
    08-function-calling/
      01-tool-calling/
    09-multimodal/
      01-vision-understanding/
      02-vision-language-models/
      03-image-generation/
    10-evaluation/
      01-benchmarks/
      02-model-selection/
    11-safety/
      01-attack-and-defense/
  model-ops/
    01-pre-training/
      01-foundations/
      02-data-engineering/
    02-fine-tuning/
      01-fine-tuning-strategies/
      02-parameter-efficient-fine-tuning/
    03-reinforcement-learning/
      01-rl/
      02-rlhf-dpo/
    04-distillation/
      01-distillation-foundations/
    05-deploy/
      01-model-quantization/
      02-model-serving/
      03-inference-acceleration/
    06-distributed-training/
      01-parallelism/
  model-video/
    00-overview/
      01-video-model-overview/
    01-foundations/
      01-frame-and-timeline/
      02-codec-and-container/
      03-bitrate-and-quality/
    02-video-understanding/
      01-action-recognition/
      02-temporal-modeling/
      03-video-retrieval/
    03-video-generation/
      01-text-to-video/
      02-temporal-consistency/
      03-diffusion-video/
    04-video-editing/
      01-frame-interpolation/
      02-video-super-resolution/
      03-inpainting-and-removal/
    05-streaming-and-realtime/
      01-streaming-protocols/
      02-realtime-inference/
    06-evaluation-and-safety/
      01-video-metrics/
      02-deepfake-and-forensics/

## cst/

  computer-algorithm/
    01-algorithmic-techniques/
      00-overview/
      01-bit-manipulation/
      02-strategy-comparison/
    02-complexity-analysis/
      00-overview/
    03-data-structures/
      00-overview/
    04-arrays-and-linked-lists/
      00-overview/
      01-linked-lists/
      02-two-pointers/
      03-sliding-window/
      04-prefix-sums-and-difference/
    05-stacks-and-queues/
      00-overview/
      01-stacks-and-queues/
      02-priority-queues/
    06-hash-tables/
      00-overview/
      01-hash-fundamentals/
    07-trees/
      00-overview/
      01-tree-traversal/
      02-balanced-trees/
    08-heaps/
      00-overview/
      01-heap-fundamentals/
      02-max-heaps/
      03-min-heaps/
    09-graphs/
      00-overview/
      01-graph-traversal/
      02-connectivity/
      03-topological-sort/
      04-shortest-path/
      05-minimum-spanning-tree/
    10-search/
      00-overview/
      01-binary-search/
      02-string-matching/
    11-sorting/
      00-overview/
      01-sorting-algorithms/
      02-heap-sort/
    12-divide-and-conquer/
      00-overview/
    13-backtracking/
      00-overview/
      01-backtracking/
    14-dynamic-programming/
      00-overview/
    15-greedy/
      00-overview/
    16-computation-theory/
      00-overview/
      01-automata/
      02-turing-machines/
      03-complexity-classes/
  computer-composition/
    01-overview/
      01-computer-organization/
    02-foundations/
      01-digital-logic-and-electronics/   (原: digital-logic-and-electronics)
    03-instruction-set-architecture/
      01-architecture-families/   (原: architecture-families)
    04-processor-foundations/
      01-bits-buses-and-addressing/
      02-architecture-and-datapath/
    05-processor-execution-and-control/
      01-instruction-execution/   (原: instruction-execution)
      02-parallelism/   (原: parallelism)
      03-registers/   (原: registers)
      04-timing-and-control/   (原: timing-and-control)
    06-memory-hierarchy/
      01-cache/   (原: cache)
      02-main-memory/   (原: main-memory)
      03-memory-ordering/   (原: memory-ordering)
      04-overview/   (原: overview)
    07-input-output/
      01-buses/   (原: buses)
      02-device-communication/   (原: device-communication)
      03-interrupts/   (原: interrupts)
    08-storage/
      01-solid-state-storage/   (原: solid-state-storage)
      02-storage-devices/   (原: storage-devices)
    09-system-lifecycle/
      01-boot/   (原: boot)
      02-program-execution/   (原: program-execution)
    10-advanced-architecture/
      01-execution-stack/   (原: execution-stack)
  computer-history/
    01-computing-evolution/
      01-computer-and-hardware-history/
    02-web-platform-evolution/
      01-browser-plugin-era/
    03-people-and-ideas/
      01-quotations-and-attribution/
  computer-math/
    01-topology/
      01-foundations-and-applications/
    02-discrete-mathematics/
      00-overview/
      01-set-theory/
      02-propositional-logic/
      03-relations-and-functions/
      04-combinatorics/
      05-boolean-algebra/
    03-linear-algebra/
      00-overview/
      01-vectors-matrices/
      02-determinants-inverses/
      03-eigenvalues/
    04-probability-statistics/
      00-overview/
      01-probability-basics/
      02-random-variables/
      03-statistical-inference/
    05-number-theory/
      00-overview/
      01-modular-arithmetic/
      02-primes-gcd/
      03-rsa-cryptography/
    06-mathematical-logic/
      00-overview/
      01-proof-techniques/
      02-predicate-logic/
  computer-network/
    01-link-layer/
      01-arp-and-ndp/   (原: arp-and-ndp)
    02-network-layer/
      01-icmp-and-diagnostics/   (原: icmp-and-diagnostics)
      02-ip/   (原: ip)
      03-nat-and-address-translation/   (原: nat-and-address-translation)
      04-routing/   (原: routing)
    03-transport-layer/
      01-code-implementation/   (原: code-implementation)
      02-overview/   (原: overview)
      03-tcp/   (原: tcp)
        01-congestion-control/   (原: congestion-control)
        02-connection-lifecycle/   (原: connection-lifecycle)
        03-connection-queues/   (原: connection-queues)
        04-reliable-delivery/   (原: reliable-delivery)
        05-stream-framing/   (原: stream-framing)
    04-application-layer/
      01-dns/   (原: dns)
      02-file-and-content-delivery/   (原: file-and-content-delivery)
        01-p2p/   (原: p2p)
      03-realtime-communication/   (原: realtime-communication)
        01-protocol-selection/   (原: protocol-selection)
        02-server-sent-events/   (原: server-sent-events)
        03-websocket/   (原: websocket)
      04-web/   (原: web)
        01-http/   (原: http)
          01-connection-management/   (原: connection-management)
          02-http-versions/   (原: http-versions)
          03-message-format/   (原: message-format)
          04-protocol/   (原: protocol)
          05-request-lifecycle/   (原: request-lifecycle)
          06-server-implementation/   (原: server-implementation)
        02-https-and-tls/   (原: https-and-tls)
    05-end-to-end-flows/
      01-protocol-overview/
      02-request-lifecycle/
    06-network-performance/
      01-metrics/   (原: metrics)
    07-network-security/
      01-common-attacks/   (原: common-attacks)
      02-web-and-cdn-protection/   (原: web-and-cdn-protection)
    08-troubleshooting-and-observability/
      01-packet-capture/   (原: packet-capture)
  computer-operating-system/
    01-overview/
      01-operating-system-basics/
    02-foundations/
      01-boot-and-program-execution/   (原: boot-and-program-execution)
      02-protection-and-privilege/   (原: protection-and-privilege)
    03-processes/
      01-cmd/   (原: cmd)
      02-lifecycle-and-control/   (原: lifecycle-and-control)
      03-process-control-block/   (原: process-control-block)
      04-program-loading-and-execution/   (原: program-loading-and-execution)
    04-threads-and-concurrency/
      01-context-switching/   (原: context-switching)
      02-execution-models/   (原: execution-models)
      03-thread-management/   (原: thread-management)
    05-memory-management/
      01-address-spaces/   (原: address-spaces)
      02-allocation-and-fragmentation/   (原: allocation-and-fragmentation)
      03-kernel-allocators/   (原: kernel-allocators)
      04-memory-models/   (原: memory-models)
      05-page-replacement/   (原: page-replacement)
      06-user-space-allocators/   (原: user-space-allocators)
      07-virtual-memory/   (原: virtual-memory)
    06-input-output/
      01-buffering/   (原: buffering)
      02-network-io/   (原: network-io)
        01-socket/   (原: socket)
      03-storage-io/   (原: storage-io)
    07-file-systems/
      01-overview/   (原: overview)
    08-virtualization/
      01-virtualization-fundamentals/
    09-observability-and-practice/
      01-observability-basics/

## database-system/

  newsql/
    00-overview/
      01-distributed-rdbms-foundations/
    01-tidb/
      01-tidb-foundations/
    02-oceanbase/
      01-oceanbase-foundations/
    03-cockroachdb/
      01-crdb-foundations/
  nosql-db/
    01-kv/
      01-cache-patterns/
      02-memcached/   (原: memcached)
        01-architecture/
        02-data-model/
        03-distributed/
        04-practice/
      03-redis/   (原: redis)
        00-overview/
        01-data-structures/
        02-io/
        03-event-loop/
        04-pipeline-transaction/
        05-concurrency/
        06-memory/
        07-persistence/
        08-architecture/
        09-advanced/
    02-document/
      01-elasticsearch/   (原: elasticsearch)
        01-architecture/
        02-indexing/
        03-search/
        04-operations/
      02-mongodb/   (原: mongodb)
        01-data-model/
        02-indexing/
        03-query/
        04-replication-sharding/
        05-practice/
    03-column-family/
      01-hbase/   (原: hbase)
        01-data-model/
        02-architecture/
        03-storage/
        04-operations/
    04-graph/
      01-neo4j/   (原: neo4j)
        01-data-model/
        02-cypher/
        03-architecture/
        04-operations/
  olap/
    00-overview/
      01-olap-foundations/
      02-columnar-and-vectorized/
    01-clickhouse/
      01-clickhouse-foundations/
      02-mergetree-engine/
    02-doris-starrocks/
      01-doris-foundations/
    03-selection/
      01-olap-selection/
  relational/
    00-overview/
      01-comparison/
      02-data-modeling/
    01-mysql/
      01-architecture/
        01-connections-and-resources/
        02-sql-execution/
        03-optimizer-entry/
      02-indexes/
        01-bplus-tree-and-pages/
        02-index-types-and-design/
        03-index-usage-and-pitfalls/
      03-query/
      04-pagination/
        01-deep-pagination/
      05-transaction/
      06-locks/
      07-logs/
        01-redo-undo-logs/
      08-storage/
      09-engines/
      10-memory/
      11-master-slave/
      12-availability/
      13-analytics/
      14-search/
      15-optimizer/
      16-executor/
    02-postgresql/
      01-architecture/
      02-indexes/
      03-query/
      04-pagination/
      05-transaction/
      06-locks/
      07-wal/
      08-storage/
      09-vacuum/
      10-memory/
      11-replication/
      12-availability/
      13-extension/
      14-search/
      15-optimizer/
      16-executor/
    03-sqlite/
      01-architecture/
      02-tutorial/
      03-transaction-lock/
      04-index/
      05-data-types/
      06-performance/
  sql-core/
    01-query/
      01-join/
      02-window-functions/
    02-aggregation/
      01-group-by/
    03-execution/
      01-execution-order/
  timeseries/
    00-overview/
      01-tsdb-foundations/
    01-influxdb/
      01-influxdb-foundations/
    02-tdengine/
      01-tdengine-foundations/
  vectordb/
    00-overview/
      01-vector-database-foundations/
      02-index-and-retrieval/
      03-retrieval-performance/
    01-milvus/
      01-milvus-foundations/
    02-qdrant/
      01-qdrant-foundations/
    03-weaviate/
      01-weaviate-foundations/

## programming-and-programs/

  build-program/
    01-bytecode/
      01-bytecode-foundations/
    02-compiler/
      01-code-generation/   (原: code-generation)
      02-foundations/   (原: foundations)
      03-frontend/   (原: frontend)
        01-parsing/   (原: parsing)
          01-grammar-transformation/   (原: grammar-transformation)
          02-parser-implementation/   (原: parser-implementation)
          03-parsing-algorithms/   (原: parsing-algorithms)
      04-intermediate-representation/   (原: intermediate-representation)
      05-language-case-studies/   (原: language-case-studies)
      06-linking-and-loading/   (原: linking-and-loading)
      07-optimization/   (原: optimization)
      08-overview/   (原: overview)
      09-tooling-and-implementation/   (原: tooling-and-implementation)
    03-language-classification/
      01-type-systems/
    04-interpreter/
      01-interpreter-fundamentals/
  golang/
    01-program-structure/
      01-modules-and-dependencies/   (原: modules-and-dependencies)
      02-naming-and-declarations/   (原: naming-and-declarations)
      03-packages-and-files/   (原: packages-and-files)
    02-language-basics/
      01-basic-types/   (原: basic-types)
      02-control-flow/   (原: control-flow)
      03-language-features/   (原: language-features)
      04-pointers-and-values/   (原: pointers-and-values)
    03-data-structures/
      01-arrays-and-slices/   (原: arrays-and-slices)
      02-maps-and-hash-tables/   (原: maps-and-hash-tables)
      03-serialization-and-templates/   (原: serialization-and-templates)
      04-strings-and-text/   (原: strings-and-text)
      05-structs-and-embedding/   (原: structs-and-embedding)
    04-functions-and-methods/
      01-error-handling/   (原: error-handling)
      02-function-values-and-closures/   (原: function-values-and-closures)
      03-functions/   (原: functions)
      04-methods-and-encapsulation/   (原: methods-and-encapsulation)
    05-type-system/
      01-generics/   (原: generics)
      02-interfaces/   (原: interfaces)
      03-reflection/   (原: reflection)
      04-type-assertions/   (原: type-assertions)
    06-concurrency/
      01-atomic-and-lock-free/   (原: atomic-and-lock-free)
      02-channels-and-select/   (原: channels-and-select)
      03-concurrency-patterns/   (原: concurrency-patterns)
      04-context-and-cancellation/   (原: context-and-cancellation)
      05-goroutines/   (原: goroutines)
      06-memory-model/   (原: memory-model)
      07-synchronization/   (原: synchronization)
    07-runtime/
      01-garbage-collection/   (原: garbage-collection)
      02-gmp-scheduler/   (原: gmp-scheduler)
      03-memory-allocation/   (原: memory-allocation)
      04-network-poller/   (原: network-poller)
      05-stack-management/   (原: stack-management)
      06-timers-and-system-monitor/   (原: timers-and-system-monitor)
    08-compiler-and-low-level/
      01-assembly-and-debugging/   (原: assembly-and-debugging)
      02-cgo-and-interop/   (原: cgo-and-interop)
      03-compiler-pipeline/   (原: compiler-pipeline)
      04-intermediate-and-machine-code/   (原: intermediate-and-machine-code)
      05-unsafe-and-memory-layout/   (原: unsafe-and-memory-layout)
    09-packages-tools-and-testing/
      01-benchmarks-and-profiling/   (原: benchmarks-and-profiling)
      02-code-style-and-naming/   (原: code-style-and-naming)
      03-coverage-and-race-detection/   (原: coverage-and-race-detection)
      04-go-command/   (原: go-command)
      05-testing/   (原: testing)
    10-standard-library/
      01-database/   (原: database)
      02-diagnostics-and-observability/   (原: diagnostics-and-observability)
      03-encoding-and-serialization/   (原: encoding-and-serialization)
      04-io-and-filesystem/   (原: io-and-filesystem)
      05-networking-and-http/   (原: networking-and-http)
      06-sorting-and-data-processing/   (原: sorting-and-data-processing)
    11-advanced-programming/
      01-code-generation/   (原: code-generation)
      02-design-patterns/   (原: design-patterns)
      03-metaprogramming/   (原: metaprogramming)
      04-plugins/   (原: plugins)
    12-engineering-practices/
      01-api-and-validation/   (原: api-and-validation)
        01-api-and-validation/   (原: api-and-validation)
      02-configuration-and-environment/   (原: configuration-and-environment)
      03-database-and-transactions/   (原: database-and-transactions)
      04-deployment-and-operations/   (原: deployment-and-operations)
      05-logging-and-observability/   (原: logging-and-observability)
      06-project-layout/   (原: project-layout)
    13-ecosystem/
      01-ecosystem-overview/   (原: ecosystem-overview)
      02-framework-comparisons/   (原: framework-comparisons)
      03-frameworks/   (原: frameworks)
        01-gin/   (原: gin)
        02-go-zero/   (原: go-zero)
          01-api-and-rpc/   (原: api-and-rpc)
          02-basics-and-architecture/   (原: basics-and-architecture)
          03-engineering-and-operations/   (原: engineering-and-operations)
          04-model-and-database/   (原: model-and-database)
      04-microservices/   (原: microservices)
      05-observability/   (原: observability)
      06-web-frameworks/   (原: web-frameworks)
      07-web-services/   (原: web-services)
    14-reference/
      01-appendix/   (原: appendix)
      02-book-notes/   (原: book-notes)
      03-glossary/   (原: glossary)
      04-learning-path/   (原: learning-path)
      05-quick-reference/   (原: quick-reference)
  python/
    01-language-basics-and-syntax/
      01-syntax-and-types/
      02-functions-and-decorators/
      03-iteration/
    02-runtime-and-memory/
      01-execution-model/
      02-memory-management/
    03-modules-and-packages/
      01-import-and-modules/
    04-concurrency/
      01-gil-and-limits/
      02-threading-and-sync/
      03-concurrency-models/
    05-async-and-event-loop/
      01-event-loop/
      02-async-await-basics/
      03-asyncio-practice/
    06-engineering-and-deployment/
      01-engineering-basics/
      02-observability-and-logging/
      03-web-framework-and-serving/
  runtime-mechanisms/
    01-memory-model/
      01-stack-heap-and-value-semantics/
      02-object-layout/
    02-memory-management/
      01-allocation-and-defragmentation/
      02-allocator-strategies/
    03-garbage-collection/
      01-collection-algorithms/
      02-gc-across-languages/
    04-event-driven-execution/
      01-event-loop/
      02-callback-to-async/
    05-performance-principles/
      01-locality/
      02-branch-and-cache/
    06-program-execution/
      01-source-to-process/
  software-design/
    01-foundations/
      02-design-principles/
      03-programming-paradigms/
      01-design-patterns/   (原: design-patterns)
    02-interface-integration/
      01-api-design/   (原: api-design)
      02-data-serialization/   (原: data-serialization)
      03-external-calls/   (原: external-calls)
    03-security/
      01-identity-and-access/   (原: identity-and-access)
    04-business-design/
      01-business-systems/   (原: business-systems)
        01-content/   (原: content)
        02-marketing/   (原: marketing)
        03-transaction/   (原: transaction)
      02-industry-systems/   (原: industry-systems)
        01-iot-and-device/   (原: iot-and-device)
          01-connectivity/   (原: connectivity)
          02-lifecycle/   (原: lifecycle)
    05-code-quality/
      01-refactoring/
      02-code-review/

## system-engineering/

  ai-engineering-system/
    01-api/
      01-api-integration/
    02-knowledge/
      01-document-ingestion/   (原: document-ingestion)
      02-knowledge-base-construction/   (原: knowledge-base-construction)
    03-rag/
      01-foundations/
      02-retrieval-strategies/
      03-quality-and-evaluation/
      04-performance/
    04-memory-case-studies/
      01-mem0-memory-engineering/
      02-openclaw-memory-engineering/
    05-mcp/
      01-protocol/
      02-integration-comparison/
    06-skills/
      01-skills-basics/
      02-skills-development/
    07-agent/
      01-agent-design/
      02-multi-agent/
    08-evaluation/
      01-model-evaluation/
      02-safety-evaluation/
    09-api-operations/
      01-rate-limiting/
    10-ai-development/   (原: 11-ai-development)
      00-overview/
      01-claude-code/   (原: claude-code)
      02-harness/   (原: harness)
      03-openclaw/   (原: openclaw)
  bigdata-system/
    00-overview/
      01-bigdata-foundations/
    01-data-collection/
      01-offline-collection/
      02-realtime-collection/
    02-data-storage/
      01-distributed-filesystem/
      02-nosql-storage/
      03-file-formats/
      04-data-lake/
    03-data-processing/
      01-batch-processing/
      02-stream-processing/
      03-interactive-query/
      04-graph-computing/
      05-performance-tuning/
    04-data-governance/
      01-metadata/
      02-data-quality/
      03-scheduling/
      04-monitoring/
    05-data-analysis-and-application/
      01-data-warehouse/
      02-sql-and-olap/
      03-bi-and-visualization/
      04-ai-and-recommendation/
  cache-system/
    01-localcache/   (原: 02-localcache)
      01-guava-caffeine/
      02-ehcache/
      03-handwritten/
    02-distributed-cache/   (原: 03-distributed-cache)
      03-memcached/
      04-consistent-hashing/
    03-eviction/   (原: 04-eviction)
      01-lru-lfu/
      02-arc-tinylfu/
      03-ttl-tti/
    04-consistency/   (原: 05-consistency)
      01-cache-patterns/
      02-dual-write/
    05-anomalies/   (原: 06-anomalies)
      01-penetration/
      02-breakdown/
      03-avalanche/
    06-multilevel-cache/   (原: 07-multilevel-cache)
      01-multi-level/
      02-cdn/
      03-best-practice/
  cloud-architecture/
    01-cloud-basics/
      01-cloud-vs-local/   (原: cloud-vs-local)
      02-general/   (原: general)
        01-architecture-foundations/
        02-scaling-and-reliability/
      03-how-to-cloud/   (原: how-to-cloud)
    02-IT-infrastructure/
      01-infrastructure-foundations/
    03-cloud-network/
      00-network-overview/
      01-bandwidth/   (原: bandwidth)
      02-cdn/   (原: cdn)
      03-slb/   (原: slb)
      04-vpc/   (原: vpc)
    04-web-serving/
      01-api/   (原: api)
      02-nginx/   (原: nginx)
      03-webserver/   (原: webserver)
    05-container/
      01-kubernetes/   (原: kubernetes)
    06-edge-computing/
      01-edge-computing-foundations/
    07-architecture/   (原: 08-architecture)
      00-software-architecture/
      01-architecture-styles/
      02-architecture-patterns/
      03-distributed-patterns/
      04-cloud-architecture/
  distributed-system/
    01-basics/
      01-consistency-theory/
      02-consistency-practice/
      03-consensus/   (原: consensus)
      04-intro/   (原: intro)
      05-scenarios/   (原: scenarios)
    02-coordination/
      01-lock/   (原: lock)
      02-zookeeper/   (原: zookeeper)
    03-messaging/
      01-message-queue-foundations/
        01-concepts-and-selection/
        02-delivery-and-operations/
      02-kafka/
        01-architecture-and-components/
        02-partitions-and-replication/
        03-delivery-and-reliability/
        04-consumer-groups/
      03-redis-queues/
    04-transaction/
      01-distributed-transactions/
    05-storage/
      01-sharding-and-ids/
      02-replication-and-hashing/
    06-microservices/
      00-microservice-foundations/
      01-rpc/   (原: rpc)
    07-service-mesh/
      01-service-mesh-foundations/
    08-resilience/
      01-reliability-patterns/
  high-performance-concurrency-availability/
    01-performance-evaluation-framework/   (原: 03-performance-evaluation-framework)
      00-overview/
      01-throughput/
      02-latency-and-percentiles/
      03-concurrency-and-queueing/
      04-capacity-and-limits/
      05-benchmarking/
    02-high-concurrency/   (原: 01-high-concurrency)
      01-cache/   (原: cache)
        01-hotspots/   (原: hotspots)
      02-concepts/   (原: concepts)
      03-concurrency-models/   (原: concurrency-models)
      04-cpu-vs-io/   (原: cpu-vs-io)
      05-lock/   (原: lock)
      06-overview/   (原: overview)
      07-pools/   (原: pools)
      08-traffic-patterns/   (原: traffic-patterns)
      09-http-connections/
      10-client-admission-control/
    03-high-availability/   (原: 02-high-availability)
      01-data-replication/   (原: data-replication)
      02-deploy/   (原: deploy)
      03-foundations/   (原: foundations)
      04-general/   (原: general)
      05-geo-redundancy/   (原: geo-redundancy)
      06-traffic-protection/   (原: traffic-protection)
    04-high-performance/   (原: programming-and-programs/performance-optimization)
      01-cpu-optimization/
      02-memory-optimization/
      03-network-io-optimization/
      04-file-io-optimization/
      05-troubleshooting/
