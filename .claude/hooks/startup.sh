#!/bin/bash
# SessionStart — 展示项目当前状态，帮助快速恢复上下文

PROJ="$CLAUDE_PROJECT_DIR"

echo "0" > "$CLAUDE_PROJECT_DIR/.claude/.edit_count"
# 清除上轮会话的技能触发标记，确保新会话重新自动触发
rm -f "$CLAUDE_PROJECT_DIR/.claude/.skill_triggered_"*
echo "━━━ 项目状态 ━━━"

# Git 状态
echo ""
echo "📋 Git 状态:"
cd "$PROJ"
CHANGED=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$CHANGED" -gt 0 ]; then
  echo "  ⚠ 未提交更改: $CHANGED 个文件"
  git status --short 2>/dev/null | head -15
else
  echo "  ✅ 工作区干净"
fi

# 最近提交
echo ""
echo "📝 最近提交:"
git log --oneline -5 2>/dev/null || echo "  (尚无提交)"

# 章节
echo ""
echo "📖 章节:"
if [ -d "$PROJ/正文" ]; then
  CHAPTERS=$(ls "$PROJ/正文/"*.md 2>/dev/null | wc -l)
  echo "  共 $CHAPTERS 章"
  ls "$PROJ/正文/"*.md 2>/dev/null | head -10 | while read f; do
    WORDS=$(wc -m < "$f" 2>/dev/null)
    echo "  $(basename "$f") — $WORDS 字"
  done
else
  echo "  (正文/ 目录为空)"
fi

# 角色
echo ""
echo "👤 角色卡:"
if [ -d "$PROJ/角色设定" ]; then
  ls "$PROJ/角色设定/"*.md 2>/dev/null | while read f; do
    echo "  $(basename "$f" .md)"
  done
else
  echo "  (尚无角色卡)"
fi

echo ""
echo "━━━━━━━━━━━━━━"
exit 0
