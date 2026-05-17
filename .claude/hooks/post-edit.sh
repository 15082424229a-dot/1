#!/bin/bash
# PostToolUse on Write|Edit — 修改写作文件后弹出检查清单提醒

# 从 stdin 读取工具调用信息
INPUT=$(cat)
FP=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# 只在修改了写作相关目录的文件时提醒
case "$FP" in
  *正文/*|*角色设定/*|*世界观/*|*大纲/*)
    echo ""
    echo "✏️  写作文件已修改: $(basename "$FP")"
    echo "   ✅ 连续性检查 (continuity-check)"
    echo "   ✅ 更新伏笔台账 (foreshadowing-tracker)"
    echo "   ✅ 更新情绪追踪 (emotional-arc)"
    echo "   ✅ git commit"
    ;;
esac
exit 0
