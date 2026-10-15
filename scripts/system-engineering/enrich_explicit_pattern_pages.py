"""Add concrete simulations and pseudocode to cache/retry pattern articles."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2] / "system-engineering"
LESSONS = []
DECISIONS = {
    "cache-patterns": {
        "signal": "读多写少、数据库查询昂贵，而且业务能明确接受多长时间的旧值；先确定谁负责回源与写库。",
        "scenarios": [
            "商品详情页的热点商品：应用用 Cache-Aside 缓解数据库读压力，并在改价后删缓存。",
            "多应用共用同一缓存代理：用 Read-Through 集中处理未命中加载，减少每个应用重复写回源逻辑。",
            "计数或遥测写入量大且允许延后落库：用 Write-Behind 批量刷库，配可靠队列和恢复流程。",
        ],
        "comparisons": [
            ("Cache-Aside 与 Read-Through", "前者由应用回源并回填；后者由缓存层在未命中时加载。两者都描述读路径。"),
            ("Write-Through 与 Write-Behind", "前者写库完成后确认；后者先确认、后刷库。后者吞吐较高，但必须承担持久化与故障恢复。"),
        ],
    },
    "cache-aside-detail": {
        "signal": "应用能控制缓存与数据库两端，并接受写后短暂旧值窗口。",
        "scenarios": [
            "商品资料大量读取，编辑相对少：未命中时从数据库加载，并设置合理 TTL。",
            "订单摘要读取频繁：更新数据库后删除对应缓存键，下次读取重新构建。",
            "已有数据库访问层的服务逐步加缓存：只为被测量证明是热点的查询加回填。",
        ],
        "comparisons": [
            ("Read-Through", "缓存代理负责加载数据库；Cache-Aside 的应用必须写未命中、回填和失效逻辑。"),
            ("Write-Through", "Write-Through 的缓存层同步完成写库；Cache-Aside 的应用先提交数据库，再删旧缓存。"),
        ],
    },
    "read-write-through": {
        "signal": "希望应用只面对缓存接口；缓存代理有能力可靠地访问权威数据库。",
        "scenarios": [
            "多服务访问同一商品数据：Read-Through 代理统一处理未命中加载。",
            "库存写入需要同步确认权威数据：Write-Through 等数据库提交后才返回成功。",
            "日志聚合写入量大、允许秒级延后：Write-Behind 先可靠入队，再批量刷库。",
        ],
        "comparisons": [
            ("Read-Through 与 Cache-Aside", "读未命中时，前者由缓存代理查询数据库；后者由业务应用查询并回填。"),
            ("Write-Through 与 Write-Behind", "前者成功通常意味着同步写库已完成；后者成功只代表写入可靠待刷记录，数据库可能仍是旧值。"),
        ],
    },
    "retry-idempotency": {
        "signal": "请求或消息可能在已产生副作用后丢失响应，调用方会再次发起同一业务操作。",
        "scenarios": [
            "支付超时后重试扣款：复用同一业务幂等键，返回首次扣款结果。",
            "消息队列重复投递积分事件：消费端按事件 ID 记录处理结果，避免重复加分。",
            "创建订单的客户端网络中断：重试时复用请求键，避免生成两个订单。",
        ],
        "comparisons": [
            ("重试与幂等", "重试处理瞬时故障以提高成功率；幂等约束重复请求的副作用。通常需要一起设计。"),
            ("去重与幂等", "去重只识别重复输入；幂等还需处理处理中状态、保存并返回首次结果，以及崩溃后的恢复。"),
        ],
    },
}


def add(path, hook, roles, steps, intro, options, code, edge):
    LESSONS.append(locals())


add("cache-system/04-consistency/01-cache-patterns/cache-patterns.html",
    "同样是“读写缓存”，真正不同的是：谁负责访问数据库，以及什么时候写数据库。",
    "应用|缓存层|数据库|异步刷盘",
    "发起操作^应用读取或更新一个商品。^0|确定责任^Cache-Aside 由应用管回源；Through 由缓存层管。^0,1|同步或异步^Write-Through 同步写库，Write-Behind 稍后刷盘。^1,2,3|选择代价^比较延迟、一致性和故障恢复。^0,1,2,3",
    "点击同一商品请求的三种路径，观察“谁知道数据库”与“什么时候可以返回”。",
    "Cache-Aside 未命中^应用查缓存>未命中>应用查 DB>应用回填缓存^数据由应用加载并回填。^实现简单，但应用必须管理失效和并发窗口。|Write-Through 写入^应用写缓存层>缓存层同步写 DB>成功返回^数据库写成功后才确认写入。^写延迟包含数据库耗时，失败语义由缓存层实现。|Write-Behind 写入^应用写缓存层>确认返回>后台批量刷 DB^用户先收到成功，数据库稍后更新。^缓存/队列崩溃时有丢失窗口，需持久化与恢复。",
    "function readAside(key):\n  value = cache.get(key)\n  if value == MISS:\n    value = db.get(key)\n    cache.set(key, value, ttl)\n  return value\n\nfunction writeAside(key, value):\n  db.update(key, value)\n  cache.delete(key)\n\n// Through/Behind 的 DB 访问位于缓存层实现中。",
    "选型关键：Cache-Aside 简单但并非强一致；Through 依赖缓存层的读写代理能力；Write-Behind 用延迟和丢失风险换写吞吐。")

add("cache-system/04-consistency/01-cache-patterns/cache-aside-detail.html",
    "读时“先查缓存，未命中再回源”；写时“先写数据库，再删缓存”。并发时仍可能短暂读到旧值。",
    "读请求|缓存|数据库|写请求",
    "读缓存^读请求先尝试 cache.get。^0,1|未命中回源^缓存未命中时查询数据库。^0,2|写入更新^写请求先提交数据库，再删除旧缓存。^3,2,1|并发窗口^旧读请求可能在删缓存后回填旧值。^0,1,2,3",
    "切换命中、未命中和并发时序。第三种不是“删缓存失败”，而是读写交错。",
    "缓存命中^读请求>缓存命中>直接返回^不访问数据库。^热门数据读延迟低。|缓存未命中^读请求>缓存未命中>数据库查询>回填缓存>返回^下次读取可命中。^要设 TTL 并防止大量请求同时回源。|并发脏回填^读 A 查到旧 DB>写 B 更新 DB 并删缓存>读 A 回填旧值^缓存暂时保存旧数据。^写后删缓存只能缩小窗口，不能单独保证强一致。",
    "function read(key):\n  cached = cache.get(key)\n  if cached != MISS: return cached\n  value = db.get(key)\n  cache.set(key, value, ttl)\n  return value\n\nfunction write(key, value):\n  db.update(key, value)   // 先提交权威数据\n  cache.delete(key)      // 再使旧缓存失效",
    "需要更严格新鲜度时，可用版本号、条件回填或串行化关键路径；延迟双删只缓解特定时序，不提供强一致保证。")

add("cache-system/04-consistency/01-cache-patterns/read-write-through.html",
    "Read-Through 管“未命中时谁加载”；Write-Through 与 Write-Behind 管“写入何时落库”。这不是同一个维度。",
    "应用|缓存代理|数据库|异步队列",
    "读取数据^应用只向缓存代理请求数据。^0,1|缓存未命中^Read-Through 代理自己去数据库加载。^1,2|同步写入^Write-Through 等数据库写成功才确认。^1,2|异步写入^Write-Behind 先入持久队列，稍后刷库。^1,3,2",
    "比较同步确认和异步确认；尤其注意成功响应究竟意味着数据在哪里。",
    "Read-Through 未命中^应用>缓存代理>数据库加载>回填缓存^应用不写回源代码。^读穿透描述的是读路径。|Write-Through^应用写代理>同步写 DB>写缓存>确认成功^确认通常意味着数据库与缓存层都已按契约更新。^延迟受数据库写入影响。|Write-Behind^应用写代理>可靠队列/缓存>先确认>异步刷 DB^吞吐高，但 DB 仍可能是旧值。^若未持久化待刷记录，进程崩溃会丢写入。",
    "function readThrough(key):\n  return cache.getOrLoad(key, loader=db.get)\n\nfunction writeThrough(key, value):\n  db.update(key, value)\n  cache.set(key, value)\n  return ACK\n\nfunction writeBehind(key, value):\n  durableQueue.append(key, value)\n  cache.set(key, value)\n  return ACK  // 后台重试刷库，需顺序和去重",
    "Read-Through 可与不同写策略组合；Write-Behind 必须设计队列持久化、顺序、重试、回放与故障恢复。")

add("distributed-system/07-resilience/01-reliability-patterns/retry-idempotency.html",
    "超时不等于失败：第一次扣款可能已成功，只是回包丢了。重试必须带同一个幂等键。",
    "调用方|网络|支付服务|幂等记录",
    "首次发起^调用方生成业务请求唯一键 K。^0|遇到超时^网络丢失响应，调用方不知道扣款是否成功。^1|带键重试^调用方复用 K，服务端查幂等记录。^0,2,3|返回结果^若 K 已完成，返回首次结果，不再扣款。^2,3",
    "同一笔支付尝试三种时序，观察重试和幂等如何配合。",
    "首次成功^请求 K>服务端占位 K>扣款>保存结果>返回成功^执行一次副作用。^键应绑定业务操作而非每次网络尝试。|响应丢失^首次扣款成功>响应丢失>重试 K>命中已有结果^第二次请求返回同一结果，不再次扣款。^超时后不能简单推断首次失败。|服务端忙^重试 K>处理中记录>等待/稍后重试^不并发执行第二次扣款。^退避、抖动和重试预算防止雪崩。",
    "function charge(request):\n  key = request.idempotencyKey\n  created, record = store.insertIfAbsent(key, PROCESSING)\n  if not created:\n    if record.done: return record.savedResult\n    return RetryLater\n  result = payment.chargeOnce(request)\n  store.complete(key, result)\n  return result\n\n// 调用方重试始终复用 key，并设置次数/退避上限。",
    "幂等记录与真实扣款之间还有崩溃窗口；生产系统要用事务、支付渠道查询、对账与恢复流程闭合这段窗口。")


def render(item):
    e = escape
    decision = DECISIONS[Path(item["path"]).stem]
    scenarios = ''.join(f'<li>{e(scenario)}</li>' for scenario in decision["scenarios"])
    comparisons = ''.join(
        f'<tr><th scope="row">{e(name)}</th><td>{e(difference)}</td></tr>'
        for name, difference in decision["comparisons"]
    )
    steps = []
    for index, raw in enumerate(item["steps"].split("|")):
        label, detail, active = raw.split("^")
        steps.append(f'<button type="button" data-pattern-step aria-pressed="false" '
                     f'data-title="{e(label, quote=True)}" data-detail="{e(detail, quote=True)}" '
                     f'data-active="{e(active)}">{index + 1}. {e(label)}</button>')
    roles = ''.join(f'<div class="pattern-role" data-pattern-role>{e(role)}</div>'
                    for role in item["roles"].split("|"))
    options = []
    for raw in item["options"].split("|"):
        label, route, result, why = raw.split("^")
        options.append(f'<button type="button" data-lab-option aria-pressed="false" '
                       f'data-route="{e(route, quote=True)}" '
                       f'data-result="{e(result, quote=True)}" '
                       f'data-why="{e(why, quote=True)}">{e(label)}</button>')
    return f'''<!-- explicit pattern lesson start -->
<section class="pattern-lesson" data-pattern-lesson aria-label="模式动态讲解">
  <span class="pattern-eyebrow">图解 · 交互 · 伪代码</span>
  <h2>先看一次完整的调用</h2>
  <p class="pattern-highlight">{e(item["hook"])}</p>
  <div class="pattern-roles">{roles}</div>
  <div class="pattern-controls" role="group" aria-label="过程步骤">
    {''.join(steps)}
    <button type="button" class="pattern-play" data-pattern-play aria-pressed="false">▶ 自动播放</button>
  </div>
  <div class="pattern-scene" aria-live="polite"><h3 data-scene-title></h3><p data-scene-detail></p></div>
  <div class="pattern-progress" aria-hidden="true"><span data-pattern-progress></span></div>
  <h3 style="margin-top:26px">改变条件，看执行路径</h3>
  <p>{e(item["intro"])}</p>
  <div class="pattern-lab" data-pattern-lab>
    <div class="pattern-lab-options" role="group" aria-label="选择实验条件">{''.join(options)}</div>
    <div class="pattern-lab-stage">
      <div class="pattern-lab-route" data-lab-route aria-label="执行路径"></div>
      <div class="pattern-lab-result"><strong>得到的结果</strong><p data-lab-result></p></div>
      <p class="pattern-lab-why" data-lab-why></p>
    </div>
  </div>
  <div class="pattern-decision">
    <h3>什么时候适用？</h3>
    <p class="pattern-decision-signal"><strong>判断信号：</strong>{e(decision["signal"])}</p>
    <ul class="pattern-list">{scenarios}</ul>
    <h3>和相近模式怎么区分？</h3>
    <div class="pattern-table-wrap"><table class="pattern-table">
      <thead><tr><th scope="col">相近方案</th><th scope="col">选择边界</th></tr></thead>
      <tbody>{comparisons}</tbody>
    </table></div>
  </div>
  <h3 style="margin-top:26px">核心伪代码</h3>
  <pre class="pattern-code"><code>{e(item["code"])}</code></pre>
  <p>{e(item["edge"])}</p>
</section>
<!-- explicit pattern lesson end -->
'''


def main():
    assert {Path(item["path"]).stem for item in LESSONS} == set(DECISIONS)
    for item in LESSONS:
        page = ROOT / item["path"]
        html = page.read_text(encoding="utf-8")
        html = re.sub(r'<!-- explicit pattern lesson start -->.*?<!-- explicit pattern lesson end -->\s*',
                      '', html, flags=re.S)
        if 'assets/pattern-lesson.css' not in html:
            html = html.replace('</head>', '<link rel="stylesheet" href="../../../../assets/pattern-lesson.css">\n</head>', 1)
        if 'assets/pattern-lesson.js' not in html:
            html = html.replace('</body>', '<script src="../../../../assets/pattern-lesson.js"></script>\n</body>', 1)
        if 'retry-idempotency.html' in item["path"]:
            html = html.replace('<main>', '<main>\n' + render(item), 1)
        else:
            html = re.sub(r'(<div class="hero">.*?</div>)', lambda m: m.group(1) + '\n' + render(item),
                          html, count=1, flags=re.S)
        page.write_text(html, encoding="utf-8")
    print(f"Enriched {len(LESSONS)} explicit pattern pages")


if __name__ == "__main__":
    main()
