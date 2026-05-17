# MCP 配置说明

## 已安装的 MCP 服务器

### 1. fanfic-helper（自定义）⭐ 核心
**功能**：同人项目管理——角色查询、章节统计、伏笔追踪、全文搜索、写作统计

**安装**：
```powershell
cd D:\写同人小说
pip install mcp
```

**配置**：已包含在 `mcp-config.json` 中

**提供的工具（15个）**：
| 工具 | 功能 |
|------|------|
| `list_characters` | 列出所有角色及基本信息 |
| `get_character` | 读取指定角色的完整设定卡 |
| `search_characters` | 在所有角色卡中搜索关键词 |
| `list_chapters` | 列出所有章节及字数 |
| `get_chapter` | 读取指定章节完整内容 |
| `get_chapter_stats` | 章节统计（总字数/平均/最多/最少） |
| `get_foreshadowing` | 读取完整伏笔台账 |
| `get_foreshadowing_by_status` | 按状态筛选伏笔 |
| `check_overdue_hooks` | 检查逾期未回收伏笔 |
| `get_emotional_arc` | 读取指定角色的情绪追踪 |
| `search_project` | 全文搜索（可限定范围） |
| `get_outline` | 读取整体大纲 |
| `list_worldbuilding` | 列出世界观设定文件 |
| `get_worldbuilding` | 读取指定世界观文件 |
| `get_writing_stats` | 总体写作统计 |
| `project_overview` | 项目全貌一览 |

---

### 2. Brave Search MCP 🔍
**功能**：免费网络搜索，用于查找原作资料、参考同人作品
**安装**：获取免费 API key: https://brave.com/search/api/
**用途**：
- 搜索原作设定、角色信息
- 查找参考同人作品
- 搜索写作技巧、类型惯例

---

### 3. Memory MCP 🧠
**功能**：持久化记忆存储，跨会话保持上下文
**用途**：
- 记住角色设定要点
- 存储创作偏好和风格指南
- 记录各平台发布规则

---

### 4. Sequential Thinking MCP 💭
**功能**：深度推理，适合复杂剧情设计
**用途**：
- 设计复杂的伏笔网络
- 推演角色决策的连锁影响
- 分析剧情逻辑一致性

---

### 5. Fetch MCP 📄
**功能**：抓取网页内容转为 Markdown
**用途**：
- 抓取原作wiki/百科内容
- 读取网上公开的同人作品
- 获取写作参考资料

---

## 推荐组合

### 最小配置（2个）
```
fanfic-helper + memory
→ 项目管理 + 跨会话记忆
```

### 标准配置（4个）
```
fanfic-helper + memory + brave-search + fetch
→ 项目管理 + 记忆 + 搜索 + 网页抓取
```

### 完整配置（5个）
```
全部 5 个
→ 加上 sequential-thinking 处理复杂剧情推理
```

---

## 安装步骤

### 1. 安装 Python 依赖
```powershell
pip install mcp
```

### 2. 获取 Brave Search API Key（可选）
访问 https://brave.com/search/api/ 注册免费账号，获取 API key

### 3. 配置 Claude Code
将 `mcp-config.json` 的内容合并到 Claude Code 的 MCP 配置中：
- 项目级：`.claude/mcp.json`
- 用户级：`~/.claude/mcp.json`

### 4. 测试
重启 Claude Code 后，询问：
- "列出我的所有角色"
- "项目总字数是多少"
- "有哪些逾期伏笔"

---

## MCP vs Skill 分工

| 场景 | 用 MCP | 用 Skill |
|------|--------|----------|
| 查询角色/统计/搜索文件 | ✅ `fanfic-helper` | — |
| 创建角色卡 | — | ✅ `character-profile` |
| 扩写正文 | — | ✅ `expand-scene` |
| 搜索原作资料 | ✅ `brave-search` | — |
| 分析作品技法 | — | ✅ `story-analyze` |
| 跨会话记住设定 | ✅ `memory` | — |
| 深度剧情推演 | ✅ `sequential-thinking` | — |
| 润色文本 | — | ✅ `polish-text` |

**简单规则**：
- MCP = **数据操作**（读/写/搜索/统计）
- Skill = **创意生成**（写/改/分析/规划）
