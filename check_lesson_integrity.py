#!/usr/bin/env python3
"""Check in-page navigation, numbered CSS class drift and known example corruption."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
KNOWLEDGE_ROOTS = (
    "artificial-intelligence", "cst", "database-system",
    "programming-and-programs", "system-engineering",
)

# These are API values or paths, not knowledge-tree directory names.
BAD_EXAMPLES = (
    re.compile(r"net/\d{2}-http"),
    re.compile(r"(?<!id=)[\"']\d{2}-tcp[\"']"),
    re.compile(r"\d{2}-database/sql"),
    re.compile(r"\.\d{2}-openclaw"),
    re.compile(r"\.\d{2}-api\b"),
    re.compile(r"/\d{2}-rpc/"),
    re.compile(r"user\.\d{2}-rpc\b"),
    re.compile(r"(?<!id=)[\"']\d{2}-content[\"']"),
)


class LessonMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.fragments = []
        self.classes = []
        self.styles = []
        self.in_style = False
        self.invalid_svg_coordinates = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and attributes.get("href", "").startswith("#"):
            self.fragments.append(attributes["href"][1:])
        self.classes.extend(attributes.get("class", "").split())
        if tag == "style":
            self.in_style = True
        if tag in {"line", "rect", "circle", "ellipse"}:
            for name, value in attrs:
                if name in {"x", "y", "x1", "y1", "x2", "y2", "cx", "cy"} and value:
                    if re.match(r"\s*\d+(?:\.\d+)?\s*[+*/-]\s*[A-Za-z_]", value):
                        self.invalid_svg_coordinates.append(f"{name}={value}")

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.styles.append(data)


def check_page(path):
    source = path.read_text(encoding="utf-8")
    page = LessonMarkup()
    page.feed(source)
    errors = []
    for fragment in page.fragments:
        if fragment and fragment not in page.ids:
            errors.append(f"缺少同页锚点 #{fragment}")
    for coordinate in page.invalid_svg_coordinates:
        errors.append(f"SVG 坐标含未计算的表达式：{coordinate}")
    for lead in re.findall(r'<p\s+class=["\x27]lead["\x27][^>]*>(.*?)</p>', source, flags=re.I | re.S):
        if "&lt;b&gt;" in lead or "&lt;/b&gt;" in lead:
            errors.append("正文强调标签被 HTML 转义")

    css = "\n".join(page.styles)
    if "{{" in css:
        errors.append("CSS 含未展开的双左花括号")
    for token in sorted(set(page.classes)):
        numbered = re.fullmatch(r"\d{2}-(.+)", token)
        if not numbered:
            continue
        plain = numbered.group(1)
        if (re.search(r"(?<![\w-])\." + re.escape(plain) + r"(?![\w-])", css)
                and not re.search(r"(?<![\w-])\." + re.escape(token) + r"(?![\w-])", css)):
            errors.append(f"class={token} 与 CSS .{plain} 不匹配")

    # A numbered directory in a real site link is intentional; only inspect
    # lesson text and examples for leaked directory prefixes.
    examples = re.sub(r'\b(?:href|src)\s*=\s*(?:"[^"]*"|\x27[^\x27]*\x27)', '', source, flags=re.I)
    for pattern in BAD_EXAMPLES:
        if pattern.search(examples):
            errors.append(f"教学示例疑似混入目录编号：{pattern.pattern}")
    return errors


def main():
    problems = []
    checked = 0
    for root in KNOWLEDGE_ROOTS:
        for page in (ROOT / root).rglob("*.html"):
            if page.name == "index.html":
                continue
            checked += 1
            for error in check_page(page):
                problems.append((page.relative_to(ROOT), error))
    for path, error in problems:
        print(f"{path}: {error}", file=sys.stderr)
    print(f"课程页面 {checked}，页面完整性问题 {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
