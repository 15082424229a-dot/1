# Skills Index

20 个技能全部在同一目录，按类别组织。1 个 `skill-creator/` 子目录（含 agent、script、reference 等文件）。

## 写作（5）
| 技能 | 文件 | 用途 |
|------|------|------|
| `expand-scene` | `expand-scene.md` | 场景大纲 → 完整正文 |
| `dialogue-craft` | `dialogue-craft.md` | 对话精修：声线、潜台词、节奏 |
| `hook-designer` | `hook-designer.md` | 13 种章末钩子模式 |
| `polish-text` | `polish-text.md` | 表层润色：语法、流畅度、词汇 |
| `deai-slop` | `deai-slop.md` | 去 AI 措辞和塑料感 |

## 分析（3）
| 技能 | 文件 | 用途 |
|------|------|------|
| `story-analyze` | `story-analyze.md` | 拆解已发布作品，提取可复用技法 |
| `pacing-ecg` | `pacing-ecg.md` | 情绪心电图——压力/释放节奏诊断 |
| `foreshadowing-tracker` | `foreshadowing-tracker.md` | A/B/C 优先级伏笔台账 + 逾期提醒 |

## 辅助（3）
| 技能 | 文件 | 用途 |
|------|------|------|
| `idea-capture` | `idea-capture.md` | 捕捉和整理灵感碎片 |
| `title-synopsis` | `title-synopsis.md` | 标题 / 简介 / 标签 / 平台文案 |
| `sensitive-tag` | `sensitive-tag.md` | 敏感内容预警 + 平台适配 |

## 项目（8）
| 技能 | 文件 | 用途 |
|------|------|------|
| `writing-workflow` | `writing-workflow.md` | 主调度器——分阶段流程：灵感 → 润色 |
| `character-profile` | `character-profile.md` | 角色卡，含声线/风格画像 |
| `worldbuilding` | `worldbuilding.md` | 世界观 / AU / 势力 / 硬软规则 |
| `chapter-outline` | `chapter-outline.md` | 三幕结构 + 逐章分解 |
| `chapter-bridge` | `chapter-bridge.md` | 上下文恢复 + 章节间衔接 |
| `continuity-check` | `continuity-check.md` | 12 维度审计 + 原作向专项检查 |
| `emotional-arc` | `emotional-arc.md` | 逐角色情绪曲线 + 关系温度 |
| `meme-fusion` | `meme-fusion.md` | 梗融合：原作梗与现代/跨作品梗结合 |

## 工具（2）
| 技能 | 文件 | 用途 |
|------|------|------|
| `find-skills` | `find-skills.md` | 从技能生态发现和安装技能 |
| `skill-creator` | `skill-creator/` | 创建、编辑、基准测试技能（含子目录） |

## Skill File Format

每个 `.md` 技能文件使用 YAML frontmatter：

```yaml
---
name: skill-name
description: one-line summary
---
```

Frontmatter 之后是技能的 system prompt / 指令正文（Markdown）。

## 调度速查

| 问题 | 用这个 | 别用 |
|------|--------|------|
| 对话感觉不对 | `dialogue-craft` | `polish-text` |
| 文字 AI 味太重 | `deai-slop` | `polish-text` |
| 章节结尾平淡 | `hook-designer` | — |
| 节奏拖沓 | `pacing-ecg` | — |
| 需要追踪伏笔 | `foreshadowing-tracker` | — |
| 需要标题/文案 | `title-synopsis` | — |
| 灵感一闪而过 | `idea-capture` | — |
| 开始新章节 | `chapter-bridge` | — |
| 写完一章 | `continuity-check` | — |
