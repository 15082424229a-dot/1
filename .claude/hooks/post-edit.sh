#!/bin/bash
# PostToolUse on Write|Edit — 修改写作文件后弹出检查清单提醒 + 会话编辑计数

INPUT=$(head -c 65536)

# Python 探测：Windows 上只有 python 没有 python3
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || echo "")

if [ -n "$PYTHON" ]; then
  FP=$(printf '%s\n' "$INPUT" | "$PYTHON" -c "
import sys, json
raw = sys.stdin.buffer.read().decode('utf-8')
d = json.loads(raw)
print(d.get('tool_input', {}).get('file_path', ''))
" 2>/dev/null)
else
  # fallback: 用 sed 从 JSON 中提取 file_path 字段
  FP=$(printf '%s\n' "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi

# 只在修改了写作相关目录的文件时提醒
case "$FP" in
  *正文/*|*角色设定/*|*世界观/*|*大纲/*)
    # --- 会话编辑计数器 ---
    COUNT_FILE="$CLAUDE_PROJECT_DIR/.claude/.edit_count"
    if [ -f "$COUNT_FILE" ]; then
      COUNT=$(cat "$COUNT_FILE" 2>/dev/null)
      COUNT=$((COUNT + 1))
    else
      COUNT=1
    fi
    echo "$COUNT" > "$COUNT_FILE"

    echo ""
    echo "✏️  写作文件已修改: $(basename "$FP") (本次会话第 ${COUNT} 次编辑)"
    echo "   ✅ 连续性检查 (continuity-check)"
    echo "   ✅ 更新伏笔台账 (foreshadowing-tracker)"
    echo "   ✅ 更新情绪追踪 (emotional-arc)"
    echo "   ✅ git commit"

    # 阈值提醒
    if [ "$COUNT" -eq 5 ]; then
      echo ""
      echo "⚠️  已写了不少，检查一下角色卡和伏笔台账"
    elif [ "$COUNT" -eq 10 ]; then
      echo ""
      echo "🚨 会话编辑量很大，建议 git commit 并考虑开新会话以释放上下文"
    elif [ "$COUNT" -gt 10 ]; then
      echo ""
      echo "🚨 已编辑 ${COUNT} 次，强烈建议 git commit 并开新会话以释放上下文"
    fi
    ;;
esac
exit 0
