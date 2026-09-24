#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校验所有使用 data-topic-tree 的学科 index.html：
左侧目录树由 topic-tree.js 按 data-path 推导，所以 data-path 必须等于真实目录，
且每张卡片的所在目录必须与所属分组的 data-path 一致。

检查项：
  A  data-path 不是真实目录      → 左侧树里冒出磁盘上不存在的节点（填了中文分组名 / 少序号前缀 / 指向旧结构）
  B  卡片所在目录 != 分组 data-path → 一个分组横跨多个目录，树的分组和右侧内容对不上
  C  卡片目标文件不存在            → 断链
  D  漏挂 / 孤立文件               → 真实目录没被任何 data-path 覆盖，或文件没被任何卡片链接

用法： python3 check_topic_tree.py
说明： 带 data-topic-tree 的子索引页会「自己管自己」，父级页不检查其子树。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SPECIAL = {"", "(根目录)", "(跨学科)"}
PLACEHOLDER = {"coming-soon"}


def is_tree_index(path):
    if not os.path.isfile(path):
        return False
    try:
        return "data-topic-tree" in open(path, encoding="utf-8").read()
    except OSError:
        return False


def find_index_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep) or ".workbuddy" in dirpath.split(os.sep):
            continue
        page = os.path.join(dirpath, "index.html")
        if is_tree_index(page):
            out.append(page)
    return sorted(out)


def extract_groups(page):
    """返回 ([(data_path, [href, ...]), ...], 生成方式)"""
    src = open(page, encoding="utf-8").read()
    groups = []
    for m in re.finditer(r'<section[^>]*class="topic-group"[^>]*>(.*?)</section>', src, re.S):
        attr = re.search(r'data-path="([^"]*)"', m.group(0))
        if attr:
            groups.append((attr.group(1), re.findall(r'href="([^"]+)"', m.group(1))))
    if groups:
        return groups, "静态HTML"
    js = re.search(r"const\s+groups\s*=\s*\{(.*?)\n?\};", src, re.S)
    if js:
        for m in re.finditer(r"'([^']*)'\s*:\s*\[(.*?)\]", js.group(1), re.S):
            groups.append((m.group(1), re.findall(r"'([^']+\.html)'", m.group(2))))
        return groups, "JS生成"
    return [], "无"


def own_scope_dirs(pagedir):
    """本页直接管辖的目录（遇到自带目录树的子索引页即停止下钻）"""
    result = set()

    def walk(d):
        for name in sorted(os.listdir(d)):
            sub = os.path.join(d, name)
            if not os.path.isdir(sub) or name.startswith("."):
                continue
            if is_tree_index(os.path.join(sub, "index.html")):
                continue
            result.add(os.path.relpath(sub, pagedir))
            walk(sub)

    walk(pagedir)
    return result


def audit():
    report = {}
    for page in find_index_files():
        pagedir = os.path.dirname(page)
        rel_page = os.path.relpath(page, ROOT)
        groups, kind = extract_groups(page)
        if not groups:
            continue
        A, B, C, D = [], [], [], []
        covered, declared = set(), set()

        for dp, hrefs in groups:
            if dp in SPECIAL:
                for h in hrefs:
                    covered.add(os.path.normpath(os.path.join(pagedir, h.split("#")[0])))
                continue
            if dp in PLACEHOLDER:
                A.append('占位分组 data-path="%s"（磁盘上无此目录）' % dp)
                continue
            target = os.path.normpath(os.path.join(pagedir, dp))
            if os.path.isdir(target):
                declared.add(os.path.relpath(target, pagedir))
            else:
                A.append('data-path="%s" → 目录不存在（%s）' % (dp, os.path.relpath(target, ROOT)))
            for h in hrefs:
                hp = h.split("#")[0]
                if not hp or hp.startswith(("http", "mailto:", "/", "javascript:")):
                    continue
                absh = os.path.normpath(os.path.join(pagedir, hp))
                covered.add(absh)
                if not os.path.exists(absh):
                    C.append("%s → %s（文件不存在）" % (dp, h))
                elif os.path.isdir(target) and os.path.normpath(os.path.dirname(absh)) != target:
                    B.append("%s 混入 %s（真实目录 %s）" % (dp, h, os.path.relpath(os.path.dirname(absh), ROOT)))

        for d in sorted(own_scope_dirs(pagedir)):
            absd = os.path.join(pagedir, d)
            has_html = any(f.endswith(".html") and f != "index.html" for f in os.listdir(absd))
            if has_html and not any(x == d or x.startswith(d + "/") for x in declared):
                D.append("真实目录 %s/ 未被任何 data-path 覆盖" % d)

        if A or B or C or D:
            report[rel_page] = (kind, A, B, C, D)

    labels = [("A", "data-path 不是真实目录 → 左侧树凭空多出节点"),
              ("B", "卡片所在目录与分组 data-path 不一致 → 树的分组和内容对不上"),
              ("C", "卡片断链"),
              ("D", "漏挂 / 孤立文件")]
    for page, (kind, A, B, C, D) in report.items():
        print("\n" + "=" * 72)
        print("### %s   [%s]" % (page, kind))
        for tag, text, items in (("A", labels[0][1], A), ("B", labels[1][1], B),
                                 ("C", labels[2][1], C), ("D", labels[3][1], D)):
            if items:
                print("  【%s %s】%d" % (tag, text, len(items)))
                for i in items:
                    print("     - " + i)
    print("\n" + "=" * 72)
    print("有问题的索引页：%d 个" % len(report))
    return 1 if report else 0


if __name__ == "__main__":
    sys.exit(audit())
