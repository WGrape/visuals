(function () {
    // Pages that need a different relative depth can declare it on <html>,
    // e.g. <html data-app-root="../../">. Existing pages retain the
    // original ../container/ behavior when the attribute is absent.
    const appRoot = document.documentElement.getAttribute("data-app-root");
    const containerBase = (appRoot === null ? "../" : appRoot) + "container/index.html?page=";

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
        if (relativePath.endsWith("/index.html")) {
            return null;
        }

        return relativePath + url.search + url.hash;
    }

    function rewriteCardLink(anchor) {
        const rawHref = anchor.getAttribute("href");
        if (shouldSkipLink(rawHref)) {
            return;
        }

        const targetPath = buildTargetPath(rawHref);
        if (!targetPath) {
            return;
        }

        anchor.setAttribute("href", containerBase + encodeURIComponent(targetPath));
    }

    document.querySelectorAll("a.card[href]").forEach(rewriteCardLink);
})();
