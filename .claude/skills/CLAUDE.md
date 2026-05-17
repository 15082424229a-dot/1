# Project Skills

These 7 skills (.md files) are fanfic-project-specific.
Global skills (11) live in `~/.claude/skills/` and apply to all writing projects.

## Skill File Format
```yaml
---
name: skill-name
description: one-line summary
---
```
Followed by the skill's system prompt / instructions in Markdown.

## When to Put a Skill Here vs Global
- **Here** (`.claude/skills/`) — tied to this fanfic project structure (roles, chapters, continuity, worldbuilding)
- **Global** (`~/.claude/skills/`) — generic writing craft (expand, polish, dialogue, pacing, hooks, etc.)

## Current Project Skills
| Skill | File |
|-------|------|
| `writing-workflow` | `writing-workflow.md` |
| `character-profile` | `character-profile.md` |
| `worldbuilding` | `worldbuilding.md` |
| `chapter-outline` | `chapter-outline.md` |
| `chapter-bridge` | `chapter-bridge.md` |
| `continuity-check` | `continuity-check.md` |
| `emotional-arc` | `emotional-arc.md` |
