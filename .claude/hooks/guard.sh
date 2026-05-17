#!/bin/bash
# PreToolUse on Bash — 拦截危险命令

INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

# 危险模式
BLOCKED="rm -rf /|DROP TABLE|DROP DATABASE|mkfs\.|> /dev/sd|--no-verify|git push --force"

for pattern in $(echo "$BLOCKED" | tr '|' '\n'); do
  if echo "$CMD" | grep -qi "$pattern"; then
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"危险命令已拦截: $pattern\"}}"
    exit 0
  fi
done

# 允许
echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\"}}"
exit 0
