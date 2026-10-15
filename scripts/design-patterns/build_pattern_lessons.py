"""Generate focused, illustrated GoF lessons from reviewed teaching material."""
from html import escape
from pathlib import Path
from pattern_deep_content import DETAILS
from pattern_atlas_data import ATLAS

ROOT = Path(__file__).resolve().parents[2] / "programming-and-programs/design-patterns"
PAGES = []


def add(category, directory, name, icon, line, analogy, problem, rule, roles,
        steps, code, use, caution, question, answer):
    PAGES.append(locals())


def step_html(item):
    out = []
    for index, raw in enumerate(item["steps"].split("|")):
        label, detail, active = raw.split("^")
        title = label
        out.append(
            '<button type="button" data-pattern-step aria-pressed="false" '
            f'data-title="{escape(title, quote=True)}" '
            f'data-detail="{escape(detail, quote=True)}" '
            f'data-active="{escape(active)}">{escape(str(index + 1) + ". " + label)}</button>'
        )
    return "".join(out)


def role_html(item):
    notes = DETAILS[item["directory"][3:]]["roles"].split("|")
    return ''.join(
        f'<button class="pattern-role" type="button" data-pattern-role '
        f'data-role-note="{escape(notes[index], quote=True)}" '
        f'aria-label="查看{escape(role)}的职责">{escape(role)}</button>'
        for index, role in enumerate(item["roles"].split("|"))
    )


def render(item, previous, following):
    e = escape
    slug = item["directory"][3:]
    d = DETAILS[slug]
    atlas = ATLAS[slug]
    category_label = {"02-creational": "创建型", "03-structural": "结构型",
                      "04-behavioral": "行为型"}[item["category"]]
    experiments = []
    for index, raw in enumerate(d["experiments"].split("|")):
        label, route, result, why = raw.split("^")
        experiments.append(
            f'<button type="button" data-lab-option aria-pressed="false" '
            f'data-route="{e(route, quote=True)}" '
            f'data-result="{e(result, quote=True)}" '
            f'data-why="{e(why, quote=True)}">{e(label)}</button>'
        )
    comparisons = []
    for raw in d["compare"].split("|"):
        label, distinction = raw.split("^")
        comparisons.append(f'<tr><th scope="row">{e(label)}</th><td>{e(distinction)}</td></tr>')
    code_notes = "".join(f"<li>{e(x)}</li>" for x in d["code_notes"].split("|"))
    checklist = "".join(f"<li>{e(x)}</li>" for x in d["checklist"].split("|"))
    scenarios = "".join(f"<li>{e(x)}</li>" for x in atlas["scenarios"])
    neighbors = "".join(
        f'<a href="../../{p["category"]}/{p["directory"]}/{p["directory"][3:]}-pattern.html">{e(label)}：{e(p["name"])}</a>'
        for label, p in (("上一篇", previous), ("下一篇", following)) if p
    )
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(item["name"])}：图解与伪代码 - Visuals</title>
<meta name="description" content="{e(item["line"], quote=True)}">
<link rel="stylesheet" href="../../../../assets/pattern-lesson.css"></head>
<body class="pattern-page"><main class="pattern-shell">
<a class="pattern-back" href="../../index.html">← 返回设计模式目录</a>
<header class="pattern-hero"><span class="pattern-kicker">{category_label} DESIGN PATTERN</span>
<h1>{item["icon"]} {e(item["name"])}</h1><p class="pattern-lead">{e(item["line"])}</p>
<div class="pattern-tldr"><strong>一句话记住</strong><span>{e(item["analogy"])}</span></div></header>
<nav class="pattern-toc" aria-label="本页目录"><a href="#problem">问题从哪来</a><a href="#mechanism">图解协作</a><a href="#playground">动手试一试</a><a href="#code">伪代码</a><a href="#decision">选型与边界</a></nav>
<section class="pattern-panel" id="problem"><span class="pattern-eyebrow">01 · 从问题出发</span><h2>为什么会需要这个模式？</h2>
<p class="pattern-lead-small">{e(item["problem"])}</p>
<p>{e(d["failure"])}</p>
<div class="pattern-before-after"><div class="pattern-before"><h3>😵 直接写会怎样</h3>
<pre class="pattern-code"><code>{e(d["naive"])}</code></pre></div>
<div class="pattern-after"><h3>💡 关键转折</h3><p>{e(item["rule"])}</p>
<p class="pattern-highlight">{e(d["turning_point"])}</p></div></div></section>
<section class="pattern-lesson" id="mechanism" data-pattern-lesson aria-label="{e(item["name"])}交互流程">
<span class="pattern-eyebrow">02 · 把协作过程看清楚</span><h2>点击角色和步骤，跟着一次调用走</h2>
<p class="pattern-help">先点角色看职责，再按步骤观察谁在工作。绿色角色是当前步骤的参与者。</p>
<div class="pattern-roles">{role_html(item)}</div>
<p class="pattern-role-detail" data-role-detail aria-live="polite"></p>
<div class="pattern-controls" role="group" aria-label="流程步骤">{step_html(item)}
<button type="button" class="pattern-play" data-pattern-play aria-pressed="false">▶ 自动播放</button></div>
<div class="pattern-scene" aria-live="polite"><h3 data-scene-title></h3><p data-scene-detail></p></div>
<div class="pattern-progress" aria-hidden="true"><span data-pattern-progress></span></div></section>
<section class="pattern-panel" id="playground"><span class="pattern-eyebrow">03 · 亲手改变输入</span><h2>小实验：换一个条件，会发生什么？</h2>
<p>{e(d["lab_intro"])}</p><div class="pattern-lab" data-pattern-lab>
<div class="pattern-lab-options" role="group" aria-label="选择实验条件">{''.join(experiments)}</div>
<div class="pattern-lab-stage"><div class="pattern-lab-route" data-lab-route aria-label="执行路径"></div>
<div class="pattern-lab-result"><strong>得到的结果</strong><p data-lab-result></p></div>
<p class="pattern-lab-why" data-lab-why></p></div></div></section>
<section class="pattern-panel" id="code"><span class="pattern-eyebrow">04 · 从图到代码</span><h2>最小伪代码：把变化留在正确的位置</h2>
<pre class="pattern-code"><code>{e(item["code"])}</code></pre>
<div class="pattern-code-notes"><h3>读代码时抓住三件事</h3><ol>{code_notes}</ol></div>
<h3>换个业务场景，还能认出来吗？</h3><p>{e(d["transfer"])}</p></section>
<section class="pattern-panel" id="decision"><span class="pattern-eyebrow">05 · 用对边界</span><h2>什么时候用，什么时候收手？</h2>
<div class="pattern-mini-grid"><div><h3>判断信号</h3><p>{e(atlas["signal"])}</p>
<h3>三个具体场景</h3><ul class="pattern-list">{scenarios}</ul></div>
<div><h3>不适合或要小心</h3><p>{e(item["caution"])}</p><p>{e(atlas["avoid"])}</p></div></div>
<h3>最容易混淆的相邻模式</h3><div class="pattern-table-wrap"><table class="pattern-table"><thead><tr><th>模式</th><th>真正的区别</th></tr></thead><tbody>{''.join(comparisons)}</tbody></table></div>
<p class="pattern-highlight"><strong>区分时问自己：</strong>{e(atlas["question"])}</p>
<h3>落地前检查</h3><ul class="pattern-list">{checklist}</ul></section>
<section class="pattern-panel"><span class="pattern-eyebrow">06 · 自己说一遍</span><h2>两道检验理解的小题</h2>
<details class="pattern-quiz"><summary>{e(item["question"])}</summary><p>{e(item["answer"])}</p></details>
<details class="pattern-quiz"><summary>{e(d["question2"])}</summary><p>{e(d["answer2"])}</p></details></section>
<nav class="pattern-neighbors" aria-label="相邻模式">{neighbors}</nav>
<footer class="pattern-footer">© 2026 Visuals · {category_label}模式</footer>
</main><script src="../../../../assets/pattern-lesson.js"></script></body></html>
'''


add("02-creational","02-factory-method","工厂方法","🏭",
    "把“创建哪一种产品”交给可替换的创建者。","外卖平台走同一套下单流程，具体由哪家厨房做菜交给店铺决定。",
    "导出流程固定，但 PDF 与 CSV 的创建细节不同；每加一种格式就修改流程，分支会不断增长。",
    "父类定义使用产品的流程和创建入口；子类只负责决定创建哪种具体产品。",
    "客户端|创建者|具体创建者|产品",
    "发起任务^客户端请求导出，尚不指定产品类。^0|调用工厂方法^创建者在通用流程中调用 createExporter()。^1|选择产品^PdfCreator 返回 PdfExporter；CsvCreator 返回 CsvExporter。^2,3|执行通用流程^创建者调用统一的 export(data) 契约。^1,3",
    "interface Exporter { export(data) }\nabstract class ExportCreator {\n  abstract createExporter(): Exporter\n  run(data) { return this.createExporter().export(data) }\n}\nclass PdfCreator extends ExportCreator {\n  createExporter() { return new PdfExporter() }\n}",
    "创建逻辑会扩展，而消费产品的流程稳定。","只有一个固定产品时直接构造更简单。与简单工厂相比，扩展点在创建者子类，而非一个不断变大的 switch。",
    "新增 HTML 格式要修改 run(data) 吗？","不用；增加 HtmlCreator 和 HtmlExporter 即可。")

add("02-creational","03-abstract-factory","抽象工厂","🎨",
    "一次选择一整套彼此兼容的产品。","换桌游主题包时，棋盘、棋子、卡片要一起属于同一主题。",
    "暗色按钮配亮色弹窗会造成视觉混乱；每个控件各自选主题容易混搭。",
    "抽象工厂声明一组创建方法；具体工厂生产同一个产品族。",
    "客户端|主题工厂|按钮|弹窗",
    "选择系列^客户端只选择 DarkFactory 或 LightFactory。^0,1|创建按钮^factory.createButton() 得到当前主题按钮。^1,2|创建弹窗^同一个工厂产出配套弹窗。^1,3|组合界面^界面使用统一接口，保持整套主题一致。^0,2,3",
    "interface ThemeFactory {\n  createButton(): Button\n  createDialog(): Dialog\n}\nclass DarkFactory implements ThemeFactory {\n  createButton() { return new DarkButton() }\n  createDialog() { return new DarkDialog() }\n}\nrender(factory.createButton(), factory.createDialog())",
    "有多个产品族，且必须保证同一族组件一起工作。","新增产品族容易；新增产品种类要修改所有工厂。工厂方法只决定一种产品，抽象工厂管理一组相关产品。",
    "为什么不分别创建 DarkButton 和 LightDialog？","单独构造不能保证产品族一致；同一工厂能统一约束。")

add("02-creational","04-builder","建造者","🧱",
    "把复杂对象的组装过程拆成清楚的步骤。","点餐先选主食、再选配菜与饮料，最后确认套餐。",
    "HTTP 请求有方法、URL、头、超时、正文；长参数列表容易把可选项填错。",
    "Builder 收集配置步骤，build() 统一校验并产出完整对象。",
    "调用方|建造者|步骤配置|结果",
    "开始构建^调用方创建 RequestBuilder。^0,1|逐项配置^method、url、timeout 各有明确方法。^1,2|校验约束^build() 检查必填字段与跨字段规则。^1,2|交付对象^得到完整 Request，交给网络层。^0,3",
    "request = RequestBuilder()\n  .method(\"POST\")\n  .url(\"/orders\")\n  .header(\"Content-Type\", \"application/json\")\n  .body(payload)\n  .build()  // 校验后返回不可变 Request",
    "对象有多个可选参数、构造顺序或跨字段约束。","不要为了两个简单参数引入 Builder。build() 后最好返回不可变结果，避免半成品对象继续被修改。",
    "为什么在 build() 校验？","各配置步骤可按不同顺序执行；最终统一校验才能保证对象完整。")

add("02-creational","05-prototype","原型","🧬",
    "复制已有样板，再修改少量差异。","复制设计好的邀请函，只换收件人和日期。",
    "每次创建图表都重新配置颜色、坐标轴、规则很费事；已有一个正确模板。",
    "原型提供 clone；复制后只改个性化字段。",
    "模板|复制操作|新对象|修改点",
    "准备模板^图表模板已有默认主题与坐标轴。^0|复制状态^clone 创建新对象，可变嵌套数据也要复制。^0,1|定制差异^只改标题和数据源。^2,3|独立使用^修改副本不影响模板。^0,2",
    "class ChartTemplate {\n  clone() {\n    return ChartTemplate(\n      style = copy(this.style),\n      axes = deepCopy(this.axes),\n      series = deepCopy(this.series))\n  }\n}\nsales = template.clone()\nsales.title = \"本周销售\"",
    "初始化成本高，或组合由运行时决定，且常以模板为起点。","关键是复制深度：共享可变列表会互相污染。数据库连接等外部资源通常不能直接复制。",
    "浅拷贝含可变数组的模板会怎样？","两个对象可能共用数组；改副本也会改模板，需按字段定义复制策略。")

add("03-structural","02-bridge","桥接","🌉",
    "把两个独立变化的维度拆开，用组合连接。","遥控器和电视品牌分别发展；遥控器只对设备接口发指令。",
    "通知渠道有邮件/短信，消息等级有普通/紧急；继承组合会产生越来越多子类。",
    "抽象层持有实现接口；两边可分别扩展，不形成乘法式子类。",
    "消息抽象|渠道接口|邮件实现|短信实现",
    "定义抽象^UrgentNotice 决定加急规则。^0|注入渠道^构造时传入满足 send(text) 的渠道。^0,1|选择实现^EmailChannel 或 SmsChannel 负责投递。^1,2,3|自由组合^加急消息可切换渠道，无需新增组合子类。^0,2,3",
    "interface Channel { send(text) }\nclass Notice {\n  constructor(channel: Channel) { this.channel = channel }\n  send(text) { this.channel.send(text) }\n}\nclass UrgentNotice extends Notice {\n  send(text) { this.channel.send(\"[加急] \" + text) }\n}\nnew UrgentNotice(new SmsChannel()).send(\"付款失败\")",
    "存在两个独立变化维度，例如消息类型 × 投递渠道。","若只有一个变化维度，普通组合已足够。桥接的两侧都应有独立演进的理由。",
    "新增微信渠道要增加 UrgentWechatNotice 吗？","不用；新增 WechatChannel，再注入现有 Notice。")

add("03-structural","03-composite","组合","🌳",
    "让单个对象和一组对象用同一种方式被处理。","文件和文件夹都能“求大小”；文件夹把子项大小相加。",
    "报价单有商品和嵌套套餐；调用方为每层分别写递归分支很难维护。",
    "叶子和容器实现同一接口；容器递归委托给孩子。",
    "客户端|统一组件|单个商品|套餐容器",
    "调用接口^客户端只调用 totalPrice()。^0,1|遇到叶子^Item 直接返回自身价格。^1,2|遇到容器^Bundle 累加孩子的 totalPrice()。^1,3|递归完成^套餐仍可嵌套套餐，返回整棵树总价。^0,2,3",
    "interface Component { totalPrice() }\nclass Item implements Component {\n  totalPrice() { return this.price }\n}\nclass Bundle implements Component {\n  totalPrice() {\n    return sum(child.totalPrice() for child in this.children)\n  }\n}\ncart.totalPrice()",
    "业务结构天然是树，且要对叶子与容器执行同一操作。","add/remove 不必强塞进叶子接口。要防止构造循环引用，否则递归可能无限进行。",
    "嵌套三层套餐为何仍能求总价？","每层只依赖 Component.totalPrice()；叶子返回价格，容器递归求和。")

add("03-structural","04-decorator","装饰器","🎁",
    "保持原接口，按需叠加行为。","咖啡先是美式，再加奶和糖；每层包装仍是一杯饮品。",
    "数据流按需压缩、加密、记录日志；为每种组合建子类会迅速膨胀。",
    "每个装饰器实现同一接口并包住下一个对象，调用沿包装链传递。",
    "客户端|日志装饰器|加密装饰器|原始流",
    "构造链^原始流包进加密器，再包进日志器。^1,2,3|统一调用^客户端只调用 stream.write(data)。^0,1|逐层叠加^日志器记录调用，加密器改写字节，最后写入原始流。^1,2,3|更换组合^移除或交换包装层即可改变职责。^0,1,2",
    "interface Stream { write(bytes) }\nclass EncryptStream implements Stream {\n  constructor(inner: Stream) { this.inner = inner }\n  write(bytes) { this.inner.write(encrypt(bytes)) }\n}\nclass LogStream implements Stream {\n  constructor(inner: Stream) { this.inner = inner }\n  write(bytes) { log(\"write\"); this.inner.write(bytes) }\n}\nstream = new LogStream(new EncryptStream(new FileStream()))",
    "需要在运行时自由叠加可选职责，且保留相同接口。","包装顺序可能改变结果。装饰器侧重叠加行为；适配器侧重翻译不兼容接口。",
    "客户端为何无需知道包了几层？","每一层都实现 Stream.write；外部看仍是一个 Stream。")

add("03-structural","05-facade","外观","🏛️",
    "给复杂子系统一个容易使用的入口。","影院“一键观影”会关灯、开投影、切音源。",
    "下单要验证库存、计价、支付、记录订单；调用方重复编排容易漏步骤。",
    "Facade 提供高层操作，内部协调子系统；底层能力仍可独立使用。",
    "客户端|结账外观|库存/计价|支付/订单",
    "发起结账^客户端调用 checkout(cart) 一次。^0,1|验证与计价^外观调用库存和价格服务。^1,2|执行支付^外观按顺序调用支付，再写订单。^1,3|返回结果^客户端获得订单结果。^0,1",
    "class CheckoutFacade {\n  checkout(cart) {\n    inventory.reserve(cart.items)\n    receipt = null\n    try {\n      amount = pricing.total(cart)\n      receipt = payment.charge(amount)\n      return orders.create(cart, receipt)\n    } catch (error) {\n      if (receipt != null) payment.refund(receipt)\n      inventory.release(cart.items)\n      throw error  // 补偿失败还需重试与人工恢复\n    }\n  }\n}",
    "多个调用方都需要同一套复杂操作顺序。","真实结账仍需处理失败补偿与幂等。外观简化入口，却不会自动解决事务。",
    "外观是否必须禁止访问子系统？","不必；它提供常用高层流程，特殊需求仍可调用合适的底层接口。")

add("03-structural","06-flyweight","享元","♻️",
    "共享大量对象中相同的不变部分。","森林有十万棵树，树种贴图共用，坐标各不相同。",
    "地图标记都保存相同图标、颜色、字体，会重复占用大量内存。",
    "把可共享的内在状态放进享元；坐标等外在状态在调用时传入。",
    "享元工厂|共享图标|外部坐标|绘制调用",
    "请求样式^按类型向工厂请求 MarkerStyle。^0|复用对象^同类型返回同一不可变样式对象。^0,1|传入位置^每个标记的坐标保存在外部记录。^2|组合绘制^共享样式，同时显示不同位置。^1,2,3",
    "class StyleFactory {\n  cache = Map()\n  get(kind) {\n    if (!cache.has(kind)) cache.set(kind, immutableStyle(kind))\n    return cache.get(kind)\n  }\n}\nfor marker in markers:\n  draw(factory.get(marker.kind), marker.x, marker.y)",
    "有海量细粒度对象，且它们共享大量不变状态。","不要把每个对象独有的可变状态写进共享实例；先测量内存收益。",
    "共用同一贴图的树能有不同位置吗？","能；贴图共享，位置作为外在状态在每次绘制时传入。")

add("03-structural","07-proxy","代理","🛡️",
    "在访问真实对象前加一道控制关卡。","门卫先核验身份，再决定能否进入。",
    "图片加载耗时，或敏感文档读取需要授权；客户端仍希望调用同一接口。",
    "代理和真实对象实现同一接口，拦截调用并控制加载、鉴权或缓存。",
    "客户端|代理|访问规则|真实对象",
    "统一请求^客户端调用 document.read()。^0,1|检查规则^代理先验证权限或查看缓存。^1,2|按需转发^通过后才创建或调用真实对象。^1,3|返回内容^代理将结果交还客户端。^0,1,3",
    "interface Document { read(user) }\nclass SecureProxy implements Document {\n  constructor(docId, loader, authorization) {\n    this.docId = docId; this.loader = loader\n    this.auth = authorization; this.real = null\n  }\n  read(user) {\n    if (!this.auth.canRead(user, this.docId)) throw Forbidden\n    if (this.real == null) this.real = this.loader()\n    return this.real.read(user)\n  }\n}",
    "要控制对对象的访问，例如延迟加载、权限、远程调用或缓存。","权限检查必须可信。代理重点是控制访问；装饰器重点是叠加职责。",
    "为什么代理与真实对象实现同一接口？","客户端不必改调用方式，代理决定何时访问真实对象。")


add("04-behavioral","01-chain-of-responsibility","责任链","🔗",
    "让请求沿着一条处理链传递，直到有人处理或链走完。","报销单先到组长，金额太大再交经理。",
    "请求要经过鉴权、限流、业务校验；把所有步骤硬写在一个巨型函数里，增删步骤都难。",
    "每个处理器只做自己的事，并决定继续传给下一位或就此结束。",
    "请求|鉴权节点|限流节点|业务节点",
    "进入链^请求进入首个处理器。^0,1|鉴权^无权限直接拒绝；通过才调用 next。^1|限流^超过配额直接返回；否则继续。^2|业务处理^最后一个节点执行真实业务并返回结果。^3",
    "function auth(req, next) {\n  if (!req.user) return Unauthorized\n  return next(req)\n}\nfunction limit(req, next) {\n  if (quota.exceeded(req.user)) return TooManyRequests\n  return next(req)\n}\nhandle = chain(auth, limit, business)\nresult = handle(request)",
    "一组检查或处理步骤需要灵活组合、调整顺序或提前终止。","明确链尾行为；顺序会影响语义，比如鉴权应先于耗资源操作。不要让处理器悄悄吞掉请求。",
    "鉴权失败后限流节点还会执行吗？","此例不会；鉴权处理器直接返回，未调用 next。")

add("04-behavioral","02-command","命令","🎮",
    "把一次操作包装成对象，方便排队、记录和撤销。","遥控器按钮只知道“执行命令”，不关心灯或空调怎样工作。",
    "编辑器按钮直接操作文档，若要支持撤销、快捷键和操作历史，每个入口都需重复逻辑。",
    "命令对象保存接收者与参数，提供 execute；需要撤销时再定义 undo。",
    "按钮|命令对象|接收者|历史记录",
    "创建命令^把文档和要插入的文本放入 InsertTextCommand。^1,2|触发执行^按钮只调用 command.execute()。^0,1|修改对象^命令让文档插入文本，并记录撤销所需位置。^1,2|记录与撤销^历史保存命令，撤销时调用 undo()。^1,3",
    "class InsertTextCommand {\n  constructor(doc, pos, text) {\n    this.doc = doc; this.pos = pos; this.text = text\n  }\n  execute() { this.doc.insert(this.pos, this.text) }\n  undo() { this.doc.delete(this.pos, this.text.length) }\n}\ncmd = new InsertTextCommand(doc, cursor, \"Hello\")\ncmd.execute()\nhistory.push(cmd)\n// history.pop().undo()",
    "操作需要排队、记录、重放、撤销，或由多种触发器调用。","撤销需要保存足够的前置状态；并非每种操作都能简单逆转，例如外部付款要用补偿操作。",
    "撤销删除文本时为什么要保存原文？","没有原文就无法恢复被删除的内容。")

add("04-behavioral","03-interpreter","解释器","🧮",
    "把小语言的语法规则变成可组合的表达式对象。","计算器先把“3 + 5 × 2”拆成语法树，再按规则求值。",
    "过滤条件支持 AND、OR、字段比较；到处拼字符串会让语义和优先级混乱。",
    "每种语法节点实现 interpret(context)，复合节点递归解释子节点。",
    "输入规则|解析器|语法树|上下文",
    "读取规则^输入 age >= 18 AND active。^0|构建树^解析器按语法和优先级生成 And 节点。^1,2|递归求值^And 调用两个子表达式的 interpret。^2|读取数据^叶子节点在 context 中取得 age 和 active。^2,3",
    "interface Expr { interpret(ctx): Boolean }\nclass And implements Expr {\n  constructor(left, right) {\n    this.left = left; this.right = right\n  }\n  interpret(ctx) {\n    return this.left.interpret(ctx) && this.right.interpret(ctx)\n  }\n}\nrule = And(GreaterEqual(\"age\", 18), Field(\"active\"))\nallowed = rule.interpret(user)",
    "语言很小、语法稳定，且希望组合与解释规则。","不要把任意用户输入直接 eval。复杂语言的词法、语法、错误处理通常交给成熟解析器。",
    "AND 节点为什么无需知道 age 字段？","它只组合两个 Expr；字段读取由叶子节点负责。")

add("04-behavioral","04-iterator","迭代器","🚶",
    "统一逐个访问元素，同时隐藏集合的内部结构。","图书馆借阅员只说“下一本”，不用知道书架是数组还是树。",
    "调用方既要遍历数组又要遍历树；若直接依赖存储结构，换结构会改遍历代码。",
    "集合提供迭代器，调用方只用 hasNext/next 或语言的 for-of 协议。",
    "调用方|迭代器|集合结构|当前元素",
    "获取迭代器^调用方请求 collection.iterator()。^0,1|保存位置^迭代器记录当前下标或遍历栈。^1,2|取下一项^next() 返回元素并推进位置。^1,3|走到末尾^hasNext() 为 false，循环结束。^0,1",
    "iterator = collection.iterator()\nwhile iterator.hasNext():\n  item = iterator.next()\n  visit(item)\n\n// 树迭代器内部可维护 stack；调用方不需要知道。",
    "需要统一遍历不同集合，或提供多种遍历顺序。","迭代期间修改集合要定义规则：快照、失败即报错或弱一致。迭代器不自动解决并发安全。",
    "把数组换成树，调用方循环要改吗？","若迭代器契约相同，就不必改；只换集合内部的迭代实现。")

add("04-behavioral","05-mediator","中介者","🕹️",
    "让多个对象通过一个协调者沟通，减少两两依赖。","机场塔台统一调度飞机起降，飞机无需互相决定跑道顺序。",
    "表单里地区、城市、邮编输入框互相通知；组件越多，两两引用越乱。",
    "组件只把变化告诉 Mediator；Mediator 决定谁该更新。",
    "地区组件|表单中介者|城市组件|邮编组件",
    "改变地区^用户选择新的地区。^0|发送事件^地区组件通知 mediator.changed('region')。^0,1|协调更新^中介者清空城市选项并按地区重载。^1,2|连锁调整^中介者清空不再有效的邮编。^1,3",
    "class FormMediator {\n  onRegionChanged(region) {\n    city.setOptions(citiesFor(region))\n    city.clear()\n    postcode.clear()\n  }\n}\nregion.onChange(value => mediator.onRegionChanged(value))",
    "多个组件有密集的相互协作，协调规则需要集中管理。","中介者可能膨胀成巨型规则类；可按业务流程拆分。它负责交互规则，不应吞掉各组件自身职责。",
    "城市组件需直接引用地区组件吗？","不用；变更由中介者接收并协调。")

add("04-behavioral","06-memento","备忘录","📸",
    "保存对象快照，以后恢复到之前的状态。","游戏存档保存角色位置和血量，读档后回到那一刻。",
    "画布编辑器要支持撤销，但历史管理器不该直接改画布内部字段。",
    "原发器生成/恢复快照；保管者只保存快照，不解释其中内容。",
    "画布对象|快照|历史栈|恢复操作",
    "保存前态^画布调用 save() 生成快照。^0,1|交给历史^历史栈保存快照，不读取内部细节。^1,2|继续编辑^画布位置、颜色等状态变化。^0|执行撤销^弹出快照，由画布 restore(snapshot) 恢复。^0,2,3",
    "class Canvas {\n  save() { return Snapshot(deepCopy(this.shapes)) }\n  restore(snapshot) { this.shapes = deepCopy(snapshot.shapes) }\n}\nundoStack.push(canvas.save())\ncanvas.move(shape, dx, dy)\ncanvas.restore(undoStack.pop())",
    "需要历史版本、撤销或可恢复的会话状态。","快照可能很大；可限制历史长度、保存增量或与命令模式结合。深浅拷贝必须按状态所有权设计。",
    "历史栈为什么不直接改 shapes？","快照的创建与恢复由画布负责，历史栈只保管，避免破坏封装。")

add("04-behavioral","08-state","状态","🚦",
    "把不同状态下的行为分给不同状态对象。","地铁闸机在“锁定”和“已解锁”时，对推门动作反应不同。",
    "订单的待支付、已支付、已取消对 cancel/pay 有不同规则；巨型 if/else 难以维护。",
    "Context 持有当前 State；每个状态决定可执行动作和下一状态。",
    "订单上下文|待支付状态|已支付状态|已取消状态",
    "初始状态^订单从 Pending 开始。^0,1|执行支付^Pending.pay() 收款成功后切到 Paid。^1,2|再次支付^Paid.pay() 拒绝重复付款或返回幂等结果。^0,2|执行取消^不同状态各自定义取消规则。^1,2,3",
    "interface OrderState { pay(order); cancel(order) }\nclass Pending implements OrderState {\n  pay(order) { charge(order); order.state = new Paid() }\n  cancel(order) { order.state = new Cancelled() }\n}\nclass Paid implements OrderState {\n  pay(order) { return AlreadyPaid }\n  cancel(order) { return RefundRequired }\n}",
    "同一对象因当前状态不同而表现不同，且状态规则/迁移较多。","不要只为两个简单布尔分支引入一堆类。状态迁移应明确定义非法操作及副作用失败时的处理。",
    "已支付订单再次 pay() 会走 Pending.pay() 吗？","不会；订单委托给当前 Paid 状态，按 Paid 的规则响应。")

add("04-behavioral","09-strategy","策略","🧭",
    "把可互换的算法封装起来，由使用方选择。","导航可以选最快、最短或避开收费道路的路线算法。",
    "运费计算因普通、加急、自提而不同；把所有公式塞进订单对象会让它不断增长。",
    "Context 持有 Strategy 接口，运行时注入某个算法。",
    "订单上下文|策略接口|普通运费|加急运费",
    "确定需求^用户选择普通配送。^0|注入策略^系统注入 StandardShipping。^0,1,2|执行算法^普通策略根据重量计算费用。^1,2|获取结果^订单只调用 strategy.cost(order)，无需识别类型。^0,1",
    "interface ShippingStrategy { cost(order) }\nclass StandardShipping implements ShippingStrategy {\n  cost(order) { return 5 + order.weight * 2 }\n}\nclass ExpressShipping implements ShippingStrategy {\n  cost(order) { return 15 + order.weight * 4 }\n}\norder.shipping = new ExpressShipping()\nfee = order.shipping.cost(order)",
    "多个算法完成同一目标，调用方需要按条件切换。","策略选择本身仍要有规则；别把选择逻辑又散落到所有调用点。与状态模式相比，策略通常由外部选择，状态由对象的生命周期迁移。",
    "新增次日达会改订单的 cost 逻辑吗？","不用；新增实现 ShippingStrategy 的策略并在选择处注入。")

add("04-behavioral","10-template-method","模板方法","🍪",
    "固定算法骨架，把少数步骤留给子类定制。","烘焙流程先和面、再烘烤、最后装盘；不同面包替换配方细节。",
    "CSV 和 JSON 导入都要打开文件、解析、校验、保存；复制整个流程会让关键顺序漂移。",
    "父类定义不可随意改的流程，子类实现差异步骤。",
    "导入模板|打开文件|格式解析|校验与保存",
    "启动流程^调用模板的 import(file)。^0|公共步骤^模板负责打开文件和关闭资源。^0,1|可变步骤^子类实现 parse(stream)。^0,2|完成流程^模板统一校验并保存记录。^0,3",
    "abstract class Importer {\n  import(file) {\n    stream = open(file)\n    try {\n      rows = this.parse(stream)  // 子类实现\n      validate(rows)\n      save(rows)\n    } finally { stream.close() }\n  }\n  abstract parse(stream)\n}\nclass CsvImporter extends Importer { parse(s) { return readCsv(s) } }",
    "整体流程稳定，只有少量步骤因类型而变，且顺序必须一致。","继承会让子类与父类耦合；变化维度多时可用组合和策略。不要让子类重写整个模板入口破坏约束。",
    "为什么 close() 放在父类模板中？","资源释放是所有导入都必须遵守的共同步骤，放父类能防遗漏。")

add("04-behavioral","11-visitor","访问者","🧳",
    "把作用于对象结构的操作放到访问者中。","博物馆同一批展品，可由讲解员讲历史，也可由估价师估价。",
    "语法树节点类型稳定，但要频繁新增格式化、类型检查、代码生成等操作。",
    "节点提供 accept(visitor)；访问者按具体节点类型实现 visitX。",
    "客户端|语法树节点|访问者接口|具体操作",
    "选择操作^客户端创建 PrettyPrinter 或 TypeChecker。^0,3|节点接待^节点执行 visitor.visitNumber(this) 等方法。^1,2|按类型处理^具体访问者知道节点类型并执行对应逻辑。^2,3|遍历子节点^复合节点继续调用孩子的 accept。^1,3",
    "interface Visitor { visitNumber(node); visitAdd(node) }\nclass NumberNode {\n  accept(visitor) { return visitor.visitNumber(this) }\n}\nclass AddNode {\n  accept(visitor) { return visitor.visitAdd(this) }\n}\nclass PrettyPrinter implements Visitor {\n  visitNumber(n) { return String(n.value) }\n  visitAdd(n) { return n.left.accept(this) + \"+\" + n.right.accept(this) }\n}",
    "对象结构较稳定，但需要经常新增作用于整棵结构的操作。","新增节点类型会迫使所有访问者增加方法；若节点常变，访问者可能反而增加维护成本。",
    "新增“统计节点数”会修改所有节点吗？","通常只需增加一个 Visitor 实现，已有节点继续调用 accept。")

add("03-structural","01-adapter","适配器","🔌",
    "把外部接口翻译成业务已经理解的接口。","旅行插头转换器让不同插头接进同一个插座。",
    "业务要求 send(message)，外部 SDK 却只有 publish(payload)；若直接调用 SDK，字段差异会散落到业务代码。",
    "适配器实现目标接口，内部持有第三方对象并完成参数、结果和错误翻译。",
    "业务调用方|适配器|目标接口|外部 SDK",
    "发起通知^业务只调用 notifier.send(message)。^0,2|进入边界^Adapter 接收目标接口参数。^1,2|翻译调用^Adapter 把 text 映射为 body，调用 publish。^1,3|统一结果^将 SDK 结果与错误转换成业务语义。^0,1",
    "interface Notifier { async send(message) }\nclass SmsAdapter implements Notifier {\n  constructor(sdk) { this.sdk = sdk }\n  async send(message) {\n    try {\n      return await this.sdk.publish({ body: message.text,\n                                      recipient: message.phone })\n    } catch (error) { throw translate(error) }\n  }\n}",
    "对接已有的外部库、老系统或不同数据格式，同时保持业务侧契约稳定。",
    "适配器只翻译边界；若塞进大量业务规则，说明领域职责可能放错位置。",
    "更换短信 SDK 后业务侧的 send 调用要改吗？",
    "不需要；实现另一个 Notifier 适配器，并保持同一契约。")

add("04-behavioral","07-observer","观察者","📣",
    "一个对象变化，已订阅的对象自动得到通知。","订阅天气播报的人，在天气变化后各自收到更新。",
    "订单支付后，页面、审计和通知都要响应；订单若直接调用每个模块，会与所有下游耦合。",
    "主题对象维护订阅集合，状态变化后通知订阅者；订阅者可独立加入或退出。",
    "发布者|订阅集合|页面观察者|审计观察者",
    "登记订阅^页面与审计模块订阅订单变化。^1,2,3|状态变化^订单先完成自己的状态更新。^0|发布事件^主题遍历订阅集合，传递 OrderPaid。^0,1|各自处理^页面刷新，审计记录；必要时取消订阅。^2,3",
    "class Subject {\n  listeners = Set()\n  subscribe(fn) {\n    listeners.add(fn)\n    return () => listeners.delete(fn)\n  }\n  emit(event) {\n    for fn in copy(listeners): fn(event)\n  }\n}\nstop = orderEvents.subscribe(onOrderPaid)\norderEvents.emit(OrderPaid(orderId))\nstop()",
    "同一进程内多个模块要对状态变化作独立响应，且订阅者会增减。",
    "同步回调会影响发布者的耗时和错误传播；跨服务可靠投递要用持久化消息与幂等消费。",
    "为什么订阅函数最好返回取消订阅句柄？",
    "组件卸载或任务结束时可移除回调，避免重复处理和长期持有对象。")


def main():
    PAGES.sort(key=lambda item: (item["category"], item["directory"]))
    assert all(item["directory"][3:] in DETAILS and item["directory"][3:] in ATLAS for item in PAGES)
    for index, item in enumerate(PAGES):
        filename = item["directory"][3:] + "-pattern.html"
        path = ROOT / item["category"] / item["directory"] / filename
        path.write_text(render(item, PAGES[index - 1] if index else None,
                               PAGES[index + 1] if index + 1 < len(PAGES) else None),
                        encoding="utf-8")
    index_path = ROOT / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    groups = []
    for item in sorted(PAGES, key=lambda page: (page["category"], page["directory"])):
        cat = item["category"]
        directory = item["directory"]
        filename = directory[3:] + "-pattern.html"
        name = escape(item["name"])
        icon = escape(item["icon"])
        line = escape(item["line"])
        groups.append(
            f'<section class="topic-group" data-path="{cat}/{directory}" '
            f'data-title="{name}" data-icon="{icon}" data-desc="{line}">'
            f'<div class="topics"><a class="card" href="{cat}/{directory}/{filename}">'
            f'<span class="card-icon">{icon}</span><h2>{name}模式</h2>'
            f'<p>{line}</p></a></div></section>'
        )
    start = "<!-- generated pattern groups start -->"
    end = "<!-- generated pattern groups end -->"
    before, rest = index_html.split(start, 1)
    _, after = rest.split(end, 1)
    index_path.write_text(before + start + "\n            " +
                          "\n            ".join(groups) + "\n            " + end + after,
                          encoding="utf-8")
    print(f"Generated {len(PAGES)} pattern lessons")


if __name__ == "__main__":
    main()
