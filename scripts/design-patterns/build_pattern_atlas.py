"""Build the searchable 23-pattern atlas from the same data as individual lessons."""
from html import escape
import json
from pathlib import Path

from build_pattern_lessons import PAGES
from pattern_atlas_data import ATLAS

ROOT = Path(__file__).resolve().parents[2] / "programming-and-programs/design-patterns"
OUT = ROOT / "01-overview/01-patterns-intro/all-patterns-at-a-glance.html"
LABELS = {
    "02-creational": ("创建型", "对象怎样被创建"),
    "03-structural": ("结构型", "对象怎样被组合"),
    "04-behavioral": ("行为型", "对象怎样协作"),
}
PAIRS = [
    ("factory-method", "abstract-factory", "只创建一种可替换产品，还是要保证一整族产品配套？", "工厂方法把一种产品的创建留给具体创建者；抽象工厂一次约束多个相关产品。"),
    ("abstract-factory", "builder", "结果是一整套对象，还是一个对象逐步组装？", "抽象工厂生产配套产品族；建造者分步骤交付一个完整对象。"),
    ("builder", "prototype", "手上已有可复制的样板吗？", "建造者从配置步骤组装；原型复制现有对象并修改差异。"),
    ("prototype", "flyweight", "要独立副本，还是共享不变部分？", "原型复制可变状态；享元按 key 共享不可变状态以节约内存。"),
    ("adapter", "facade", "是接口不兼容，还是子系统太难用？", "适配器翻译接口；外观为多个子系统提供高层入口。"),
    ("adapter", "decorator", "需要翻译接口，还是保留接口叠加功能？", "适配器改变接口形状；装饰器保持接口并逐层附加行为。"),
    ("decorator", "proxy", "主要是增加职责，还是控制真实对象的访问？", "装饰器可自由叠加功能；代理重点在鉴权、延迟加载或远程访问。"),
    ("bridge", "strategy", "是否存在两个独立变化维度？", "桥接分离两个可扩展层次；策略通常替换一个算法维度。"),
    ("composite", "decorator", "节点拥有多个孩子，还是一层包住一个对象？", "组合表达树的部分与整体；装饰器形成单对象包装链。"),
    ("chain-of-responsibility", "decorator", "请求可能在中途停止吗？", "责任链沿处理器传播并允许短路；装饰器为一个对象叠加职责。"),
    ("observer", "mediator", "只发布变化，还是集中制定参与者互动规则？", "观察者让订阅者各自响应；中介者协调多个对象的交互。"),
    ("state", "strategy", "变化来自内部状态迁移，还是外部主动选算法？", "状态封装生命周期中的行为；策略封装可互换的算法。"),
    ("command", "memento", "要保存操作，还是保存状态？", "命令保存可执行操作及可能的逆操作；备忘录保存一个时刻的快照。"),
    ("template-method", "strategy", "固定流程的少数步骤变化，还是整个算法可互换？", "模板方法用继承固定骨架；策略用组合切换算法。"),
    ("iterator", "visitor", "要解决怎么走到每个节点，还是对节点做什么？", "迭代器控制遍历；访问者分离作用于不同节点类型的操作。"),
]


def catalog():
    items = [{
        "slug": "singleton", "category": "02-creational", "directory": "01-singleton",
        "name": "单例", "icon": "🔒", "line": "限制同一进程内某类对象至多一个",
        "href": "../../02-creational/01-singleton/singleton-pattern.html",
    }]
    for page in PAGES:
        slug = page["directory"][3:]
        items.append({
            "slug": slug, "category": page["category"], "directory": page["directory"],
            "name": page["name"], "icon": page["icon"], "line": page["line"],
            "href": f'../../{page["category"]}/{page["directory"]}/{slug}-pattern.html',
        })
    items.sort(key=lambda item: (item["category"], item["directory"]))
    assert len(items) == 23 and {item["slug"] for item in items} == set(ATLAS)
    for item in items:
        item.update(ATLAS[item["slug"]])
        item["categoryLabel"] = LABELS[item["category"]][0]
    return items


def main():
    items = catalog()
    by_slug = {item["slug"]: item for item in items}
    rows = []
    for item in items:
        e = escape
        rows.append(
            f'<tr data-category="{item["category"]}" data-search="{e(" ".join([item["name"], item["line"], item["signal"], *item["scenarios"], item["nearest"]]), quote=True)}">'
            f'<th scope="row"><a href="{item["href"]}"><span class="mode-icon">{item["icon"]}</span>{e(item["name"])}</a>'
            f'<small>{e(item["categoryLabel"])}</small></th>'
            f'<td>{e(item["signal"])}</td><td>{e(item["scenarios"][0])}</td>'
            f'<td>{e(item["avoid"])}</td><td>{e(item["nearest"])}</td>'
            f'<td><button type="button" data-pick="{item["slug"]}" aria-pressed="false">加入对比</button></td></tr>'
        )
    pair_rows = []
    for left, right, question, answer in PAIRS:
        a, b = by_slug[left], by_slug[right]
        pair_rows.append(
            f'<tr><th scope="row"><a href="{a["href"]}">{escape(a["name"])}</a> ↔ '
            f'<a href="{b["href"]}">{escape(b["name"])}</a></th>'
            f'<td>{escape(question)}</td><td>{escape(answer)}</td></tr>'
        )
    data = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    template = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="23 个经典设计模式的适用场景、相似模式区别与交互对比速查表">
<title>23 个设计模式速查与对比 - Visuals</title>
<style>
:root{--bg:#0c1625;--panel:#16283b;--line:#38546b;--text:#edf5fc;--muted:#b5c8d8;--mint:#7ee0cc;--gold:#ffd17d;--blue:#90c5ff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 80% 0,#1d4960 0,transparent 28%),var(--bg);color:var(--text);font:16px/1.65 system-ui,-apple-system,"PingFang SC",sans-serif}
a{color:var(--mint)}button,input{font:inherit}button{cursor:pointer}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.shell{width:min(1320px,calc(100% - 32px));margin:auto;padding:22px 0 70px}.back{display:inline-block;margin:8px 0 22px}.hero{padding:20px 0 14px}.eyebrow{color:var(--mint);font-size:.82rem;letter-spacing:.1em;font-weight:800}.hero h1{font-size:clamp(2.2rem,5vw,3.7rem);line-height:1.16;margin:8px 0}.hero p{max-width:850px;color:var(--muted);font-size:1.13rem}.lead-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:22px 0 30px}.lead-grid a{display:block;background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:18px;text-decoration:none;color:var(--text)}.lead-grid strong{display:block;color:var(--mint);font-size:1.08rem}.lead-grid span{color:var(--muted);font-size:.9rem}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:clamp(17px,2.8vw,27px);margin:25px 0}.panel h2{font-size:1.4rem;margin:0 0 8px}.panel p{margin:8px 0;color:var(--muted)}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:18px 0}.toolbar input{flex:1 1 290px;min-height:44px;border-radius:9px;border:1px solid #66859a;background:#0e2133;color:var(--text);padding:10px 14px}.filters{display:flex;flex-wrap:wrap;gap:7px}.filters button{padding:9px 13px;border:1px solid #648199;background:#243d52;color:var(--text);border-radius:9px}.filters button[aria-pressed="true"]{background:#126365;border-color:var(--mint)}#count{font-size:.9rem;color:var(--gold)}
.scroll{overflow:auto;border-radius:11px;border:1px solid #3a566b}table{width:100%;border-collapse:collapse;text-align:left}th,td{padding:13px 14px;vertical-align:top;border-bottom:1px solid #344e63}thead th{color:var(--mint);background:#102c3b;font-size:.83rem;position:sticky;top:0}tbody tr:hover{background:#1e394d}tbody tr:last-child th,tbody tr:last-child td{border-bottom:0}.atlas-table{min-width:1050px;font-size:.93rem}.atlas-table th:first-child{min-width:140px}.atlas-table th a{color:#f4fbff;text-decoration:none;font-size:1rem}.atlas-table th a:hover{text-decoration:underline}.atlas-table small{display:block;color:var(--muted);font-weight:400}.mode-icon{margin-right:7px}.atlas-table td:nth-child(2){min-width:220px}.atlas-table td:nth-child(3){min-width:200px}.atlas-table td:nth-child(4){min-width:230px;color:var(--muted)}.atlas-table td:nth-child(5){min-width:150px;color:var(--blue)}.atlas-table button{border:1px solid #63879b;background:#254254;color:var(--text);border-radius:8px;padding:5px 9px;white-space:nowrap}.atlas-table button[aria-pressed="true"]{background:#146961;border-color:var(--mint)}
.compare{display:none;background:#102c3b;border:1px solid #4f8c8b;border-radius:12px;padding:17px;margin-top:18px}.compare.show{display:block}.compare-head{display:flex;justify-content:space-between;gap:10px;align-items:center}.compare-head h3{margin:0}.compare-head button{background:transparent;color:var(--mint);border:1px solid #4f8c8b;border-radius:8px;padding:5px 9px}.compare-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:12px}.compare-card{background:#193e4c;border-radius:10px;padding:16px;min-width:0}.compare-card h4{margin:0 0 6px;color:var(--mint)}.compare-card p{margin:8px 0;color:var(--text)}.compare-card ul{margin:8px 0;padding-left:1.3em}.compare-card li{margin:5px 0}.compare-question{color:var(--gold);font-weight:700;margin-top:12px}.pair-table{min-width:750px;font-size:.94rem}.pair-table th{width:190px}.pair-table td:nth-child(2){width:270px;color:var(--gold)}.pair-table td:nth-child(3){color:var(--muted)}
.foot{color:var(--muted);font-size:.9rem;margin-top:30px}@media(max-width:720px){.lead-grid,.compare-grid{grid-template-columns:1fr}.shell{width:min(100% - 24px,1320px)}.hero p{font-size:1rem}}
</style></head><body><main class="shell">
<a class="back" href="../../index.html">← 返回设计模式目录</a>
<header class="hero"><span class="eyebrow">DESIGN PATTERN ATLAS · 23 个经典模式</span><h1>🧭 设计模式速查与对比</h1>
<p>先找问题，再选模式。表格列出每种模式的判断信号、具体场景、边界与易混淆对象；点“加入对比”可以并排看两种模式。</p></header>
<div class="lead-grid"><a href="#table"><strong>🏭 创建型 · 5</strong><span>对象该如何创建、配置、复制或共享？</span></a>
<a href="#table"><strong>🧩 结构型 · 7</strong><span>接口不合、组合爆炸或访问控制问题？</span></a>
<a href="#table"><strong>🎭 行为型 · 11</strong><span>请求、状态、算法与通知怎样协作？</span></a></div>
<section class="panel" id="table"><h2>23 个模式总表</h2><p>搜索“支付”“树”“撤销”或模式名；分类按钮可缩小范围。适用场景是典型信号，不代表所有项目都必须引入模式。</p>
<div class="toolbar"><input id="search" type="search" placeholder="搜索模式、问题或场景" aria-label="搜索设计模式">
<div class="filters" role="group" aria-label="筛选分类"><button type="button" data-filter="all" aria-pressed="true">全部</button>
<button type="button" data-filter="02-creational" aria-pressed="false">创建型</button>
<button type="button" data-filter="03-structural" aria-pressed="false">结构型</button>
<button type="button" data-filter="04-behavioral" aria-pressed="false">行为型</button></div><span id="count" aria-live="polite">显示 23 / 23</span></div>
<div class="scroll"><table class="atlas-table"><thead><tr><th>模式</th><th>何时想到它</th><th>典型场景</th><th>不适合 / 代价</th><th>易混淆</th><th>对比</th></tr></thead><tbody>__ROWS__</tbody></table></div>
<div class="compare" id="compare" aria-live="polite"><div class="compare-head"><h3>并排对比</h3><button type="button" id="clear">清空</button></div>
<div class="compare-grid"><div class="compare-card" id="compare-a"></div><div class="compare-card" id="compare-b"></div></div>
<p class="compare-question" id="compare-question"></p></div></section>
<section class="panel"><h2>最容易选错的 15 组</h2><p>看“判别问题”比背定义更快。点击模式名进入详细图解与伪代码。</p>
<div class="scroll"><table class="pair-table"><thead><tr><th>相似模式</th><th>先问自己</th><th>关键差异</th></tr></thead><tbody>__PAIRS__</tbody></table></div></section>
<section class="panel"><h2>怎么从原则走到模式？</h2><p>先定位真正变化的地方，再看模式是否把这个变化限制在一处。只需要一个简单分支时，直接写清楚通常更合适。</p>
<p><a href="../02-design-principles/design-principles.html">先学 SOLID 与基础原则</a> · <a href="../02-design-principles/composition-over-inheritance.html">组合优于继承</a> · <a href="../../../../system-engineering/whole-architecture-system/index.html">再看系统级架构模式</a></p></section>
<footer class="foot">© 2026 Visuals · 表格与各模式专题共用同一份场景资料</footer></main>
<script>
const patterns=__DATA__;
const pairAnswers=__PAIR_DATA__;
const rows=[...document.querySelectorAll('.atlas-table tbody tr')],search=document.getElementById('search'),filters=[...document.querySelectorAll('[data-filter]')];
let category='all',selected=[];
function filterRows(){const q=search.value.trim().toLocaleLowerCase();let n=0;rows.forEach(row=>{const ok=(category==='all'||row.dataset.category===category)&&row.dataset.search.toLocaleLowerCase().includes(q);row.hidden=!ok;if(ok)n++});document.getElementById('count').textContent='显示 '+n+' / '+rows.length}
filters.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.filter;filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));filterRows()}));search.addEventListener('input',filterRows);
function fillCard(id,item){const card=document.getElementById(id);card.replaceChildren();if(!item){card.textContent='从表格中再选一个模式。';return}const h=document.createElement('h4');const a=document.createElement('a');a.href=item.href;a.textContent=item.icon+' '+item.name;h.append(a);card.append(h);const signal=document.createElement('p');signal.textContent='判断信号：'+item.signal;card.append(signal);const ul=document.createElement('ul');item.scenarios.forEach(s=>{const li=document.createElement('li');li.textContent=s;ul.append(li)});card.append(ul);const avoid=document.createElement('p');avoid.textContent='代价 / 边界：'+item.avoid;card.append(avoid)}
function updateCompare(){document.querySelectorAll('[data-pick]').forEach(button=>button.setAttribute('aria-pressed',String(selected.includes(button.dataset.pick))));const box=document.getElementById('compare');box.classList.toggle('show',selected.length>0);fillCard('compare-a',patterns.find(p=>p.slug===selected[0]));fillCard('compare-b',patterns.find(p=>p.slug===selected[1]));const q=document.getElementById('compare-question');if(selected.length===2){const key=[...selected].sort().join('|');q.textContent='关键差异：'+(pairAnswers[key]||patterns.find(p=>p.slug===selected[0]).question+'；'+patterns.find(p=>p.slug===selected[1]).question)}else q.textContent='再选一个模式，即可并排比较。'}
document.querySelectorAll('[data-pick]').forEach(button=>button.addEventListener('click',()=>{const slug=button.dataset.pick;if(selected.includes(slug))selected=selected.filter(x=>x!==slug);else selected=[...selected,slug].slice(-2);updateCompare()}));document.getElementById('clear').addEventListener('click',()=>{selected=[];updateCompare()});
</script></body></html>'''
    pair_data = {"|".join(sorted((a, b))): answer for a, b, _, answer in PAIRS}
    html = (template.replace("__ROWS__", "\n".join(rows))
            .replace("__PAIRS__", "\n".join(pair_rows))
            .replace("__DATA__", data)
            .replace("__PAIR_DATA__", json.dumps(pair_data, ensure_ascii=False).replace("</", "<\\/")))
    OUT.write_text(html, encoding="utf-8")
    print(f"Generated {len(items)}-pattern atlas")


if __name__ == "__main__":
    main()
