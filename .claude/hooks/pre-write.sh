#!/bin/bash
# PreToolUse on Write|Edit — 首次写入章节时自动触发完整创作技能链
#
# 逻辑：
#   第一次编辑正文/第X章.md → 输出 MANDATORY 指令，强制 Claude 依次调用 10 个技能
#   后续编辑同一章 → 跳过（不重复触发）
#   编辑大纲 → 轻量提醒

INPUT=$(head -c 65536)
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || echo "")

if [ -n "$PYTHON" ]; then
  # Use printf + buffer.read for explicit UTF-8 handling across all platforms
  FP=$(printf '%s\n' "$INPUT" | "$PYTHON" -c "
import sys, json
raw = sys.stdin.buffer.read().decode('utf-8')
d = json.loads(raw)
print(d.get('tool_input', {}).get('file_path', ''))
" 2>/dev/null)
else
  FP=$(printf '%s\n' "$INPUT" | grep -o '"file_path"\s*:\s*"[^"]*"' | head -1 | sed 's/.*"file_path"\s*:\s*"\([^"]*\)".*/\1/')
fi

PROJ="$CLAUDE_PROJECT_DIR"

case "$FP" in
  *正文/*)
    CHAPTER=$(basename "$FP" .md)
    TRIGGERED="$PROJ/.claude/.skill_triggered_${CHAPTER}"

    if [ -f "$TRIGGERED" ]; then
      # 已触发过，静默放行
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\"}}"
      exit 0
    fi

    # 首次写入此章 → 标记已触发
    touch "$TRIGGERED"

    # 收集角色列表
    CHARS=""
    if ls "$PROJ/角色设定/"*.md >/dev/null 2>&1; then
      CHARS=$(ls "$PROJ/角色设定/"*.md 2>/dev/null | while read f; do basename "$f" .md; done | tr '\n' ' ')
    fi

    cat <<SKILL_TRIGGER

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  🚀 开始创作: ${CHAPTER}
║                                                                      ║
║  ── 项目状态 ────────────────────────────────────────────────────────║
║                                                                      ║
SKILL_TRIGGER

    if [ -n "$CHARS" ]; then
      echo "║  👤 可用角色: ${CHARS}"
      echo "║                                                                      ║"
    fi

    if [ -f "$PROJ/大纲/伏笔台账.md" ]; then
      echo "║  📌 伏笔台账就绪"
      echo "║                                                                      ║"
    fi

    if [ -f "$PROJ/大纲/情绪追踪.md" ]; then
      echo "║  📈 情绪追踪就绪"
      echo "║                                                                      ║"
    fi

    cat <<SKILL_TRIGGER
║                                                                      ║
║  ── PHASE 1: 写作前 — 恢复上下文 ───────────────────────────────────║
║                                                                      ║
║  ① Skill(skill="chapter-bridge")                                     ║
║     → 加载上一章摘要、验证钩子衔接、恢复角色位置/情绪状态             ║
║                                                                      ║
║  ── PHASE 2: 写作中 — 正文生成 ──────────────────────────────────────║
║     ⚠ 先完成本章初稿，再依次调用以下 4 个技能：                       ║
║                                                                      ║
║  ② Skill(skill="expand-scene")                                       ║
║     → 将场景大纲展开为完整正文                                       ║
║  ③ Skill(skill="dialogue-craft")                                     ║
║     → 对话精修：角色声线、潜台词、叙事节奏                           ║
║  ④ Skill(skill="hook-designer")                                      ║
║     → 设计章末钩子：冲突/悬念/反转/情绪共振                          ║
║  ⑤ Skill(skill="meme-fusion")                                        ║
║     → 搜索当下热梗 + 评估适配 + 自然融入正文                         ║
║                                                                      ║
║  ── PHASE 3: 写作后 — 质量打磨 ──────────────────────────────────────║
║     ⚠ 在正文初稿完成且 PHASE 2 技能全部执行后再调用：                ║
║                                                                      ║
║  ⑥ Skill(skill="continuity-check")                                   ║
║     → 12 维度穿帮审查：位置/时间/角色/道具/规则一致性                ║
║  ⑦ Skill(skill="polish-text")                                        ║
║     → 语法修正 + 流畅度优化 + 措辞升级                               ║
║  ⑧ Skill(skill="deai-slop")                                          ║
║     → 去除 AI 措辞、塑料感句式、翻译腔、模板化表达                   ║
║  ⑨ Skill(skill="pacing-ecg")                                         ║
║     → 情绪心电图：压力/释放节奏诊断 + 调峰建议                      ║
║  ⑩ Skill(skill="sensitive-tag")                                      ║
║     → 敏感内容预警 + 平台标签适配                                    ║
║                                                                      ║
║  ── 最终一步 ────────────────────────────────────────────────────────║
║                                                                      ║
║  git commit 保存本章 + 更新伏笔台账 + 更新情绪追踪                   ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  🔴 MANDATORY ACTION REQUIRED — 不可跳过                             ║
║                                                                      ║
║  你现在必须执行以下操作。这不是提示或建议，是必须完成的指令：         ║
║                                                                      ║
║  1. 立即调用 Skill(skill="chapter-bridge")                            ║
║     → 恢复上一章上下文，确认角色位置和情感状态                        ║
║                                                                      ║
║  2. 编写本章正文初稿                                                  ║
║                                                                      ║
║  3. 初稿完成后，按顺序调用以下技能：                                  ║
║     Skill(skill="expand-scene")                                       ║
║     Skill(skill="dialogue-craft")                                     ║
║     Skill(skill="hook-designer")                                      ║
║     Skill(skill="meme-fusion")                                        ║
║                                                                      ║
║  4. 正文定稿后，按顺序调用以下技能：                                  ║
║     Skill(skill="continuity-check")                                   ║
║     Skill(skill="polish-text")                                        ║
║     Skill(skill="deai-slop")                                          ║
║     Skill(skill="pacing-ecg")                                         ║
║     Skill(skill="sensitive-tag")                                      ║
║                                                                      ║
║  5. git commit 保存本章                                               ║
║                                                                      ║
║  ⛔ 禁止行为：                                                        ║
║     - 禁止说"建议运行以上技能"然后什么都不做                          ║
║     - 禁止跳过 PHASE 1 直接开始写正文                                 ║
║     - 禁止在 PHASE 2/3 完成前结束工作                                 ║
║     - 禁止只提醒而不实际调用 Skill 工具                               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
SKILL_TRIGGER
    ;;
  *大纲/*)
    cat <<OUTLINE_REMINDER

╔══════════════════════════════════════════════════════════════╗
║  📋 即将编辑大纲: $(basename "$FP")
║                                                              ║
║  💡 修改大纲后务必同步更新：                                  ║
║     - 伏笔台账 (大纲/伏笔台账.md)                            ║
║     - 情绪追踪 (大纲/情绪追踪.md)                            ║
║     - 受影响章节的角色位置/状态                              ║
╚══════════════════════════════════════════════════════════════╝
OUTLINE_REMINDER
    ;;
esac

echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\"}}"
exit 0
