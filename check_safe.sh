#!/bin/bash

# check_safe.sh —— 仓库安全检查脚本
#
# 设计目标：在提交 / 发布前扫描本仓库，发现“不该出现”的内容：
#   步骤 1：找出所有非 .html 文件（防止脚本 / 二进制 / 密钥文件混入 HTML 知识库）
#   步骤 2：检查 HTML 内部坏链（href / src 指向不存在的本地文件）
#   步骤 3：扫描疑似密钥 / 敏感信息（password / api_key / token / 私钥 等）
#
# 用法：  bash check_safe.sh
# 退出码：发现“硬失败”项（坏链 / 敏感信息）时返回 1，否则返回 0。
#         非 HTML 文件默认只做“提示(warn)”，不导致失败（见 FAIL_ON_NON_HTML）。
#
# 所有目录 / 文件过滤项都在下方 CONFIG 区，可自行增删。
# 兼容性：仅使用 bash 3.2（macOS 默认 /bin/bash）支持的特性。

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# =========================  CONFIG  =========================
# 内部 / 工具目录，整个扫描跳过（不参与任何步骤）
EXCLUDE_DIRS=(".git" "node_modules" ".workbuddy" ".claude")

# 明确已知、刻意保留的非 HTML 文件（步骤 1 中跳过，避免自报）
EXCLUDE_FILES=("check_html_link.sh" "check_safe.sh")

# 步骤 1：是否把“非 HTML 文件”视为失败（true=失败，false=仅提示）
FAIL_ON_NON_HTML=false

# 步骤 2：是否启用坏链检查
RUN_STEP2=true

# 步骤 3：是否启用敏感信息扫描
RUN_STEP3=true
# 仅扫描这些“可能存放真实密钥”的代码 / 配置文件类型，
# 不扫 .html / .md 等教程正文（正文里 password / token 等词是正常教学内容，会严重误报）
CODE_EXT=("sh" "py" "js" "ts" "jsx" "tsx" "json" "yml" "yaml" "toml" "env" "conf" "cfg" "ini" "xml" "txt" "properties" "gradle")
# 高精度匹配：结构化密钥格式，或“赋值后跟 >=24 位凭证型字符串”
SECRET_PATTERNS=(
  'BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY'
  'AKIA[0-9A-Z]{16}'
  'sk-[A-Za-z0-9]{20,}'
  'ghp_[A-Za-z0-9]{36}'
  '(password|passwd|secret|api[_-]?key|token)[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9+/_=-]{24,}'
)
# ===========================================================

# 统计
non_html_count=0
ext_list=()                # 扩展名列表（步骤 1，最后统一计数）
broken_count=0
secret_count=0
fail_flag=0

# 判断是否应跳过该路径（命中 EXCLUDE_DIRS 或 EXCLUDE_FILES）
should_skip() {
  local f="$1"
  local d base
  for d in "${EXCLUDE_DIRS[@]}"; do
    if [[ "$f" == *"/$d/"* || "$f" == "./$d/"* || "$f" == "./$d" ]]; then
      return 0
    fi
  done
  base=$(basename "$f")
  for ef in "${EXCLUDE_FILES[@]}"; do
    if [[ "$base" == "$ef" ]]; then
      return 0
    fi
  done
  return 1
}

echo -e "${CYAN}开始仓库安全检查...${NC}"
echo "=============================="

# ------------------------------------------------------------------
# 步骤 1：扫描所有文件，打印非 .html 文件
# ------------------------------------------------------------------
echo -e "${CYAN}[步骤 1] 检查非 HTML 文件${NC}"
echo "--------------------------------------------------"
while IFS= read -r -d '' f; do
  should_skip "$f" && continue
  if [[ "$f" != *.html ]]; then
    echo -e "  ${YELLOW}非 HTML: $f${NC}"
    non_html_count=$((non_html_count + 1))
    # 扩展名归类（无扩展名记为 <none>）
    if [[ "$f" == *.* ]]; then
      ext="${f##*.}"
    else
      ext="<none>"
    fi
    ext_list+=("$ext")
  fi
done < <(find . -type f -print0)

echo "--------------------------------------------------"
if [[ $non_html_count -eq 0 ]]; then
  echo -e "  ${GREEN}✓ 未发现非 HTML 文件${NC}"
else
  echo -e "  ${YELLOW}非 HTML 文件共 $non_html_count 个，按扩展名分布：${NC}"
  printf '%s\n' "${ext_list[@]}" | sort | uniq -c | while read -r cnt ext; do
    echo -e "    .$ext : $cnt"
  done
  if $FAIL_ON_NON_HTML; then
    fail_flag=1
  fi
fi

# ------------------------------------------------------------------
# 步骤 2：检查 HTML 内部坏链
# ------------------------------------------------------------------
if $RUN_STEP2; then
  echo
  echo -e "${CYAN}[步骤 2] 检查 HTML 内部坏链（href / src 指向不存在的本地文件）${NC}"
  echo "--------------------------------------------------"
  broken_links=()
  while IFS= read -r -d '' html_file; do
    should_skip "$html_file" && continue
    dir=$(dirname "$html_file")
    # 用进程替换避免 subshell，保证变量作用域；提取 href="..." 与 src="..."
    while IFS= read -r target; do
      [[ -z "$target" ]] && continue
      # 去掉 URL 片段（#...），片段不是文件路径的一部分
      target="${target%%#*}"
      [[ -z "$target" ]] && continue
      # 跳过外链 / 协议 / 脚本 / data URI
      # 也跳过协议相对(//cdn...)与站点根绝对(/style.css) —— 这类由 Web 服务器 / CDN 解析，不是文件相对路径
      if [[ "$target" == http://* || "$target" == https://* || "$target" == mailto:* \
         || "$target" == tel:* || "$target" == \#* || "$target" == javascript:* \
         || "$target" == data:* || "$target" == //* || "$target" == /* ]]; then
        continue
      fi
      # 跳过动态 / 模板生成的 href（含 + ${ < > { } 引号或空格），这类不是真实文件引用
      if [[ "$target" == *"+"* || "$target" == *"\${"* || "$target" == *"<"* || "$target" == *">"* \
         || "$target" == *"{"* || "$target" == *"}"* || "$target" == *"'"* || "$target" == *'"'* \
         || "$target" == *" "* ]]; then
        continue
      fi
      # 既没有 "/" 也没有 "." 的，通常是页内锚点 / JS 钩子（如 s6、tab1），不是文件路径
      if [[ "$target" != *"/"* && "$target" != *"."* ]]; then
        continue
      fi
      # 解析相对路径（macOS 无 realpath，用 python3 兜底）
      resolved=$(python3 -c "import os,sys;print(os.path.normpath(os.path.join(sys.argv[1], sys.argv[2])))" "$dir" "$target" 2>/dev/null)
      if [[ -n "$resolved" && ! -e "$resolved" ]]; then
        echo -e "  ${RED}坏链: ${html_file#./} -> $target${NC}"
        broken_links+=("${html_file#./} -> $target")
      fi
    done < <(grep -oE '(href|src)="[^"]*"' "$html_file" | sed -E 's/.*="([^"]*)"/\1/')
  done < <(find . -name "*.html" -print0)

  echo "--------------------------------------------------"
  broken_count=${#broken_links[@]}
  if [[ $broken_count -eq 0 ]]; then
    echo -e "  ${GREEN}✓ 未发现坏链${NC}"
  else
    echo -e "  ${RED}坏链共 $broken_count 处${NC}"
    fail_flag=1
  fi
fi

# ------------------------------------------------------------------
# 步骤 3：扫描疑似密钥 / 敏感信息
# ------------------------------------------------------------------
if $RUN_STEP3; then
  echo
  echo -e "${CYAN}[步骤 3] 扫描疑似密钥 / 敏感信息${NC}"
  echo "--------------------------------------------------"
  secret_hits=()
  pattern=$(IFS='|'; echo "${SECRET_PATTERNS[*]}")
  while IFS= read -r -d '' f; do
    should_skip "$f" && continue
    # 仅扫描“可能存放真实密钥”的代码 / 配置文件类型
    fext="${f##*.}"
    is_code=0
    for ce in "${CODE_EXT[@]}"; do
      if [[ "$fext" == "$ce" ]]; then is_code=1; break; fi
    done
    [[ $is_code -eq 1 ]] || continue
    # -I 跳过二进制，-i 大小写不敏感，-n 带行号，-E 扩展正则
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      echo -e "  ${RED}敏感信息: $line${NC}"
      secret_hits+=("$line")
    done < <(grep -IniE "$pattern" "$f" 2>/dev/null)
  done < <(find . -type f -print0)

  echo "--------------------------------------------------"
  secret_count=${#secret_hits[@]}
  if [[ $secret_count -eq 0 ]]; then
    echo -e "  ${GREEN}✓ 未发现疑似密钥 / 敏感信息${NC}"
  else
    echo -e "  ${RED}疑似敏感信息共 $secret_count 处${NC}"
    fail_flag=1
  fi
fi

# ------------------------------------------------------------------
# 汇总
# ------------------------------------------------------------------
echo
echo "=============================="
echo -e "${CYAN}安全检查完成！${NC}"
echo "非 HTML 文件 : $non_html_count"
echo "坏链         : $broken_count"
echo "敏感信息     : $secret_count"
if [[ $fail_flag -eq 1 ]]; then
  echo -e "${RED}存在问题，请检查上方输出。${NC}"
  exit 1
else
  echo -e "${GREEN}未发现问题。${NC}"
  exit 0
fi
