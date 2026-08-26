#!/bin/bash

# 检查每个HTML文件是否被链接到对应的上级index.html文件中

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

total=0
missing=0
found=0
skipped=0
missing_files=""
skipped_files=""

echo "开始检查HTML文件链接..."
echo "=============================="

# 遍历所有HTML文件，排除根目录的index.html和备份文件
while IFS= read -r -d '' html_file; do
    # 跳过根目录的index.html
    if [[ "$html_file" == "./index.html" ]]; then
        continue
    fi

    # 跳过特定文件
    if [[ "$html_file" == *".bak" || "$html_file" == *"container.html" ]]; then
        # 备份文件、在visuals中引入不同HTML页面的一个容器文件
        continue
    fi

    # 跳过node_modules等目录
    if [[ "$html_file" == *"node_modules"* || "$html_file" == *".git"* ]]; then
        continue
    fi

    total=$((total + 1))

    # 获取文件的相对路径（去掉开头的./）
    relative_path="${html_file#./}"

    # 查找“最近的上级 index.html”：从文件所在目录开始，逐级向上查找，
    # 直到仓库根目录。只要任意一级祖先 index.html 中包含了指向该文件的链接，
    # 即视为已链接。这样可以正确处理嵌套目录（如
    # kaoyan/kaoyan-math-2/Linear-Algebra/ch01.html 应检查
    # kaoyan/kaoyan-math-2/Linear-Algebra/index.html，而不是 kaoyan/index.html）。
    #
    # 逻辑示例：
    # - game-design/flash.html               -> game-design/index.html
    # - algorithm/trees/binary_tree.html     -> algorithm/trees/index.html（或更高层 index）
    # - kaoyan/kaoyan-math-2/LA/ch01.html    -> kaoyan/kaoyan-math-2/LA/index.html（或更高层 index）

    dir=$(dirname "$relative_path")
    linked=0
    checked=""

    while [[ "$dir" != "." && "$dir" != "/" && -n "$dir" ]]; do
        candidate="$dir/index.html"
        if [[ -f "$candidate" ]]; then
            checked="$checked $candidate"
            # 计算从 candidate 所在目录到该文件的相对路径（macOS 无 realpath，用 python3 兜底）
            link_target=$(python3 -c "import os,sys;print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$relative_path" "$dir" 2>/dev/null || basename "$relative_path")
            if grep -q "href=\"${link_target}\"" "$candidate" 2>/dev/null; then
                linked=1
                break
            fi
            # 兜底：文件名匹配（适配 href="子目录/文件名" 等写法）
            filename=$(basename "$relative_path")
            if grep -q "href=\".*${filename}\"" "$candidate" 2>/dev/null; then
                linked=1
                break
            fi
        fi
        dir=$(dirname "$dir")
    done

    if [[ "$linked" -eq 1 ]]; then
        echo -e "${GREEN}✓ $relative_path${NC}"
        found=$((found + 1))
    else
        if [[ -z "$checked" ]]; then
            skip_info="$relative_path (未找到任何上级 index.html)"
            echo -e "${YELLOW}跳过: $skip_info${NC}"
            skipped=$((skipped + 1))
            if [[ -z "$skipped_files" ]]; then
                skipped_files="$skip_info"
            else
                skipped_files="$skipped_files, $skip_info"
            fi
        else
            missing_info="$relative_path -> 未在以下 index 中找到链接:$checked"
            echo -e "${RED}✗ $missing_info${NC}"
            missing=$((missing + 1))
            if [[ -z "$missing_files" ]]; then
                missing_files="$missing_info"
            else
                missing_files="$missing_files, $missing_info"
            fi
        fi
    fi

done < <(find . -name "*.html" -print0)

echo "=============================="
echo "检查完成！"
echo "总计: $total 个文件"
echo -e "${GREEN}已链接: $found${NC}"
echo -e "${RED}未链接: $missing${NC}"
if [[ $missing -gt 0 ]]; then
    echo -e "${RED}未链接文件: $missing_files${NC}"
fi
echo -e "${YELLOW}跳过(无上级 index.html): $skipped${NC}"
if [[ $skipped -gt 0 ]]; then
    echo -e "${YELLOW}跳过文件: $skipped_files${NC}"
fi

if [[ $missing -gt 0 ]]; then
    exit 1
else
    exit 0
fi
