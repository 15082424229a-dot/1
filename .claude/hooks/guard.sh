#!/bin/bash
# PreToolUse on Bash — 拦截危险命令

INPUT=$(head -c 65536)

# Python 探测：Windows 上只有 python 没有 python3
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || echo "")

if [ -n "$PYTHON" ]; then
  CMD=$(printf '%s\n' "$INPUT" | "$PYTHON" -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)
else
  # fallback: 用 sed 从 JSON 中提取 command 字段
  CMD=$(printf '%s\n' "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi

# 危险模式
BLOCKED="rm -rf /|DROP TABLE|DROP DATABASE|mkfs\.|> /dev/sd|--no-verify"

# 使用 | 分隔符读入数组，避免含空格的模式被单词拆分
IFS='|' read -ra PATTERNS <<< "$BLOCKED"
for pattern in "${PATTERNS[@]}"; do
  if printf '%s\n' "$CMD" | grep -qi "$pattern"; then
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"危险命令已拦截: $pattern\"}}"
    exit 0
  fi
done

# git push --force 单独检查：允许 --force-with-lease（会检查远程是否前进），只拦截裸 --force
if printf '%s\n' "$CMD" | grep -qi "git push" && printf '%s\n' "$CMD" | grep -qi -- "--force" && ! printf '%s\n' "$CMD" | grep -qi -- "--force-with-lease"; then
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"危险命令已拦截: git push --force（允许 --force-with-lease）\"}}"
  exit 0
fi

# 允许
echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\"}}"
exit 0
