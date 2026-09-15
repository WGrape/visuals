/* ===== 通用目录树索引组件 =====
   用法（学科 index.html 里只需要写「目录清单」，不用写任何树结构/样式）：

   <div class="tree-layout" data-topic-tree>
       <section class="topic-group" data-path="relational/mysql/architecture"
                data-title="基础架构" data-icon="🐬">
           <div class="topics"> ...卡片... </div>
       </section>
       ...
   </div>

   data-path 必须是该组文章的真实所在目录（相对学科根目录），目录树完全由它推导，
   因此左侧目录树与本地目录结构严格一一对应。
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
    const footerEl = document.querySelector("footer");
    const heroH1 = document.querySelector(".hero h1");
    const subject = heroH1 ? heroH1.textContent.replace(/^[^\w\u4e00-\u9fa5]+/, "").trim() : "";

    const ROOT = "(根目录)";
    const CROSS = "(跨学科)";

    function newBranch(name) {
        return { name: name, children: [], childMap: {}, leaves: [], count: 0 };
    }

    const root = newBranch(null);

    groups.forEach(function (group, index) {
        const path = group.getAttribute("data-path") || ROOT;
        const title = group.getAttribute("data-title") || "未命名";
        const icon = group.getAttribute("data-icon") || "📄";
        const topics = group.querySelector(".topics");
        const count = topics ? topics.querySelectorAll(".card").length : 0;
        const item = {
            id: "p" + (index + 1),
            path: path,
            title: title,
            icon: icon,
            topics: topics,
            count: count
        };
        let node = root;
        if (path !== ROOT && path !== CROSS && path !== "") {
            const parts = path.split("/").filter(Boolean);
            const chain = [];
            parts.forEach(function (part) {
                if (!node.childMap[part]) {
                    const branch = newBranch(part);
                    node.childMap[part] = branch;
                    node.children.push(branch);
                }
                node = node.childMap[part];
                chain.push(node);
            });
            chain.forEach(function (branch) {
                branch.count += count;
            });
        } else {
            node.count += count;
        }
        node.leaves.push(item);
        group.__item = item;
    });

    /* ---------- 生成右侧内容面板 ---------- */
    const content = document.createElement("section");
    content.className = "tree-content";

    groups.forEach(function (group) {
        const item = group.__item;
        const panel = document.createElement("article");
        panel.className = "group-panel";
        panel.id = item.id;
        panel.setAttribute("data-path", item.path);

        const head = document.createElement("header");
        head.className = "panel-head";
        const h2 = document.createElement("h2");
        h2.className = "panel-title";
        const iconSpan = document.createElement("span");
        iconSpan.textContent = item.icon;
        h2.appendChild(iconSpan);
        h2.appendChild(document.createTextNode(item.title));
        const crumb = document.createElement("p");
        crumb.className = "panel-crumb";
        crumb.appendChild(document.createTextNode(subject ? subject + " / " : ""));
        const code = document.createElement("code");
        code.textContent = item.path;
        crumb.appendChild(code);
        crumb.appendChild(document.createTextNode(" \u00b7 " + item.count + " 篇"));
        head.appendChild(h2);
        head.appendChild(crumb);
        panel.appendChild(head);

        if (item.topics) panel.appendChild(item.topics);
        content.appendChild(panel);
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
    filter.placeholder = "筛选分组 / 目录…";
    filter.setAttribute("aria-label", "筛选分组");
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

    function leafNode(item, indent) {
        const li = document.createElement("li");
        li.className = "tree-leaf";
        li.setAttribute("data-target", item.id);
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tree-row";
        const caret = document.createElement("span");
        caret.className = "tree-caret";
        caret.textContent = item.icon;
        const name = document.createElement("span");
        name.className = "tree-name";
        name.textContent = item.title;
        const badge = document.createElement("span");
        badge.className = "tree-badge";
        badge.textContent = item.count;
        btn.appendChild(caret);
        btn.appendChild(name);
        btn.appendChild(badge);
        li.appendChild(btn);
        return li;
    }

    function branchNode(branch) {
        const li = document.createElement("li");
        li.className = "tree-branch is-open";
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tree-row";
        btn.setAttribute("aria-expanded", "true");
        const caret = document.createElement("span");
        caret.className = "tree-caret";
        caret.textContent = "\u25b6";
        const name = document.createElement("span");
        name.className = "tree-name";
        const code = document.createElement("code");
        code.textContent = branch.name;
        name.appendChild(code);
        const badge = document.createElement("span");
        badge.className = "tree-badge";
        badge.textContent = branch.count;
        btn.appendChild(caret);
        btn.appendChild(name);
        btn.appendChild(badge);
        li.appendChild(btn);

        const ul = document.createElement("ul");
        ul.className = "tree-children";
        branch.leaves.forEach(function (item) {
            ul.appendChild(leafNode(item));
        });
        branch.children.forEach(function (child) {
            ul.appendChild(branchNode(child));
        });
        li.appendChild(ul);
        return li;
    }

    root.leaves.forEach(function (item) {
        rootUl.appendChild(leafNode(item));
    });
    root.children.forEach(function (branch) {
        rootUl.appendChild(branchNode(branch));
    });
    nav.appendChild(rootUl);
    const empty = document.createElement("p");
    empty.className = "tree-empty";
    empty.hidden = true;
    empty.textContent = "没有匹配的分组";
    nav.appendChild(empty);
    aside.appendChild(nav);

    layout.appendChild(aside);
    layout.appendChild(content);

    /* ---------- 交互 ---------- */
    const leaves = Array.prototype.slice.call(layout.querySelectorAll(".tree-leaf"));
    const panels = Array.prototype.slice.call(layout.querySelectorAll(".group-panel"));
    const branches = Array.prototype.slice.call(layout.querySelectorAll(".tree-branch"));
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

    function activate(target, opts) {
        opts = opts || {};
        let found = null;
        leaves.forEach(function (leaf) {
            const match = leaf.getAttribute("data-target") === target;
            leaf.classList.toggle("is-active", match);
            if (match) found = leaf;
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

    function openBranch(branch, open) {
        branch.classList.toggle("is-open", open);
        const row = branch.querySelector(":scope > .tree-row");
        if (row) row.setAttribute("aria-expanded", open ? "true" : "false");
    }

    function allOpen() {
        return branches.every(function (branch) {
            return branch.classList.contains("is-open");
        });
    }

    function syncToggleLabel() {
        toggle.textContent = allOpen() ? "收起全部" : "展开全部";
    }

    function ancestorsOf(node) {
        const chain = [];
        let current = node.parentElement;
        while (current && current !== layout) {
            if (current.classList && current.classList.contains("tree-branch")) chain.push(current);
            current = current.parentElement;
        }
        return chain;
    }

    branches.forEach(function (branch) {
        const row = branch.querySelector(":scope > .tree-row");
        if (!row) return;
        row.addEventListener("click", function () {
            openBranch(branch, !branch.classList.contains("is-open"));
            syncToggleLabel();
        });
    });

    leaves.forEach(function (leaf) {
        const row = leaf.querySelector(":scope > .tree-row");
        if (!row) return;
        row.addEventListener("click", function () {
            activate(leaf.getAttribute("data-target"), { scroll: true });
        });
    });

    toggle.addEventListener("click", function () {
        const open = !allOpen();
        branches.forEach(function (branch) {
            openBranch(branch, open);
        });
        syncToggleLabel();
    });

    filter.addEventListener("input", function () {
        const q = filter.value.trim().toLowerCase();
        const items = Array.prototype.slice.call(nav.querySelectorAll("li"));
        items.forEach(function (li) {
            li.classList.remove("is-filtered-out");
        });
        if (!q) {
            empty.hidden = true;
            branches.forEach(function (branch) {
                openBranch(branch, true);
            });
            syncToggleLabel();
            return;
        }
        let anyHit = false;
        leaves.forEach(function (leaf) {
            const hit = (leaf.textContent || "").toLowerCase().indexOf(q) !== -1;
            leaf.classList.toggle("is-filtered-out", !hit);
            if (hit) {
                anyHit = true;
                ancestorsOf(leaf).forEach(function (branch) {
                    openBranch(branch, true);
                });
            }
        });
        branches.forEach(function (branch) {
            const visible = branch.querySelector(".tree-leaf:not(.is-filtered-out)");
            branch.classList.toggle("is-filtered-out", !visible);
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
    const hashTarget = (location.hash || "").slice(1);
    const exists = leaves.some(function (leaf) {
        return leaf.getAttribute("data-target") === hashTarget;
    });
    const candidate = exists ? hashTarget : saved.target;
    const valid = leaves.some(function (leaf) {
        return leaf.getAttribute("data-target") === candidate;
    });
    activate(valid ? candidate : leaves[0].getAttribute("data-target"), { hash: false });
    const active = layout.querySelector(".tree-leaf.is-active");
    if (active) {
        ancestorsOf(active).forEach(function (branch) {
            openBranch(branch, true);
        });
    }
    syncToggleLabel();
})();
