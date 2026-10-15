"""Add interactive walkthroughs and pseudocode to existing architecture pattern pages."""
from html import escape
from pathlib import Path
from architecture_pattern_labs import LABS
from architecture_pattern_decisions import DECISIONS

ROOT = Path(__file__).resolve().parents[2] / "system-engineering/whole-architecture-system"
LESSONS = []


def add(path, hook, roles, steps, code, edge):
    LESSONS.append(locals())


add("02-architecture-styles/01-layered/layered-architecture.html",
    "像餐厅的前台、厨房、仓库：请求按职责逐层处理，每层只认识约定的下一层。",
    "请求|表示层|业务层|数据层",
    "接收输入^表示层解析请求和基础格式。^0,1|执行规则^业务层检查库存与订单规则。^1,2|读写数据^数据层负责持久化，不决定业务政策。^2,3|返回结果^结果沿调用链返回给用户。^0,1,2",
    "function placeOrder(request):\n  dto = web.parse(request)\n  order = application.place(dto)\n  // application 调用 repository.save(order)\n  return web.respond(order)",
    "边界：分层不是每层都必须转发空壳方法；跨层调用规则应明确，避免业务逻辑泄漏到控制器。")

add("02-architecture-styles/02-service-oriented/soa.html",
    "把企业能力做成有契约的服务，多个业务流程可以复用同一能力。",
    "订单流程|服务契约|客户服务|库存服务",
    "提出需求^订单流程需要客户资料与库存状态。^0|调用契约^通过版本化服务契约请求能力。^0,1|服务独立处理^客户服务和库存服务各维护自身数据。^2,3|组合结果^订单流程协调结果并处理部分失败。^0,2,3",
    "customer = customerService.get(customerId)\nif not customer.active: return Rejected\nstock = inventoryService.reserve(items)\ntry:\n  return orderService.create(customer, stock)\ncatch error:\n  inventoryService.release(stock)\n  throw error",
    "边界：服务化会增加网络调用和治理成本。共享契约不能变成所有服务直接共享数据库。")

add("02-architecture-styles/03-event-driven/event-driven-architecture.html",
    "像新闻订阅：事实发生后发事件，感兴趣的下游各自处理。",
    "订单服务|事件总线|积分服务|通知服务",
    "完成事务^订单服务提交已支付状态。^0|发布事实^发出 OrderPaid(orderId) 事件。^0,1|并行消费^积分服务加积分，通知服务发消息。^2,3|处理失败^消费者按重试与幂等规则恢复。^1,2,3",
    "transaction:\n  order.markPaid()\n  outbox.insert(OrderPaid(order.id))\n// 提交后由发布器把 outbox 送入总线\non OrderPaid(event):\n  if not processed(event.id): grantPoints(event.orderId)",
    "边界：事件是已发生事实；可靠投递需要 outbox/重试等机制，消费者要能处理重复与乱序。")

add("02-architecture-styles/04-microservices/monolith-vs-microservices.html",
    "像把大车间拆成小工坊：可以独立交付，但需要额外运输和协调。",
    "业务边界|订单服务|库存服务|运行平台",
    "寻找边界^按业务能力和数据所有权拆分。^0|独立部署^订单服务可单独发布。^1,3|跨服务协作^订单通过 API 或事件请求库存能力。^1,2|运维治理^监控、追踪、重试和故障隔离成为必需。^1,2,3",
    "function submitOrder(command):\n  order = orders.createPending(command)\n  inventory.reserve(command.items, command.id)\n  orders.confirm(order.id)\n// 网络失败需重试/补偿，不能假设是本地函数调用",
    "边界：拆分前先确认团队、部署节奏和扩展瓶颈。小系统优先保持清晰模块边界。")

add("03-application-patterns/01-presentation-and-flow/mvc-pattern.html",
    "像餐馆：顾客下单给服务员，厨房处理数据，菜单/餐盘负责展示。",
    "用户|Controller|Model|View",
    "发出操作^用户提交搜索或编辑请求。^0,1|修改模型^Controller 调用 Model 的业务操作。^1,2|准备展示^Controller 选择视图并传入模型数据。^1,3|渲染界面^View 把数据呈现给用户。^0,3",
    "function showOrder(request):\n  id = request.path.orderId\n  order = orderModel.find(id)\n  return orderView.render(order)",
    "边界：Web MVC 常由 Controller 将数据传给 View；传统桌面 MVC 可由 View 观察 Model。")

add("03-application-patterns/01-presentation-and-flow/pipe-filter-pattern.html",
    "像流水线：每站只处理自己的一步，输出交给下一站。",
    "输入|解析过滤器|清洗过滤器|输出",
    "读取原料^原始日志进入管道。^0|解析结构^解析器将文本转成结构化记录。^1|清洗数据^清洗器过滤无效记录并补全字段。^2|写出结果^最终结果写入存储或下一段管道。^3",
    "records = readLines(source)\nparsed = map(parseLine, records)\nvalid = filter(isValid, parsed)\nwrite(sink, map(normalize, valid))",
    "边界：每段应有明确输入输出契约；有状态过滤器和错误处理需要额外约定。")

add("03-application-patterns/02-boundaries-and-dependencies/clean-architecture.html",
    "像同心圆：业务规则在中心，数据库和界面在外圈，依赖箭头指向中心。",
    "用户界面|用例|领域规则|数据库适配器",
    "收到请求^界面把输入转成用例参数。^0,1|执行业务^用例调用领域实体的规则。^1,2|访问存储^用例依赖仓储接口，外圈适配器实现它。^1,3|返回结果^用例输出结果，界面负责展示格式。^0,1",
    "interface OrderRepository { save(order) }\nclass PlaceOrder {\n  constructor(repo: OrderRepository) { this.repo = repo }\n  run(items) {\n    order = Order.create(items)  // 领域规则\n    this.repo.save(order)\n    return order.id\n  }\n}",
    "边界：内层不导入具体数据库或 Web 框架；接口应由内层需求定义，而非为每个类机械造接口。")

add("03-application-patterns/02-boundaries-and-dependencies/hexagonal-architecture.html",
    "像通用插座：业务核心只认端口，HTTP、CLI、数据库都是可替换适配器。",
    "输入适配器|应用端口|业务核心|输出适配器",
    "进入系统^HTTP 控制器或 CLI 把请求转成端口调用。^0,1|执行业务^核心按领域规则处理订单。^1,2|访问外部^核心通过仓储端口请求持久化。^2,3|替换技术^换数据库只替换输出适配器。^0,2,3",
    "interface PlaceOrderPort { place(items) }\ninterface OrderStore { save(order) }\nclass PlaceOrder implements PlaceOrderPort {\n  constructor(store: OrderStore) { this.store = store }\n  place(items) { this.store.save(Order.create(items)) }\n}",
    "边界：端口代表业务需要的能力；别把数据库客户端接口原样搬进核心。")

add("03-application-patterns/03-read-write-separation/cqrs-pattern.html",
    "写入和查询各走适合自己的模型，像收银台与看板分工。",
    "写命令|命令模型|查询模型|读请求",
    "提交命令^用户发出 CreateOrder。^0,1|更新写模型^命令侧验证规则并写入权威数据。^1|投影查询^事件或变更把数据整理成读模型。^1,2|读取视图^读请求直接查询适合展示的模型。^2,3",
    "function createOrder(cmd):\n  transaction:\n    order = Order.create(cmd.items)\n    writeStore.save(order)\n    outbox.insert(OrderCreated(order.id))\n// 提交后发布器投递 outbox，消费者幂等更新读模型\non OrderCreated(event):\n  readStore.upsert(project(event.orderId))",
    "边界：异步投影有延迟；需要定义读己之写体验、重建投影和重复事件处理。简单 CRUD 未必需要 CQRS。")

add("04-distributed-patterns/01-entry-and-discovery/api-gateway.html",
    "像商场服务台：外部只见一个入口，内部按路由分发。",
    "客户端|API 网关|订单服务|用户服务",
    "发起请求^客户端访问统一域名。^0,1|入口处理^网关鉴权、限流并匹配路由。^1|转发服务^订单路径到订单服务，用户路径到用户服务。^2,3|返回响应^网关回传结果与统一错误格式。^0,1",
    "function gateway(request):\n  identity = verifyToken(request.token)\n  enforceRateLimit(identity)\n  target = routes.match(request.path)\n  return forward(target, request, timeout=2s)",
    "边界：网关不应承载复杂领域规则；后端服务仍需保护自己的安全边界。")

add("04-distributed-patterns/01-entry-and-discovery/service-discovery.html",
    "像电话簿：调用方按服务名找当前健康实例，而非记死 IP。",
    "调用方|服务注册表|健康实例 A|健康实例 B",
    "实例注册^实例启动后登记地址和健康状态。^1,2,3|服务查询^调用方查询 order-service 的可用地址。^0,1|选择实例^负载均衡选中一个健康实例。^0,2,3|故障更新^不健康实例被摘除，后续流量转向其余实例。^1,2,3",
    "instances = registry.healthy(\"order-service\")\ntarget = loadBalancer.choose(instances)\ntry:\n  return http.get(target + \"/orders/42\", timeout=1s)\ncatch Timeout:\n  markSuspect(target)",
    "边界：健康检查与注册信息可能滞后；调用方仍需超时、重试预算和故障处理。")

add("04-distributed-patterns/02-resilience-and-traffic/circuit-breaker.html",
    "像保险丝：故障持续时先断开，过一会儿试探是否恢复。",
    "调用方|熔断器|下游服务|回退结果",
    "闭合状态^正常请求通过并记录失败率。^0,1,2|触发断开^失败超过阈值，后续请求快速失败。^1,3|半开探测^冷却后允许少量请求试探。^1,2|恢复或重断^探测成功重新闭合，否则继续断开。^1,2,3",
    "if breaker.state == OPEN:\n  if not cooldownExpired(): return fallback()\n  breaker.enterHalfOpen(maxProbes=1)\nif not breaker.allowRequest(): return fallback()\ntry:\n  result = callDownstream(timeout=500ms)\n  breaker.recordSuccess()  // 探测成功可闭合\n  return result\ncatch error:\n  breaker.recordFailure()  // 超阈值或探测失败则断开\n  return fallback()",
    "边界：熔断不修复下游。阈值、窗口、半开并发和回退结果应按业务影响设置。")

add("04-distributed-patterns/02-resilience-and-traffic/rate-limit-degrade.html",
    "像景区限流：人太多先控制入场，同时保留最重要的游览路线。",
    "入口流量|限流器|核心服务|降级功能",
    "请求到达^入口收到突发流量。^0|计算配额^令牌桶决定是否允许进入。^1|保障核心^获准请求进入支付等核心能力。^2|主动降级^非核心推荐功能可关闭或返回简化结果。^3",
    "if not bucket.tryTake(userId):\n  return TooManyRequests(retryAfter=1s)\nresult = payment.process(order)\nif recommendation.overloaded():\n  return response(result, recommendations=[])\nreturn response(result, recommendation.fetch(order))",
    "边界：限流拒绝入口流量，降级缩减功能；需明确保护目标、优先级和用户可接受的结果。")

add("04-distributed-patterns/03-consistency-and-idempotency/idempotency-design.html",
    "像刷门禁：同一张票重复刷，也只允许一次入场。",
    "请求|幂等键|原子记录|已有结果",
    "携带键^客户端为同一业务操作复用同一个 key。^0,1|原子占位^服务端以 key 原子创建处理记录。^1,2|执行业务^第一次请求执行扣款并保存结果。^2|重复请求^相同 key 直接返回已有结果，不再扣款。^1,3",
    "function charge(request):\n  key = request.idempotencyKey\n  created, record = store.insertIfAbsent(key, status=PROCESSING)\n  if not created:\n    if record.alreadyDone: return record.savedResult\n    return RetryLater\n  result = payment.charge(request)\n  store.complete(key, result)\n  return result",
    "边界：键要绑定请求语义和有效期；占位、业务副作用、结果保存之间仍需事务或恢复方案。")

add("04-distributed-patterns/03-consistency-and-idempotency/saga-pattern.html",
    "像连环预约：机票、酒店、租车逐个确认；后一步失败就逐个取消已成功的预约。",
    "订单本地事务|库存本地事务|支付本地事务|补偿流程",
    "创建订单^本地提交待处理订单。^0|预留库存^库存服务本地提交预留。^1|尝试支付^支付成功则完成；失败则转入补偿。^2|逆序补偿^先释放库存，再取消订单，且补偿需幂等。^3,1,0",
    "completed = []\ntry:\n  order.createPending(); completed.push(cancelOrder)\n  stock.reserve(); completed.push(releaseStock)\n  payment.charge(); completed.push(refundPayment)\ncatch error:\n  for compensate in reverse(completed):\n    retryIdempotently(compensate)",
    "边界：补偿是新的业务动作，并非数据库回滚；要处理补偿失败、事件乱序和中间状态。")


def render(item):
    decision = DECISIONS[Path(item["path"]).stem]
    scenarios = ''.join(f'<li>{escape(scenario)}</li>' for scenario in decision["scenarios"])
    comparisons = ''.join(
        f'<tr><th scope="row">{escape(name)}</th><td>{escape(difference)}</td></tr>'
        for name, difference in decision["comparisons"]
    )
    buttons = []
    for index, raw in enumerate(item["steps"].split("|")):
        title, detail, active = raw.split("^")
        buttons.append(
            f'<button type="button" data-pattern-step aria-pressed="false" '
            f'data-title="{escape(title, quote=True)}" '
            f'data-detail="{escape(detail, quote=True)}" '
            f'data-active="{escape(active)}">{index + 1}. {escape(title)}</button>'
        )
    roles = ''.join(
        f'<div class="pattern-role" data-pattern-role>{escape(role)}</div>'
        for role in item["roles"].split("|")
    )
    intro, options = LABS[Path(item["path"]).stem]
    lab_buttons = []
    for raw in options.split("|"):
        label, route, result, why = raw.split("^")
        lab_buttons.append(
            f'<button type="button" data-lab-option aria-pressed="false" '
            f'data-route="{escape(route, quote=True)}" '
            f'data-result="{escape(result, quote=True)}" '
            f'data-why="{escape(why, quote=True)}">{escape(label)}</button>'
        )
    return f'''<!-- interactive pattern lesson start -->
    <section class="pattern-lesson" data-pattern-lesson aria-label="模式交互演示">
      <h2>动手看一遍：场景、流程、伪代码</h2>
      <p class="pattern-highlight">{escape(item["hook"])}</p>
      <div class="pattern-roles">{roles}</div>
      <div class="pattern-controls" role="group" aria-label="流程步骤">
        {''.join(buttons)}
        <button type="button" class="pattern-play" data-pattern-play aria-pressed="false">▶ 自动播放</button>
      </div>
      <div class="pattern-scene" aria-live="polite"><h3 data-scene-title></h3><p data-scene-detail></p></div>
      <div class="pattern-progress" aria-hidden="true"><span data-pattern-progress></span></div>
      <h3 style="margin-top:24px">改变条件，看看系统怎么走</h3>
      <p>{escape(intro)}</p>
      <div class="pattern-lab" data-pattern-lab>
        <div class="pattern-lab-options" role="group" aria-label="选择实验条件">{''.join(lab_buttons)}</div>
        <div class="pattern-lab-stage">
          <div class="pattern-lab-route" data-lab-route aria-label="执行路径"></div>
          <div class="pattern-lab-result"><strong>得到的结果</strong><p data-lab-result></p></div>
          <p class="pattern-lab-why" data-lab-why></p>
        </div>
      </div>
      <div class="pattern-decision">
        <h3>什么时候适用？</h3>
        <p class="pattern-decision-signal"><strong>判断信号：</strong>{escape(decision["signal"])}</p>
        <ul class="pattern-list">{scenarios}</ul>
        <h3>和相近方案怎么区分？</h3>
        <div class="pattern-table-wrap"><table class="pattern-table">
          <thead><tr><th scope="col">相近方案</th><th scope="col">选择边界</th></tr></thead>
          <tbody>{comparisons}</tbody>
        </table></div>
      </div>
      <h3 style="margin-top:24px">最小伪代码</h3>
      <pre class="pattern-code"><code>{escape(item["code"])}</code></pre>
      <p>{escape(item["edge"])}</p>
    </section>
    <!-- interactive pattern lesson end -->
'''


def main():
    import re
    assert all(Path(item["path"]).stem in LABS for item in LESSONS)
    assert {Path(item["path"]).stem for item in LESSONS} == set(DECISIONS)
    for item in LESSONS:
        page = ROOT / item["path"]
        html = page.read_text(encoding="utf-8")
        html = re.sub(r'<!-- interactive pattern lesson start -->.*?<!-- interactive pattern lesson end -->\s*',
                      '', html, flags=re.S)
        html = html.replace("</head>",
            '<link rel="stylesheet" href="../../../../assets/pattern-lesson.css">\n</head>')
        html = html.replace('<div class="container">',
                            '<div class="container">\n' + render(item), 1)
        html = html.replace("</body>",
            '<script src="../../../../assets/pattern-lesson.js"></script>\n</body>')
        # Re-running the source updates content without duplicating shared assets.
        html = html.replace(
            '<link rel="stylesheet" href="../../../../assets/pattern-lesson.css">\n'
            '<link rel="stylesheet" href="../../../../assets/pattern-lesson.css">',
            '<link rel="stylesheet" href="../../../../assets/pattern-lesson.css">')
        html = html.replace(
            '<script src="../../../../assets/pattern-lesson.js"></script>\n'
            '<script src="../../../../assets/pattern-lesson.js"></script>',
            '<script src="../../../../assets/pattern-lesson.js"></script>')
        page.write_text(html, encoding="utf-8")
    print(f"Enriched {len(LESSONS)} architecture pattern lessons")


if __name__ == "__main__":
    main()
