/* ===== 通用目录树索引组件 =====
   用法（学科 index.html 里只需要写「目录清单」，不用写任何树结构/样式）：

   <div class="tree-layout" data-topic-tree>
       <section class="topic-group" data-path="relational/mysql/architecture"
                data-title="基础架构" data-icon="🐬" data-desc="这段目录里讲的是什么…">
           <div class="topics"> ...卡片... </div>
       </section>
       ...
   </div>

   渲染规则：
   - 左侧渲染成一棵「纯目录树」：节点就是目录名（data-path 推导），只显示目录名 + 篇数。
   - 最后一级目录同样是一个目录节点，但可点击（点击后右侧显示该目录的内容）。
   - 右侧按「目录」为单位生成内容区，只展示该目录下的文件卡片；
     分类名称、层级与篇数均由左侧目录树承担。
*/
(function () {
    const layout = document.querySelector("[data-topic-tree]");
    if (!layout) return;

    // 样式与脚本同目录，自动引入，索引页无需再写 <link>
    if (!document.querySelector('link[data-topic-tree-css]')) {
        const current = document.currentScript;
        const base = current ? current.src.replace(/[^/]+$/, "") : "";
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = base + "topic-tree.css";
        link.setAttribute("data-topic-tree-css", "");
        document.head.appendChild(link);
    }

    // 索引页始终从顶部打开，避免浏览器恢复滚动位置后看不到页头与目录树顶部
    if ("scrollRestoration" in history) {
        history.scrollRestoration = "manual";
    }

    const groups = Array.prototype.slice.call(layout.querySelectorAll(".topic-group"));
    if (!groups.length) return;

    const headerEl = document.querySelector("header");

    const ROOT_LABEL = "(根目录)";
    const CROSS_LABEL = "(跨学科)";

    function newDir(name, parent) {
        return {
            name: name,
            parent: parent,
            path: "",
            children: [],
            childMap: {},
            groups: [],
            count: 0,
            panelId: null,
            li: null
        };
    }

    const root = newDir(null, null);

    /* ---------- 由 data-path 推导目录树 ---------- */
    groups.forEach(function (group) {
        const rawPath = group.getAttribute("data-path") || "";
        const title = group.getAttribute("data-title") || "未命名";
        const icon = group.getAttribute("data-icon") || "📄";
        const desc = group.getAttribute("data-desc") || "";
        const topics = group.querySelector(".topics");
        const count = topics ? topics.querySelectorAll(".card").length : 0;
        const item = { rawPath: rawPath, title: title, icon: icon, desc: desc, topics: topics, count: count };

        const isSpecial = rawPath === "" || rawPath === ROOT_LABEL || rawPath === CROSS_LABEL;
        if (isSpecial) {
            // 「(根目录) / (跨学科)」这类没有真实目录的分组，挂到根节点上，稍后作为顶层节点渲染
            root.groups.push(item);
            root.count += count;
        } else {
            const parts = rawPath.split("/").filter(Boolean);
            let node = root;
            parts.forEach(function (part) {
                if (!node.childMap[part]) {
                    const dir = newDir(part, node);
                    dir.path = node.path ? node.path + "/" + part : part;
                    node.childMap[part] = dir;
                    node.children.push(dir);
                }
                node = node.childMap[part];
            });
            let cur = node;
            while (cur && cur !== root) {
                cur.count += count;
                cur = cur.parent;
            }
            node.groups.push(item);
        }
        group.__item = item;
    });

    // 把根节点上的特殊分组（跨学科等）包成一个顶层伪目录节点，保证它们也能被渲染、被点击
    if (root.groups.length) {
        const label = root.groups[0].rawPath === CROSS_LABEL ? CROSS_LABEL : ROOT_LABEL;
        const pseudo = newDir(label, root);
        pseudo.path = label;
        pseudo.groups = root.groups;
        pseudo.count = root.count;
        root.children.push(pseudo);
    }

    /* ---------- 收集「有内容的目录」节点（决定右侧内容区与树的点击目标） ---------- */
    const ordered = [];
    (function walk(node) {
        if (node.groups.length) {
            node.panelId = "g" + (ordered.length + 1);
            ordered.push(node);
        }
        node.children.forEach(walk);
    })(root);

    if (!ordered.length) return;

    /* ---------- 生成右侧内容面板：一个目录 = 一块内容区 ---------- */
    const content = document.createElement("section");
    content.className = "tree-content";

    ordered.forEach(function (node) {
        const panel = document.createElement("article");
        panel.className = "group-panel";
        panel.id = node.panelId;
        panel.setAttribute("data-path", node.path);

        const single = node.groups.length === 1;
        const first = node.groups[0];

        // 分类名称和层级只由左侧目录树呈现；右侧仅展示当前目录的知识入口。
        if (single) {
            if (first.topics) panel.appendChild(first.topics);
        } else {
            // 同一路径下的多个卡片集合按原顺序连续展示。
            node.groups.forEach(function (item) {
                const sec = document.createElement("section");
                sec.className = "panel-section";

                if (item.topics) sec.appendChild(item.topics);
                panel.appendChild(sec);
            });
        }

        content.appendChild(panel);
    });

    // 原始 <section class="topic-group"> 已被搬空，移除占位
    groups.forEach(function (group) {
        group.remove();
    });

    /* ---------- 生成左侧目录树 ---------- */
    const aside = document.createElement("aside");
    aside.className = "tree-panel";

    const toolbar = document.createElement("div");
    toolbar.className = "tree-toolbar";
    const filter = document.createElement("input");
    filter.className = "tree-filter";
    filter.type = "search";
    filter.placeholder = "筛选目录…";
    filter.setAttribute("aria-label", "筛选目录");
    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "tree-toggle";
    toggle.textContent = "收起全部";
    toolbar.appendChild(filter);
    toolbar.appendChild(toggle);
    aside.appendChild(toolbar);

    const nav = document.createElement("nav");
    nav.className = "tree-nav";
    const rootUl = document.createElement("ul");
    rootUl.className = "tree-root";

    function buildNode(node) {
        const hasChildren = node.children.length > 0;
        const hasContent = node.groups.length > 0;

        const li = document.createElement("li");
        li.className = "tree-node" + (hasChildren ? " tree-branch" : "") + (hasContent ? " is-content" : "");
        if (hasChildren) li.classList.add("is-open");

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tree-row";
        if (hasChildren) btn.setAttribute("aria-expanded", "true");

        const mark = document.createElement("span");
        mark.className = "tree-mark";
        if (hasChildren) {
            mark.classList.add("tree-caret");
            mark.textContent = "\u25b8";
        } else if (hasContent) {
            // 叶子目录（有内容）：实心圆点
            mark.classList.add("tree-dot");
        }

        const name = document.createElement("span");
        name.className = "tree-name";
        const code = document.createElement("code");
        code.textContent = node.name;
        name.appendChild(code);

        const badge = document.createElement("span");
        badge.className = "tree-badge";
        badge.textContent = node.count;

        btn.appendChild(mark);
        btn.appendChild(name);
        btn.appendChild(badge);
        li.appendChild(btn);

        if (hasChildren) {
            const ul = document.createElement("ul");
            ul.className = "tree-children";
            node.children.forEach(function (child) {
                ul.appendChild(buildNode(child));
            });
            li.appendChild(ul);
        }

        node.li = li;
        return li;
    }

    root.children.forEach(function (node) {
        rootUl.appendChild(buildNode(node));
    });

    nav.appendChild(rootUl);
    const empty = document.createElement("p");
    empty.className = "tree-empty";
    empty.hidden = true;
    empty.textContent = "没有匹配的目录";
    nav.appendChild(empty);
    aside.appendChild(nav);

    layout.appendChild(aside);
    layout.appendChild(content);

    /* ---------- 交互 ---------- */
    const allNodes = [];
    (function collect(node) {
        allNodes.push(node);
        node.children.forEach(collect);
    })(root);

    const panels = Array.prototype.slice.call(layout.querySelectorAll(".group-panel"));
    const branches = allNodes.filter(function (n) {
        return n.li && n.children.length > 0;
    });
    const isNarrow = window.matchMedia("(max-width: 900px)");

    const storageKey = "visuals-tree:" + location.pathname;
    let saved = {};
    try {
        saved = JSON.parse(localStorage.getItem(storageKey) || "{}") || {};
    } catch (err) {
        saved = {};
    }

    function remember(target) {
        saved.target = target;
        try {
            localStorage.setItem(storageKey, JSON.stringify(saved));
        } catch (err) {
            /* ignore */
        }
    }

    function openNode(node, open) {
        if (!node || !node.li || !node.li.classList.contains("tree-branch")) return;
        node.li.classList.toggle("is-open", open);
        const row = node.li.querySelector(":scope > .tree-row");
        if (row) row.setAttribute("aria-expanded", open ? "true" : "false");
    }

    function ancestorsOf(node) {
        const chain = [];
        let current = node ? node.parent : null;
        while (current && current !== root) {
            chain.push(current);
            current = current.parent;
        }
        return chain;
    }

    function activate(target, opts) {
        opts = opts || {};
        let found = null;
        ordered.forEach(function (node) {
            const match = node.panelId === target;
            if (node.li) node.li.classList.toggle("is-active", match);
            if (match) found = node;
        });
        panels.forEach(function (panel) {
            panel.classList.toggle("is-active", panel.id === target);
        });
        if (!found) return;
        remember(target);
        if (opts.scroll) {
            const panel = document.getElementById(target);
            if (panel && isNarrow.matches) {
                const top = panel.getBoundingClientRect().top + window.pageYOffset - 90;
                window.scrollTo({ top: top, behavior: "smooth" });
            }
        }
        if (opts.hash !== false) {
            try {
                history.replaceState(null, "", "#" + target);
            } catch (err) {
                /* ignore */
            }
        }
    }

    function allOpen() {
        return branches.every(function (node) {
            return node.li.classList.contains("is-open");
        });
    }

    function syncToggleLabel() {
        toggle.textContent = allOpen() ? "收起全部" : "展开全部";
    }

    allNodes.forEach(function (node) {
        if (!node.li) return;
        const hasChildren = node.children.length > 0;
        const hasContent = node.groups.length > 0;
        if (!hasChildren && !hasContent) return;

        const row = node.li.querySelector(":scope > .tree-row");
        row.addEventListener("click", function (ev) {
            const onCaret = !!(ev.target.closest && ev.target.closest(".tree-caret"));
            if (hasChildren && (onCaret || !hasContent)) {
                openNode(node, !node.li.classList.contains("is-open"));
            }
            if (hasContent && !onCaret) {
                activate(node.panelId, { scroll: true });
            }
            syncToggleLabel();
        });
    });

    toggle.addEventListener("click", function () {
        const open = !allOpen();
        branches.forEach(function (node) {
            openNode(node, open);
        });
        syncToggleLabel();
    });

    filter.addEventListener("input", function () {
        const q = filter.value.trim().toLowerCase();
        allNodes.forEach(function (node) {
            if (node.li) node.li.classList.remove("is-filtered-out");
        });
        if (!q) {
            empty.hidden = true;
            branches.forEach(function (node) {
                openNode(node, true);
            });
            syncToggleLabel();
            return;
        }
        let anyHit = false;
        (function filterNode(node) {
            const selfHit =
                (node.name || "").toLowerCase().indexOf(q) !== -1 ||
                node.groups.some(function (g) {
                    return (g.title || "").toLowerCase().indexOf(q) !== -1;
                });
            let childHit = false;
            node.children.forEach(function (child) {
                if (filterNode(child)) childHit = true;
            });
            const visible = selfHit || childHit;
            if (node.li) node.li.classList.toggle("is-filtered-out", !visible);
            if (visible && node.children.length) openNode(node, true);
            return visible;
        })(root);
        anyHit = root.children.some(function (child) {
            return child.li && !child.li.classList.contains("is-filtered-out");
        });
        empty.hidden = anyHit;
        syncToggleLabel();
    });

    /* ---------- 尺寸自适应：让吸顶目录树永远紧贴页头下方 ---------- */
    function fitLayout() {
        const headerH = headerEl ? Math.round(headerEl.getBoundingClientRect().height) : 72;
        document.documentElement.style.setProperty("--header-h", headerH + "px");
        const rect = layout.getBoundingClientRect();
        const afterLayout = Math.max(
            0,
            Math.round(document.documentElement.scrollHeight - (rect.bottom + window.pageYOffset))
        );
        document.documentElement.style.setProperty("--below-layout", afterLayout + "px");
    }

    /* ---------- 初始化 ---------- */
    fitLayout();
    window.addEventListener("resize", fitLayout);
    window.addEventListener("load", fitLayout);

    nav.scrollTop = 0;
    const ids = ordered.map(function (node) {
        return node.panelId;
    });
    const hashTarget = (location.hash || "").slice(1);
    const defaultTarget = ids[0];
    let target = ids.indexOf(hashTarget) !== -1 ? hashTarget : saved.target;
    if (ids.indexOf(target) === -1) target = defaultTarget;

    const activeNode = ordered.filter(function (node) {
        return node.panelId === target;
    })[0];
    if (activeNode) {
        ancestorsOf(activeNode).forEach(function (node) {
            openNode(node, true);
        });
        openNode(activeNode, true);
    }
    activate(target, { hash: false });
    syncToggleLabel();
})();
