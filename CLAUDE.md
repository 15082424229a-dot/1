# 同人小说

> Inherits the global writing ecosystem: 5 MCP servers + 13 global skills.
> See `~/.claude/CLAUDE.md` for the full skill/MCP inventory and dispatch table.

## Project Skills (7) — Fanfic-Specific

Location: `.claude/skills/`

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `writing-workflow` | Master scheduler — stage-gated process from idea to final polish | "开始写作"、"创作流程" |
| `character-profile` | Character card with voice/style profile | "创建角色XX"、"回顾XX设定" |
| `worldbuilding` | World / AU / factions / hard & soft rules | "构建世界观"、"这是AU" |
| `chapter-outline` | Three-act structure + per-chapter breakdown | "规划大纲"、"写第X章大纲" |
| `chapter-bridge` | Context recovery + inter-chapter bridging | "准备写第X章" |
| `continuity-check` | 12-dimension audit + fandom-specific checks | "连续性检查"、"检查穿帮" |
| `emotional-arc` | Per-character emotion curve + relationship temperature | "情绪追踪"、"查看情感弧线" |

## Project Layout

```
├── CLAUDE.md
├── .claude/
│   ├── settings.json        ← Project config + hooks
│   ├── hooks/               ← 4 workflow automation scripts
│   └── skills/              ← 7 project skills
├── mcp/
│   ├── fanfic-helper/       ← Custom MCP server source
│   ├── mcp-config.json      ← All 5 MCP server configs
│   └── README.md            ← MCP documentation
├── 角色设定/[角色名].md       ← One card per character
├── 世界观/*.md               ← Canon / AU / factions / rules
├── 大纲/
│   ├── 整体大纲.md           ← Master outline
│   ├── 伏笔台账.md           ← Foreshadowing ledger (A/B/C)
│   └── 情绪追踪.md           ← Emotional tracking per character
└── 正文/第X章.md             ← Chapter drafts
```

## Data Flow

```
角色设定/*.md  →  expand-scene / dialogue-craft / continuity-check / emotional-arc
世界观/*.md     →  expand-scene / continuity-check
大纲/整体大纲.md →  chapter-bridge / expand-scene / continuity-check
大纲/伏笔台账.md →  chapter-bridge / expand-scene / continuity-check
大纲/情绪追踪.md →  chapter-bridge / continuity-check / pacing-ecg
```

## Hooks (4)

Automated workflow reminders via `.claude/settings.json` + `.claude/hooks/*.sh`.

| Hook | Trigger | Does |
|------|---------|------|
| `startup.sh` | SessionStart | Dashboard: git status + chapter list + character count |
| `post-edit.sh` | PostToolUse (Write\|Edit) | Reminds: continuity-check → foreshadowing → commit |
| `pre-stop.sh` | Stop | Warns if uncommitted changes exist |
| `guard.sh` | PreToolUse (Bash) | Blocks dangerous commands (rm -rf /, force push, etc.) |

## Quick Start

```
"开始写作"          → Full workflow from stage 0
"创建角色XX"        → Character profile card
"规划大纲"          → Three-act + chapter outline
"准备写第N章"       → Context recovery, ready to draft
"扩写：[scene]"     → Scene → prose (global skill)
"连续性检查"        → 12-dimension audit
"去AI味"           → Remove AI-slop (global skill)
"记一个灵感"        → Capture idea (global skill)
```

## Conventions

1. **Every chapter → continuity check.** Bugs compound if skipped.
2. **Foreshadowing is live.** Log when planted, update when resolved — same session.
3. **Emotion tracking is sparse.** Key turning points only, not every chapter.
4. **De-AI is the final pass.** Write first, de-slop last.
5. **MCP = data ops** (read/search/stats). **Skill = creative ops** (write/edit/plan/analyze).
6. **Author retains final say.** All skills and tools are advisory.
