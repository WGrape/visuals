#!/usr/bin/env python3
"""Check the physical, numbered four-level hierarchy of the knowledge library."""
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parent
ROOTS = (
    "artificial-intelligence", "cst", "database-system",
    "programming-and-programs", "system-engineering",
)
NUMBERED = re.compile(r"^\d{2}-")
LESSONS = {".html", ".md"}


def is_lesson(path):
    return path.is_file() and path.suffix.lower() in LESSONS and path.name != "index.html"


def check_sibling_numbers(parent, directories, errors):
    """Numbered topic siblings must not reuse or skip a position."""
    numbers = sorted(int(path.name[:2]) for path in directories if NUMBERED.match(path.name))
    if len(numbers) > 1 and numbers != list(range(numbers[0], numbers[-1] + 1)):
        errors.append(f"同层目录编号重复或断档：{parent.relative_to(ROOT)}，编号 {numbers}")


def check_overview_name(directory, errors):
    if directory.name.startswith("00-") and directory.name != "00-overview":
        errors.append(f"概览目录应命名为 00-overview：{directory.relative_to(ROOT)}")


class IndexLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.cards = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        attributes = dict(attrs)
        href = attributes.get("href", "")
        if href:
            self.links.append(href)
            if "card" in attributes.get("class", "").split():
                self.cards.append(href)


def local_page(index, href):
    path = unquote(urlsplit(href).path)
    if not path or path.startswith("/") or Path(path).suffix.lower() not in LESSONS:
        return None
    target = (index.parent / path).resolve()
    if target == ROOT / "index.html" or any(target.is_relative_to(ROOT / name) for name in ROOTS):
        return target
    return None


def check_navigation(errors):
    home = ROOT / "index.html"
    reachable = {home}
    pending = deque([home])
    cards = set()
    while pending:
        index = pending.popleft()
        links = IndexLinks()
        links.feed(index.read_text(encoding="utf-8"))
        for href in links.cards:
            target = local_page(index, href)
            if target is not None:
                cards.add(target)
        for href in links.links:
            target = local_page(index, href)
            if target is not None and target.name == "index.html" and target.is_file() and target not in reachable:
                reachable.add(target)
                pending.append(target)

    for root_name in ROOTS:
        for subject in (ROOT / root_name).iterdir():
            if not subject.is_dir():
                continue
            for page in subject.rglob("*"):
                if not page.is_file() or (page.name != "index.html" and not is_lesson(page)):
                    continue
                if page.name == "index.html" and page not in reachable:
                    errors.append(f"首页无法到达索引：{page.relative_to(ROOT)}")
                elif page.name != "index.html" and page not in cards:
                    errors.append(f"可达索引缺少课程卡片：{page.relative_to(ROOT)}")


def audit():
    errors = []
    placeholders = []
    subjects = chapters = articles = 0
    for root_name in ROOTS:
        root = ROOT / root_name
        if not root.is_dir():
            errors.append(f"缺少一级目录：{root_name}")
            continue
        if (root / "index.html").exists():
            errors.append(f"一级目录不应建立 index.html：{root_name}")
        for marker in root.rglob(".gitkeep"):
            if any(item.name not in {".gitkeep", ".DS_Store"} for item in marker.parent.iterdir()):
                errors.append(f"非空目录不应保留 .gitkeep：{marker.relative_to(ROOT)}")
        for subject in sorted(p for p in root.iterdir() if p.is_dir()):
            subjects += 1
            if not (subject / "index.html").is_file():
                errors.append(f"二级目录缺少 index.html：{subject.relative_to(ROOT)}")
            for file in subject.iterdir():
                if is_lesson(file):
                    errors.append(f"课程停留在二级目录：{file.relative_to(ROOT)}")
            chapter_dirs = sorted(p for p in subject.iterdir() if p.is_dir())
            check_sibling_numbers(subject, chapter_dirs, errors)
            if not chapter_dirs:
                errors.append(f"二级目录缺少三级目录：{subject.relative_to(ROOT)}")
            for chapter in chapter_dirs:
                chapters += 1
                check_overview_name(chapter, errors)
                contained = [p for p in chapter.rglob("*") if is_lesson(p)]
                articles += len(contained)
                has_topics = any(p.is_dir() for p in chapter.iterdir())
                if not NUMBERED.match(chapter.name):
                    errors.append(f"三级目录未编号：{chapter.relative_to(ROOT)}")
                if not has_topics:
                    errors.append(f"三级目录缺少四级专题：{chapter.relative_to(ROOT)}")
                if not contained:
                    placeholders.append(f"待填充：{chapter.relative_to(ROOT)}")
                for index in chapter.rglob("index.html"):
                    errors.append(f"三级及更深目录不应建立 index.html：{index.relative_to(ROOT)}")
                for topic in chapter.iterdir():
                    if topic.is_dir() and not any(is_lesson(p) for p in topic.rglob("*")):
                        placeholders.append(f"待填充专题：{topic.relative_to(ROOT)}")
                for directory in (chapter, *(p for p in chapter.rglob("*") if p.is_dir())):
                    children = [p for p in directory.iterdir() if p.is_dir()]
                    check_sibling_numbers(directory, children, errors)
                for descendant in chapter.rglob("*"):
                    if descendant.is_dir():
                        check_overview_name(descendant, errors)
                        if not NUMBERED.match(descendant.name):
                            errors.append(f"四级及更深目录未编号：{descendant.relative_to(ROOT)}")
                for file in chapter.iterdir():
                    if is_lesson(file):
                        errors.append(f"课程停留在三级目录：{file.relative_to(ROOT)}")
    check_navigation(errors)
    print(f"二级学科 {subjects}，三级章节 {chapters}，四级或更深课程 {articles}")
    for item in sorted(set(placeholders)):
        print("占位提醒：", item)
    for item in errors:
        print("结构错误：", item, file=sys.stderr)
    print(f"结构错误 {len(errors)}，未填充占位提醒 {len(set(placeholders))}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(audit())
