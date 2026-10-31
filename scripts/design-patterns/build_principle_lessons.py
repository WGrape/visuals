"""Generate practical design-principle lessons with visual branches and pseudocode."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "programming-and-programs/design-patterns"
OUT = ROOT / "01-foundations/02-design-principles"
LESSONS = []


def add(slug, title, icon, lead, signal, story, naive, turn, roles, steps,
        lab_intro, options, code, takeaways, related, caution, question, answer):
    LESSONS.append(locals())


add("composition-over-inheritance", "组合优于继承", "🧩",
    "把可变能力放进对象引用，别为每种搭配造一个子类。",
    "当两个功能维度会独立变化、子类名称开始拼接多个形容词时，先考虑组合。",
    "通知有普通/加急两种规则，发送渠道有邮件/短信两种。继承容易做成四个子类；以后再加推送渠道与定时发送，组合数继续增长。",
    "class UrgentEmailNotice ...\nclass UrgentSmsNotice ...\nclass NormalEmailNotice ...\nclass NormalSmsNotice ...\n// 新增渠道 × 新增规则，子类数不断相乘",
    "把消息规则和发送渠道分成两种职责；Notice 持有 Channel 接口。运行时选择搭配即可。",
    "调用方|Notice 规则|Channel 接口|具体渠道",
    "识别维度^列出消息规则与投递渠道两个变化轴。^0,1|抽出契约^Channel 只承诺 send(text)，Rule 只负责格式化。^1,2|注入能力^Notice 构造时接收规则与渠道。^1,2,3|自由搭配^新增 PushChannel 不修改 Notice 或现有规则。^0,1,3",
    "切换组合，观察新增能力时需要改哪些类。",
    "加急短信^Notice(UrgentRule)>Channel.send>SmsChannel>短信发出^规则与渠道分别组合。^无需 UrgentSmsNotice 这种组合子类。|普通邮件^Notice(NormalRule)>Channel.send>EmailChannel>邮件发出^同一接口让普通与加急规则复用邮件能力。^调用方在组装处选择搭配。|新增推送^Notice(UrgentRule)>Channel.send>PushChannel>推送发出^只新增一个渠道实现。^变化局限在渠道维度，不触碰已有消息规则。",
    "interface Channel { send(text) }\ninterface Rule { format(text) }\nclass Notice {\n  constructor(rule: Rule, channel: Channel) {\n    this.rule = rule; this.channel = channel\n  }\n  send(text) { this.channel.send(this.rule.format(text)) }\n}\nnotice = Notice(UrgentRule(), SmsChannel())",
    "找出独立变化轴，而不是看到继承就一律重写。|抽象只表达稳定契约，不把 Email 的专有参数塞进 Channel。|在组装处选择实现；业务流程只依赖接口。",
    "桥接^../../03-structural/02-bridge/bridge-pattern.html^两个独立维度由组合连接|策略^../../04-behavioral/09-strategy/strategy-pattern.html^注入可替换算法|装饰器^../../03-structural/04-decorator/decorator-pattern.html^组合叠加可选职责",
    "继承不是错误：稳定的 is-a 关系、共享不变量和模板流程仍可用继承。问题是用继承表示“可以自由拼装的能力”。",
    "加急通知和短信渠道都可能增加新类型，为什么不要建立 UrgentSmsNotice？",
    "两个维度的组合会成倍扩张；让 UrgentNotice 持有 Channel，可分别新增消息规则或渠道。")

add("dependency-inversion-and-injection", "依赖倒置与依赖注入", "🔌",
    "高层业务定义自己需要的能力，外部实现来满足这个契约。",
    "当业务服务直接 new 数据库、支付或第三方 SDK，导致切换供应商和单元测试都要修改业务代码。",
    "订单服务直接构造某支付 SDK，并到处使用 SDK 专有请求与错误码。测试订单规则也必须连真实支付沙箱。",
    "class CheckoutService {\n  pay(order) {\n    client = new StripeSdk(secret)\n    return client.createCharge({amount_cents: order.total})\n  }\n}",
    "先由业务定义 PaymentPort.charge(amount)。支付供应商的适配器实现它；构造器只接收这个契约。",
    "业务服务|业务端口|真实适配器|测试替身",
    "定义需求^Checkout 只需要 charge(amount) 和明确失败语义。^0,1|实现端口^StripeAdapter 把业务金额映射为 SDK 字段。^1,2|注入实现^组装处把真实适配器传给 Checkout。^0,2|替换测试^单元测试注入 FakePayment，不访问网络。^0,3",
    "业务逻辑保持相同，换一个实现对象后会怎样？",
    "真实支付^Checkout>PaymentPort>StripeAdapter>支付渠道^订单服务不包含 SDK 字段。^变化停留在边界适配器。|切换供应商^Checkout>PaymentPort>AnotherAdapter>新渠道^订单流程与接口契约不变。^新的实现遵守同一业务语义。|单元测试^Checkout>PaymentPort>FakePayment>可断言调用^测试无需真实支付网络。^依赖关系显式，替换能力来自构造注入。",
    "interface PaymentPort { charge(amount): Receipt }\nclass CheckoutService {\n  constructor(payment: PaymentPort) { this.payment = payment }\n  pay(order) {\n    order.ensurePayable()\n    return this.payment.charge(order.total)\n  }\n}\nclass StripeAdapter implements PaymentPort {\n  charge(amount) { return mapReceipt(stripe.charge(toCents(amount))) }\n}",
    "DIP 是依赖方向：业务不依赖具体 SDK。|DI 是传入依赖的做法，不要求引入容器框架。|端口由业务需要定义，别照搬第三方 SDK 的全部方法。",
    "适配器^../../03-structural/01-adapter/adapter-pattern.html^把外部接口翻译成业务契约|工厂方法^../../02-creational/02-factory-method/factory-method-pattern.html^创建具体实现但消费端只见接口|代理^../../03-structural/07-proxy/proxy-pattern.html^保持接口并控制访问",
    "不是每个类都需要接口。只有真实的替换边界、外部依赖或测试隔离需求，才值得引入抽象。",
    "依赖注入和依赖倒置是一回事吗？",
    "不是。依赖倒置规定高层依赖抽象；依赖注入是把依赖从外部传入的一种实现手段。")

add("cohesion-coupling-and-demeter", "高内聚、低耦合与最少知识", "🧭",
    "一个模块做好自己的事，调用方别穿透别人的内部结构。",
    "当改一个字段名就要改许多服务，或一个类同时管业务、数据库、展示与日志，边界通常放错了。",
    "结账逻辑读取 customer.profile.address.city.code，再据此选运费；客户对象内部层级稍一变化，订单代码就会被迫修改。",
    "if customer.profile.address.city.code == \"SH\":\n  fee = 8\n// 结账代码知道客户内部四层结构",
    "让拥有数据和规则的一方提供稳定行为，或在明确的业务边界放一个专门的策略/服务。",
    "结账服务|客户对象|配送规则|外部数据",
    "定位职责^结账只需要“能否配送、运费多少”。^0|封装内部^客户对象或配送规则提供业务方法。^1,2|调用契约^结账不再逐层读取内部字段。^0,1,2|替换细节^地址模型变更时，结账流程不变。^1,3",
    "试试改变内部数据结构，看看改动会不会扩散。",
    "链式穿透^Checkout>profile>address>city.code^内部字段改名，调用方也要修改。^调用方知道太多无关细节。|封装业务问题^Checkout>ShippingPolicy.quote(customer)^策略内部读取必要数据，返回运费。^调用方只说自己需要什么。|更换地址来源^Checkout>ShippingPolicy>新地址提供者^结账服务保持不变。^高内聚让同一规则集中，低耦合限制变化传播。",
    "class ShippingPolicy {\n  quote(customer, order) {\n    region = customer.shippingRegion()\n    return rateTable.lookup(region, order.weight)\n  }\n}\nclass Checkout {\n  total(customer, order) {\n    return order.subtotal + shippingPolicy.quote(customer, order)\n  }\n}",
    "高内聚：同一变化原因的规则集中在合适模块。|低耦合：调用方只依赖必要的公开契约。|迪米特法则不是禁止所有点号；DTO 与不可变值对象的读取可能合理。",
    "外观^../../03-structural/05-facade/facade-pattern.html^用高层入口缩小客户端知识范围|中介者^../../04-behavioral/05-mediator/mediator-pattern.html^减少对象间网状依赖|组合^../../03-structural/03-composite/composite-pattern.html^对树形结构提供统一操作",
    "别把所有逻辑都搬进一个巨型 Customer 类；规则属于哪个业务概念，就放在那里。封装应减少变化扩散，不是藏起所有数据。",
    "customer.address.city.name 这样的访问一定违反迪米特法则吗？",
    "不一定。若只是读取稳定的不可变 DTO，没有暴露行为耦合，未必需要包装；重点看内部变化是否迫使调用方修改。")

add("substitutability-and-small-interfaces", "可替换性与小接口", "🧱",
    "子类守住父类承诺；接口只包含使用者真正需要的能力。",
    "当实现类只能靠抛 UnsupportedOperation 满足接口，或替换某实现后调用方行为被破坏时。",
    "一个 Bird 接口同时要求 fly、layEgg。企鹅无法飞，蝙蝠不会下蛋；硬实现只会制造异常和无意义方法。",
    "interface Bird { fly(); layEgg() }\nclass Penguin implements Bird {\n  fly() { throw UnsupportedOperation }\n  layEgg() { ... }\n}",
    "拆出 Flyable、EggLayer 等小契约；只让真正具备能力的对象实现。调用方依赖它所需的小接口。",
    "调用方|小接口|能飞的实现|不会飞的实现",
    "发现违约^Penguin.fly() 抛错，无法替换“能飞的 Bird”。^0,3|拆小契约^把 fly 从笼统 Bird 接口拆为 Flyable。^1|按能力实现^Sparrow 实现 Flyable，Penguin 不实现。^2,3|安全调用^需要飞行的代码只接收 Flyable。^0,1,2",
    "选择不同对象，观察“接口声明”和“实际行为”是否一致。",
    "错误大接口^飞行调用方>Bird.fly>Penguin 抛错^替换实现后功能被破坏。^违反里氏替换，也暴露接口过宽。|小接口匹配^飞行调用方>Flyable>麻雀.fly^所有接受的实现都能飞。^客户端不依赖它不需要的方法。|企鹅入队^动物展示>Bird 基础能力>企鹅展示^企鹅只参与自己能履行的契约。^不让不具备飞行能力的类型承担飞行承诺。",
    "interface Flyable { fly() }\ninterface EggLayer { layEgg() }\nclass Sparrow implements Flyable, EggLayer { ... }\nclass Penguin implements EggLayer { ... }\nfunction startFlight(actor: Flyable) { actor.fly() }\n// Penguin 不能被传给 startFlight，错误在边界暴露。",
    "LSP 关注可替换后的行为承诺，不只是类型检查通过。|ISP 关注客户端只依赖所需方法。|契约测试应验证返回值、异常、副作用与顺序约束。",
    "策略^../../04-behavioral/09-strategy/strategy-pattern.html^每种算法实现必须守住相同结果语义|装饰器^../../03-structural/04-decorator/decorator-pattern.html^包装层应保持原接口的行为承诺|代理^../../03-structural/07-proxy/proxy-pattern.html^控制访问仍需让客户端理解失败语义",
    "接口越小并非越好；拆分应由使用者的不同需求驱动。不要把一个稳定契约机械拆成几十个单方法接口。",
    "实现了同一个接口，就一定满足里氏替换吗？",
    "不一定。若某实现抛出接口未约定的异常、收紧前置条件或改变结果语义，类型相同也不能安全替换。")

add("simplicity-dry-yagni", "DRY、KISS 与 YAGNI：克制抽象", "✂️",
    "设计模式解决已经出现的变化压力；抽象的成本也是真实成本。",
    "当团队为“以后也许会有”先建十层接口，或把只是长得像的两段业务强行合并。",
    "两个报表导出函数各有三行相似代码，但业务规则不同。为去掉重复，团队做了一个带十几个布尔开关的通用 ExportEngine；任何改动都要理解所有开关组合。",
    "export(type, isPdf, hasWatermark, isMonthly, useLegacy,\n       skipAudit, enableCache, ...)  // “通用”成了组合地狱",
    "先让代码简单、语义清楚；只有同一知识被多个地方重复维护时，再抽出稳定的共同点。",
    "需求证据|简单实现|真实重复|合适抽象",
    "先满足当前^一两个已知需求先直接写清楚。^0,1|观察变化^记录哪些代码因同一个原因一起改。^0,2|判断是否共享^相似外形不等于相同业务知识。^2|引入抽象^抽出稳定共同点，保留不同规则。^1,3",
    "切换三种演化阶段，看看什么时候抽象真正省事。",
    "只有一个格式^当前需求>清楚函数>完成^没有必要提前搭建插件框架。^YAGNI：不为想象的未来付费。|两个相似但不同规则^分别实现>观察变化原因>保持分离^两段代码长得像，但独立变化。^DRY 避免重复知识，不要求合并所有相似文本。|第三种同规则出现^三个实现>提取稳定契约>复用核心^抽象有了足够样本。^KISS 约束抽象仍应容易理解。",
    "function exportPdf(data) { validatePdf(data); renderPdf(data) }\nfunction exportCsv(data) { validateCsv(data); renderCsv(data) }\n// 先保留独立语义。若共同审计规则重复出现：\nfunction withAudit(exporter, data) {\n  audit.start(data)\n  return exporter(data)\n}",
    "DRY 指不要多处维护同一条知识。|KISS 要求当前设计尽量容易理解。|YAGNI 要求不为尚未证实的需求预付复杂度。",
    "工厂方法^../../02-creational/02-factory-method/factory-method-pattern.html^产品种类真的扩展时再引入|策略^../../04-behavioral/09-strategy/strategy-pattern.html^算法真的需要互换时再抽出|建造者^../../02-creational/04-builder/builder-pattern.html^参数复杂到影响可读性时再使用",
    "“重复三次再抽象”只是启发式，不是硬规则。安全修复或核心业务不变量即使只重复两处，也可能值得统一。",
    "两段代码看起来一样，就应该立刻抽成一个函数吗？",
    "不一定。先看它们是否表达同一知识、是否因同一原因变化；只看文本相似容易得到错误抽象。")


def render(item):
    e = escape
    role_html = ''.join(f'<div class="pattern-role" data-pattern-role>{e(role)}</div>'
                        for role in item["roles"].split("|"))
    steps = []
    for i, raw in enumerate(item["steps"].split("|")):
        label, detail, active = raw.split("^")
        steps.append(f'<button type="button" data-pattern-step aria-pressed="false" '
                     f'data-title="{e(label, quote=True)}" data-detail="{e(detail, quote=True)}" '
                     f'data-active="{e(active)}">{i + 1}. {e(label)}</button>')
    options = []
    for raw in item["options"].split("|"):
        label, route, result, why = raw.split("^")
        options.append(f'<button type="button" data-lab-option aria-pressed="false" '
                       f'data-route="{e(route, quote=True)}" data-result="{e(result, quote=True)}" '
                       f'data-why="{e(why, quote=True)}">{e(label)}</button>')
    takeaways = ''.join(f'<li>{e(x)}</li>' for x in item["takeaways"].split("|"))
    related = []
    for raw in item["related"].split("|"):
        name, href, why = raw.split("^")
        related.append(f'<li><a href="{href}">{e(name)}</a>：{e(why)}</li>')
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(item["lead"], quote=True)}">
<title>{e(item["title"])}：设计原则图解 - Visuals</title>
<link rel="stylesheet" href="../../../../assets/pattern-lesson.css"></head>
<body class="pattern-page"><main class="pattern-shell">
<a class="pattern-back" href="../../index.html">← 返回设计模式目录</a>
<header class="pattern-hero"><span class="pattern-kicker">DESIGN PRINCIPLES · 从原则到模式</span>
<h1>{item["icon"]} {e(item["title"])}</h1><p class="pattern-lead">{e(item["lead"])}</p>
<div class="pattern-tldr"><strong>判断信号</strong><span>{e(item["signal"])}</span></div></header>
<nav class="pattern-toc" aria-label="本页目录"><a href="#problem">问题</a><a href="#flow">角色协作</a><a href="#lab">改变条件</a><a href="#code">伪代码</a><a href="#use">落地边界</a></nav>
<section class="pattern-panel" id="problem"><span class="pattern-eyebrow">01 · 原则从问题里长出来</span><h2>直接写会有什么代价？</h2>
<p>{e(item["story"])}</p><div class="pattern-before-after"><div class="pattern-before"><h3>先看问题写法</h3>
<pre class="pattern-code"><code>{e(item["naive"])}</code></pre></div><div class="pattern-after"><h3>关键转折</h3>
<p class="pattern-highlight">{e(item["turn"])}</p></div></div></section>
<section class="pattern-lesson" id="flow" data-pattern-lesson><span class="pattern-eyebrow">02 · 点一步，看依赖和职责</span>
<h2>角色怎样重新分工？</h2><div class="pattern-roles">{role_html}</div>
<div class="pattern-controls" role="group" aria-label="讲解步骤">{''.join(steps)}
<button type="button" class="pattern-play" data-pattern-play aria-pressed="false">▶ 自动播放</button></div>
<div class="pattern-scene" aria-live="polite"><h3 data-scene-title></h3><p data-scene-detail></p></div>
<div class="pattern-progress" aria-hidden="true"><span data-pattern-progress></span></div></section>
<section class="pattern-panel" id="lab"><span class="pattern-eyebrow">03 · 让变化真的发生</span><h2>三种输入，三条执行路径</h2>
<p>{e(item["lab_intro"])}</p><div class="pattern-lab" data-pattern-lab>
<div class="pattern-lab-options" role="group" aria-label="选择实验条件">{''.join(options)}</div>
<div class="pattern-lab-stage"><div class="pattern-lab-route" data-lab-route aria-label="执行路径"></div>
<div class="pattern-lab-result"><strong>得到的结果</strong><p data-lab-result></p></div>
<p class="pattern-lab-why" data-lab-why></p></div></div></section>
<section class="pattern-panel" id="code"><span class="pattern-eyebrow">04 · 把原则写进代码</span><h2>最小伪代码</h2>
<pre class="pattern-code"><code>{e(item["code"])}</code></pre><div class="pattern-code-notes"><h3>从代码中带走三件事</h3><ol>{takeaways}</ol></div></section>
<section class="pattern-panel" id="use"><span class="pattern-eyebrow">05 · 原则不是教条</span><h2>对应哪些模式？什么时候收手？</h2>
<ul class="pattern-list">{''.join(related)}</ul><p class="pattern-highlight">{e(item["caution"])}</p>
<details class="pattern-quiz"><summary>{e(item["question"])}</summary><p>{e(item["answer"])}</p></details></section>
<nav class="pattern-neighbors"><a href="design-principles.html">SOLID 与基础原则总览</a>
<a href="../01-patterns-intro/all-patterns-at-a-glance.html">23 个模式速查</a></nav>
<footer class="pattern-footer">© 2026 Visuals · 设计原则专题</footer></main>
<script src="../../../../assets/pattern-lesson.js"></script></body></html>'''


def main():
    for item in LESSONS:
        path = OUT / (item["slug"] + ".html")
        path.write_text(render(item), encoding="utf-8")
    print(f"Generated {len(LESSONS)} principle lessons")


if __name__ == "__main__":
    main()
