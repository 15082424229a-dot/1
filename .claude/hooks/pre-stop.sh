#!/bin/bash
# Stop — 会话结束前检查未提交更改

PROJ="$CLAUDE_PROJECT_DIR"
cd "$PROJ"

CHANGED=$(git status --porcelain 2>/dev/null | wc -l)
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l)

if [ "$CHANGED" -gt 0 ]; then
  echo ""
  echo "╔══════════════════════════╗"
  echo "║  ⚠  ️未提交的更改         ║"
  echo "║  修改: $(printf '%3d' $((CHANGED - UNTRACKED))) 个文件          ║"
  echo "║  新增: $(printf '%3d' $UNTRACKED) 个文件          ║"
  echo "║                         ║"
  echo "║  git add -A             ║"
  echo "║  git commit -m '...'    ║"
  echo "╚══════════════════════════╝"
  echo ""
fi
exit 0
