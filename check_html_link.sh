#!/bin/bash

# 检查每个HTML文件是否被链接到对应的上级index.html文件中

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

total=0
missing=0
found=0
missing_files=""

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

    # 找到对应的上级index.html
    # 逻辑：
    # - game-design/flash-technology-explained.html -> game-design/index.html
    # - algorithm/trees/binary_tree_traversal.html -> algorithm/index.html
    # - high-concurrency/kafka/kafka-partition-explained.html -> high-concurrency/index.html

    # 按/分割路径，取第一部分作为顶级目录
    top_dir=$(echo "$relative_path" | cut -d'/' -f1)

    # 如果文件直接在顶级目录下（如 game-design/xxx.html），则上级index就是 top_dir/index.html
    # 如果文件在更深的目录（如 algorithm/trees/xxx.html），上级index也是 top_dir/index.html
    parent_index="${top_dir}/index.html"

    # 检查parent_index是否存在
    if [[ ! -f "$parent_index" ]]; then
        echo -e "${YELLOW}跳过: $relative_path (上级index $parent_index 不存在)${NC}"
        continue
    fi

    # 检查parent_index中是否有链接指向这个文件
    # 需要匹配的可能形式：
    # - href="kafka/kafka-partition-explained.html"
    # - href="trees/binary_tree_traversal.html"
    # - href="flash-technology-explained.html"

    # 获取相对于parent_index所在目录的路径
    parent_dir=$(dirname "$parent_index")
    link_target=$(realpath --relative-to="$parent_dir" "$html_file" 2>/dev/null || echo "$relative_path" | sed "s|^${top_dir}/||")

    # 检查链接是否存在
    if grep -q "href=\"${link_target}\"" "$parent_index" 2>/dev/null; then
        echo -e "${GREEN}✓ $relative_path${NC}"
        found=$((found + 1))
    else
        # 尝试另一种方式：直接搜索文件名
        filename=$(basename "$html_file")
        if grep -q "href=\".*${filename}\"" "$parent_index" 2>/dev/null; then
            echo -e "${GREEN}✓ $relative_path${NC}"
            found=$((found + 1))
        else
            missing_info="$relative_path -> 未在 $parent_index 中找到链接"
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

if [[ $missing -gt 0 ]]; then
    exit 1
else
    exit 0
fi
