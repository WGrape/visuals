(function () {
    // Pages that need a different relative depth can declare it on <html>,
    // e.g. <html data-app-root="../../">. Existing pages retain the
    // original ../container/ behavior when the attribute is absent.
    const appRoot = document.documentElement.getAttribute("data-app-root");
    const containerBase = (appRoot === null ? "../" : appRoot) + "container.html?page=";

    function shouldSkipLink(rawHref) {
        if (!rawHref) return true;

        const href = rawHref.trim();
        if (!href || href === "#") return true;
        if (href.startsWith("javascript:")) return true;
        if (href.startsWith("mailto:")) return true;
        return false;
    }

    function buildTargetPath(rawHref) {
        const url = new URL(rawHref, window.location.href);

        if (url.origin !== window.location.origin) {
            return null;
        }

        const marker = "/visuals/";
        const markerIndex = url.pathname.indexOf(marker);
        if (markerIndex === -1) {
            return null;
        }

        const relativePath = url.pathname
            .slice(markerIndex + marker.length)
            .replace(/^\/+/, "");

        if (!relativePath.endsWith(".html")) {
            return null;
        }

        // Skip directory index cards; keep section navigation unchanged.
        if (relativePath.endsWith("index.html")) {
            return null;
        }

        return relativePath + url.search + url.hash;
    }

    function buildSourceIndexPath() {
        const marker = "/visuals/";
        const markerIndex = window.location.pathname.indexOf(marker);
        if (markerIndex === -1) {
            return null;
        }

        const relativePath = window.location.pathname
            .slice(markerIndex + marker.length)
            .replace(/^\/+/, "");

        return relativePath.endsWith("index.html") ? relativePath : null;
    }

    const sourceIndexPath = buildSourceIndexPath();

    function rewriteCardLink(anchor) {
        const rawHref = anchor.getAttribute("href");
        if (shouldSkipLink(rawHref)) {
            return;
        }

        // 知识内容始终在新标签页学习，不离开当前目录定位。
        anchor.setAttribute("target", "_blank");
        anchor.setAttribute("rel", "noopener");

        const targetPath = buildTargetPath(rawHref);
        if (!targetPath) {
            return;
        }

        let target = containerBase + encodeURIComponent(targetPath);
        if (sourceIndexPath) {
            target += "&from=" + encodeURIComponent(sourceIndexPath);
        }
        anchor.setAttribute("href", target);
    }

    document.querySelectorAll("a.card[href]").forEach(rewriteCardLink);
})();
