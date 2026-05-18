# 同人小说写作项目

> **层级**: PROJECT — 所有 21 个技能均位于本项目 `.claude/skills/`，无全局/项目区分。
> **工作风格、MCP、版本管理** 见 `~/.claude/CLAUDE.md`。

---

## 技能（21 个）

路径：`.claude/skills/`

### 写作（5）
| 技能 | 用途 | 触发词 |
|------|------|--------|
| `expand-scene` | 场景大纲→完整正文 | "扩写"、"展开这个场景" |
| `dialogue-craft` | 对话精修（声线、潜台词、节奏） | "精修对话" |
| `hook-designer` | 13 种章末钩子模式 | "设计钩子"、"结尾怎么卡" |
| `polish-text` | 表层润色：语法、流畅度、词汇 | "润色"、"深度润色" |
| `deai-slop` | 去 AI 措辞和塑料感 | "去AI味"、"塑料感太重" |

### 分析（3）
| 技能 | 用途 | 触发词 |
|------|------|--------|
| `story-analyze` | 拆解已发布作品，提取可复用技法 | "拆文"、"全面拆解" |
| `pacing-ecg` | 情绪心电图——压力/释放节奏诊断 | "节奏分析"、"心电图" |
| `foreshadowing-tracker` | A/B/C 优先级伏笔台账 + 逾期提醒 | "埋一个伏笔"、"查看所有伏笔" |

### 辅助（3）
| 技能 | 用途 | 触发词 |
|------|------|--------|
| `idea-capture` | 捕捉和整理灵感碎片 | "记一个灵感"、"有个脑洞" |
| `title-synopsis` | 标题 / 简介 / 标签 / 平台文案 | "起标题"、"写文案"、"设计简介" |
| `sensitive-tag` | 敏感内容预警 + 平台适配 | "检查敏感内容"、"帮我标tag" |

### 项目专属（8）
| 技能 | 用途 | 触发词 |
|------|------|--------|
| `writing-workflow` | 主调度器——分阶段流程：灵感→润色 | "开始写作"、"创作流程" |
| `character-profile` | 角色卡，含声线/风格画像 | "创建角色XX"、"回顾XX设定" |
| `worldbuilding` | 世界观 / AU / 势力 / 硬软规则 | "构建世界观"、"这是AU" |
| `chapter-outline` | 三幕结构 + 逐章分解 | "规划大纲"、"写第X章大纲" |
| `chapter-bridge` | 上下文恢复 + 章节间衔接 | "准备写第X章" |
| `continuity-check` | 12 维度审计 + 原作向专项检查 | "连续性检查"、"检查穿帮" |
| `emotional-arc` | 逐角色情绪曲线 + 关系温度 | "情绪追踪"、"查看情感弧线" |
| `meme-fusion` | 实时搜索热门网络梗，自然融入正文 | "加梗"、"融梗"、"查梗"、"最近有什么梗" |

### 工具（2）
| 技能 | 用途 | 触发词 |
|------|------|--------|
| `find-skills` | 从技能生态发现和安装技能 | "找skill" |
| `skill-creator` | 创建、编辑、基准测试技能 | "创建skill"、"写一个skill" |

## 调度速查

| 问题 | 用这个 | 别用 |
|------|--------|------|
| 不知道从哪开始 | `writing-workflow` | — |
| 需要创建/回顾角色 | `character-profile` | — |
| 需要构建世界观/AU | `worldbuilding` | — |
| 需要规划章节结构 | `chapter-outline` | — |
| 章与章之间断了 | `chapter-bridge` | — |
| 怕有穿帮/矛盾 | `continuity-check` | — |
| 情感线不清晰 | `emotional-arc` | — |
| 想蹭热点/加网络梗 | `meme-fusion` | — |
| 对话感觉不对 | `dialogue-craft` | `polish-text` |
| 文字 AI 味太重 | `deai-slop` | `polish-text` |
| 章节结尾平淡 | `hook-designer` | — |
| 节奏拖沓 | `pacing-ecg` | — |
| 需要追踪伏笔 | `foreshadowing-tracker` | — |
| 需要标题/文案 | `title-synopsis` | — |
| 灵感一闪而过 | `idea-capture` | — |
| 需要内容标签 | `sensitive-tag` | — |

---

## MCP 服务器（2 个）

配置于 `.claude/mcp.json`。

| MCP | 工具数 | 用途 |
|-----|--------|------|
| `chinese-writing-aids` | 7 | 词典查询/同义词反义词/成语建议/语法检查/翻译腔检测/拼音 |
| `story-timeline-keeper` | 7 | 结构化时间线：事件录入/查询/角色轨迹/冲突检测/章节上下文 |


---

## 项目目录

```
├── CLAUDE.md                  ← 本文件
├── .claude/
│   ├── settings.json          ← 项目配置 + hooks
│   ├── hooks/                 ← 工作流自动化脚本
│   └── skills/                ← 项目技能（21 个 .md）
├── 角色设定/[角色名].md
├── 世界观/*.md
├── 大纲/
│   ├── 整体大纲.md
│   ├── 伏笔台账.md
│   └── 情绪追踪.md
└── 正文/第X章.md
```

---

## Hooks（5 个）

通过 `.claude/settings.json` + `.claude/hooks/*.sh` 实现。

| Hook | 触发时机 | 功能 |
|------|----------|------|
| `startup.sh` | 会话启动 | 仪表盘 + 清除上轮技能触发标记 |
| `pre-write.sh` | 写入/编辑前 | 首次写章节 → 强制输出 MANDATORY 指令，自动触发 10 技能链 |
| `post-edit.sh` | 写入/编辑后 | 编辑计数 + 连续性/伏笔/情绪提醒；超 5/10 次警告 |
| `pre-stop.sh` | 会话结束 | 未提交更改警告 |
| `guard.sh` | Bash 执行前 | 拦截 rm -rf /、force push 等危险命令 |

---

## 约定

1. **每写完一章 → 跑连续性检查。** 跳过会累积穿帮。
2. **伏笔即埋即登。** 埋设时登记，回收时更新。
3. **情绪追踪从简。** 只记关键转折点，不逐章记录。
4. **去 AI 味是最后一步。** 先写完，最后再去塑料感。
5. **Skill = 创意生成，作者最终拍板。** 所有技能都是建议工具。
