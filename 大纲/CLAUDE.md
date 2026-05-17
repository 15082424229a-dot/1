# 大纲 & 追踪

## Files
| File | Created By | Purpose |
|------|-----------|---------|
| `整体大纲.md` | `chapter-outline` | Three-act structure + per-chapter beats |
| `伏笔台账.md` | `foreshadowing-tracker` | A/B/C priority ledger — plant, status, resolution |
| `情绪追踪.md` | `emotional-arc` | Per-character emotion curve + relationship temperature |

## Conventions
- **Outline**: Mark key foreshadowing plant points and high-tension beats (爽点) inline
- **Foreshadowing**: Log immediately when planted; update status immediately when resolved. Never batch-defer updates
- **Emotions**: Record only key turning points. Sparse is better than noisy

## Data Consumers
- → `chapter-bridge` (context recovery: where are we? what's pending?)
- → `expand-scene` (scene-level guidance)
- → `continuity-check` (verify against plan)
- → `pacing-ecg` (emotional data for rhythm analysis)
