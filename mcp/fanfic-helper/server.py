"""
同人写作助手 MCP Server
提供角色管理、章节统计、伏笔追踪、全文搜索等功能。
"""
import os
import re
import json
import glob
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

# ---- 配置 ----
PROJECT_ROOT = Path(os.environ.get("FANFIC_PROJECT", r"D:\写同人小说"))
CHAR_DIR = PROJECT_ROOT / "角色设定"
OUTLINE_DIR = PROJECT_ROOT / "大纲"
CHAPTER_DIR = PROJECT_ROOT / "正文"
WORLD_DIR = PROJECT_ROOT / "世界观"

server = Server("fanfic-helper")


# ==================== 工具函数 ====================

def _read_file(path: Path) -> str:
    """安全读取文件，UTF-8"""
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _list_md_files(directory: Path) -> list[Path]:
    """列出目录下所有 .md 文件"""
    if not directory.exists():
        return []
    return sorted(directory.glob("*.md"))


def _count_words(text: str) -> int:
    """统计中文字数（去标点和空白）"""
    # 匹配中文字符
    chinese_chars = re.findall(r'[一-鿿]', text)
    # 匹配英文单词
    english_words = re.findall(r'[a-zA-Z]+', text)
    return len(chinese_chars) + len(english_words)


def _extract_title(content: str) -> str:
    """从 markdown 提取一级标题"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "未知"


def _search_in_file(path: Path, query: str) -> list[dict]:
    """在文件中搜索，返回匹配行及上下文"""
    content = _read_file(path)
    if not content:
        return []
    lines = content.split("\n")
    results = []
    for i, line in enumerate(lines):
        if query.lower() in line.lower():
            start = max(0, i - 1)
            end = min(len(lines), i + 2)
            context = "\n".join(lines[start:end])
            results.append({
                "file": str(path.relative_to(PROJECT_ROOT)),
                "line": i + 1,
                "match": line.strip(),
                "context": context,
            })
    return results


# ==================== MCP Tools ====================

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # --- 角色 ---
        Tool(
            name="list_characters",
            description="列出所有角色及其基本信息",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_character",
            description="读取指定角色的完整设定卡",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "角色名（文件名不含扩展名）"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="search_characters",
            description="在所有角色卡中搜索关键词（如技能、关系、背景）",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                },
                "required": ["query"],
            },
        ),
        # --- 章节 ---
        Tool(
            name="list_chapters",
            description="列出所有章节文件及字数统计",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_chapter",
            description="读取指定章节的完整内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "chapter": {"type": "string", "description": "章节号（如 1, 2, 3）或文件名"},
                },
                "required": ["chapter"],
            },
        ),
        Tool(
            name="get_chapter_stats",
            description="获取章节统计：总字数、平均每章字数、章节数",
            inputSchema={"type": "object", "properties": {}},
        ),
        # --- 伏笔 ---
        Tool(
            name="get_foreshadowing",
            description="读取伏笔台账，查看所有伏笔状态",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_foreshadowing_by_status",
            description="按状态筛选伏笔",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "状态：已埋 / 部分揭露 / 已回收 / 逾期",
                    },
                },
                "required": ["status"],
            },
        ),
        Tool(
            name="check_overdue_hooks",
            description="检查是否有逾期未回收的伏笔",
            inputSchema={"type": "object", "properties": {}},
        ),
        # --- 情绪追踪 ---
        Tool(
            name="get_emotional_arc",
            description="读取指定角色的情绪追踪数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "character": {"type": "string", "description": "角色名"},
                },
                "required": ["character"],
            },
        ),
        # --- 全文搜索 ---
        Tool(
            name="search_project",
            description="在所有项目文件中全文搜索关键词",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "scope": {
                        "type": "string",
                        "description": "搜索范围：all / characters / chapters / outline / worldbuilding",
                        "default": "all",
                    },
                },
                "required": ["query"],
            },
        ),
        # --- 大纲 ---
        Tool(
            name="get_outline",
            description="读取整体大纲文件",
            inputSchema={"type": "object", "properties": {}},
        ),
        # --- 世界观 ---
        Tool(
            name="list_worldbuilding",
            description="列出所有世界观设定文件",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_worldbuilding",
            description="读取指定的世界观设定文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "文件名（如 原作设定, 本文私设, 势力格局）"},
                },
                "required": ["file"],
            },
        ),
        # --- 写作统计 ---
        Tool(
            name="get_writing_stats",
            description="获取整体写作统计：总字数、章节数、角色数、伏笔数、创作天数",
            inputSchema={"type": "object", "properties": {}},
        ),
        # --- 项目概览 ---
        Tool(
            name="project_overview",
            description="获取项目全貌：所有角色+所有章节+伏笔状态+写作统计的一次性汇总",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    result = ""

    # --- 角色 ---
    if name == "list_characters":
        files = _list_md_files(CHAR_DIR)
        if not files:
            result = "📭 暂无角色设定。使用 character-profile skill 创建。"
        else:
            lines = [f"## 角色列表（共 {len(files)} 个）\n"]
            for f in files:
                content = _read_file(f)
                title = _extract_title(content)
                # 提取基本信息行
                info_lines = []
                for line in content.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("- 原作：") or stripped.startswith("- 性别：") or stripped.startswith("- 身份"):
                        info_lines.append(stripped)
                lines.append(f"### {title} (`角色设定/{f.name}`)")
                for il in info_lines[:3]:
                    lines.append(f"  {il}")
                lines.append("")
            result = "\n".join(lines)

    elif name == "get_character":
        name_arg = arguments["name"]
        path = CHAR_DIR / f"{name_arg}.md"
        if path.exists():
            result = _read_file(path)
        else:
            # 模糊搜索
            files = _list_md_files(CHAR_DIR)
            matches = [f for f in files if name_arg in f.stem]
            if matches:
                result = _read_file(matches[0])
            else:
                result = f"❌ 未找到角色 '{name_arg}'。使用 list_characters 查看所有角色。"

    elif name == "search_characters":
        query = arguments["query"]
        results = []
        for f in _list_md_files(CHAR_DIR):
            results.extend(_search_in_file(f, query))
        if results:
            lines = [f"## 在角色卡中搜索 '{query}'：{len(results)} 条匹配\n"]
            for r in results[:20]:
                lines.append(f"- **{r['file']}** (第{r['line']}行): {r['match'][:100]}")
            result = "\n".join(lines)
        else:
            result = f"🔍 在角色卡中未找到 '{query}'"

    # --- 章节 ---
    elif name == "list_chapters":
        files = _list_md_files(CHAPTER_DIR)
        if not files:
            result = "📭 暂无章节。使用 expand-scene skill 开始写作。"
        else:
            lines = [f"## 章节列表（共 {len(files)} 章）\n"]
            lines.append("| 章节 | 标题 | 字数 |")
            lines.append("|------|------|------|")
            total_words = 0
            for f in files:
                content = _read_file(f)
                title = _extract_title(content)
                words = _count_words(content)
                total_words += words
                lines.append(f"| {f.stem} | {title} | {words:,} |")
            lines.append(f"\n**总字数：{total_words:,}**")
            result = "\n".join(lines)

    elif name == "get_chapter":
        ch = arguments["chapter"]
        # 尝试多种文件名匹配
        path = CHAPTER_DIR / f"{ch}.md"
        if not path.exists():
            files = _list_md_files(CHAPTER_DIR)
            matches = [f for f in files if ch in f.stem]
            if matches:
                path = matches[0]
        if path.exists():
            content = _read_file(path)
            words = _count_words(content)
            result = f"## {_extract_title(content)}\n字数：{words:,}\n\n{content}"
        else:
            result = f"❌ 未找到第 {ch} 章。使用 list_chapters 查看所有章节。"

    elif name == "get_chapter_stats":
        files = _list_md_files(CHAPTER_DIR)
        if not files:
            result = "📭 暂无章节。"
        else:
            word_counts = []
            for f in files:
                wc = _count_words(_read_file(f))
                word_counts.append((f.stem, wc))
            total = sum(w for _, w in word_counts)
            avg = total // len(word_counts)
            max_ch = max(word_counts, key=lambda x: x[1])
            min_ch = min(word_counts, key=lambda x: x[1])
            lines = [
                f"## 章节统计",
                f"- 总章节数：{len(files)}",
                f"- 总字数：{total:,}",
                f"- 平均每章：{avg:,} 字",
                f"- 最长章节：{max_ch[0]}（{max_ch[1]:,} 字）",
                f"- 最短章节：{min_ch[0]}（{min_ch[1]:,} 字）",
            ]
            result = "\n".join(lines)

    # --- 伏笔 ---
    elif name == "get_foreshadowing":
        path = OUTLINE_DIR / "伏笔台账.md"
        if path.exists():
            result = _read_file(path)
        else:
            result = "📭 暂无伏笔台账。使用 foreshadowing-tracker skill 创建。"

    elif name == "get_foreshadowing_by_status":
        status = arguments["status"]
        path = OUTLINE_DIR / "伏笔台账.md"
        if not path.exists():
            result = "📭 暂无伏笔台账。"
        else:
            content = _read_file(path)
            # 按 F### 分割伏笔条目
            entries = re.split(r'\n(?=### F\d+)', content)
            matched = []
            for entry in entries:
                if f"状态**：`{status}`" in entry or f"状态**：{status}" in entry:
                    # 提取标题行
                    title_match = re.search(r'### (F\d+: .+)', entry)
                    title = title_match.group(1) if title_match else entry[:80]
                    matched.append(title)
            if matched:
                lines = [f"## 状态为 '{status}' 的伏笔（{len(matched)} 条）\n"]
                for m in matched:
                    lines.append(f"- {m}")
                result = "\n".join(lines)
            else:
                result = f"📭 没有状态为 '{status}' 的伏笔。"

    elif name == "check_overdue_hooks":
        path = OUTLINE_DIR / "伏笔台账.md"
        if not path.exists():
            result = "📭 暂无伏笔台账。"
        else:
            content = _read_file(path)
            entries = re.split(r'\n(?=### F\d+)', content)
            overdue = []
            for entry in entries:
                if "⚠️逾期" in entry:
                    title_match = re.search(r'### (F\d+: .+)', entry)
                    title = title_match.group(1) if title_match else entry[:80]
                    overdue.append(title)
            if overdue:
                lines = [f"## ⚠️ 逾期未回收的伏笔（{len(overdue)} 条）\n"]
                for o in overdue:
                    lines.append(f"- {o}")
                lines.append("\n⚠️ 建议尽快回收或更新预计回收章节。")
                result = "\n".join(lines)
            else:
                result = "✅ 目前没有逾期未回收的伏笔。"

    # --- 情绪追踪 ---
    elif name == "get_emotional_arc":
        char = arguments["character"]
        path = OUTLINE_DIR / "情绪追踪.md"
        if not path.exists():
            result = "📭 暂无情绪追踪数据。使用 emotional-arc skill 创建。"
        else:
            content = _read_file(path)
            # 提取指定角色的信息
            pattern = rf'## {re.escape(char)}\b(.*?)(?=\n## |\Z)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                result = f"## {char} 的情绪追踪\n\n{match.group(0)}"
            else:
                result = f"❌ 未找到角色 '{char}' 的情绪数据。检查角色名是否正确。"

    # --- 全文搜索 ---
    elif name == "search_project":
        query = arguments["query"]
        scope = arguments.get("scope", "all")
        search_dirs = []
        if scope == "all":
            search_dirs = [CHAR_DIR, CHAPTER_DIR, OUTLINE_DIR, WORLD_DIR]
        elif scope == "characters":
            search_dirs = [CHAR_DIR]
        elif scope == "chapters":
            search_dirs = [CHAPTER_DIR]
        elif scope == "outline":
            search_dirs = [OUTLINE_DIR]
        elif scope == "worldbuilding":
            search_dirs = [WORLD_DIR]

        all_results = []
        for d in search_dirs:
            for f in _list_md_files(d):
                all_results.extend(_search_in_file(f, query))

        if all_results:
            lines = [f"## 搜索 '{query}'：{len(all_results)} 条匹配\n"]
            for r in all_results[:30]:
                lines.append(
                    f"### 📄 {r['file']} (第{r['line']}行)\n"
                    f"```\n{r['context']}\n```\n"
                )
            if len(all_results) > 30:
                lines.append(f"\n...（还有 {len(all_results) - 30} 条结果）")
            result = "\n".join(lines)
        else:
            result = f"🔍 在整个项目中未找到 '{query}'"

    # --- 大纲 ---
    elif name == "get_outline":
        path = OUTLINE_DIR / "整体大纲.md"
        if path.exists():
            result = _read_file(path)
        else:
            # 尝试其他大纲文件
            files = _list_md_files(OUTLINE_DIR)
            if files:
                result = _read_file(files[0])
            else:
                result = "📭 暂无大纲文件。使用 chapter-outline skill 创建。"

    # --- 世界观 ---
    elif name == "list_worldbuilding":
        files = _list_md_files(WORLD_DIR)
        if not files:
            result = "📭 暂无世界观设定。使用 worldbuilding skill 创建。"
        else:
            lines = [f"## 世界观设定文件（共 {len(files)} 个）\n"]
            for f in files:
                content = _read_file(f)
                title = _extract_title(content)
                words = _count_words(content)
                lines.append(f"- **{title}** (`世界观/{f.name}`) — {words} 字")
            result = "\n".join(lines)

    elif name == "get_worldbuilding":
        file_arg = arguments["file"]
        path = WORLD_DIR / f"{file_arg}.md"
        if not path.exists():
            # 模糊搜索
            files = _list_md_files(WORLD_DIR)
            matches = [f for f in files if file_arg in f.stem]
            if matches:
                path = matches[0]
        if path.exists():
            result = _read_file(path)
        else:
            result = f"❌ 未找到世界观文件 '{file_arg}'。使用 list_worldbuilding 查看。"

    # --- 写作统计 ---
    elif name == "get_writing_stats":
        ch_files = _list_md_files(CHAPTER_DIR)
        char_files = _list_md_files(CHAR_DIR)
        world_files = _list_md_files(WORLD_DIR)

        total_words = sum(_count_words(_read_file(f)) for f in ch_files)

        # 创作天数（最早文件修改时间到最新）
        all_files = ch_files + char_files + list(OUTLINE_DIR.glob("*.md"))
        if all_files:
            mtimes = [f.stat().st_mtime for f in all_files if f.exists()]
            if mtimes:
                earliest = datetime.fromtimestamp(min(mtimes))
                latest = datetime.fromtimestamp(max(mtimes))
                days = (latest - earliest).days + 1
            else:
                earliest = latest = datetime.now()
                days = 0
        else:
            earliest = latest = datetime.now()
            days = 0

        # 伏笔统计
        foreshadowing_count = 0
        overdue_count = 0
        fs_path = OUTLINE_DIR / "伏笔台账.md"
        if fs_path.exists():
            content = _read_file(fs_path)
            foreshadowing_count = len(re.findall(r'### F\d+:', content))
            overdue_count = len(re.findall(r'⚠️逾期', content))

        lines = [
            "## 📊 写作统计",
            "",
            "| 指标 | 数值 |",
            "|------|------|",
            f"| 📝 总字数 | {total_words:,} |",
            f"| 📖 章节数 | {len(ch_files)} |",
            f"| 👤 角色数 | {len(char_files)} |",
            f"| 🌍 世界观文件数 | {len(world_files)} |",
            f"| 🎯 伏笔总数 | {foreshadowing_count} |",
            f"| ⚠️ 逾期伏笔 | {overdue_count} |",
            f"| 📅 创作天数 | {days} 天 |",
            f"| 📅 最早创作 | {earliest.strftime('%Y-%m-%d')} |",
            f"| 📅 最近更新 | {latest.strftime('%Y-%m-%d')} |",
            "",
        ]
        if ch_files:
            avg = total_words // len(ch_files)
            lines.append(f"📏 平均每章：{avg:,} 字")
            if avg < 2000:
                lines.append("   💡 建议：每章增加至2000-5000字，读者体验更好")
            elif avg > 8000:
                lines.append("   💡 建议：考虑拆分过长章节，减轻单章阅读压力")

        result = "\n".join(lines)

    # --- 项目概览 ---
    elif name == "project_overview":
        ch_files = _list_md_files(CHAPTER_DIR)
        char_files = _list_md_files(CHAR_DIR)
        total_words = sum(_count_words(_read_file(f)) for f in ch_files)

        # 角色
        char_names = [_extract_title(_read_file(f)) for f in char_files]

        # 章节
        ch_summary = []
        for f in ch_files:
            wc = _count_words(_read_file(f))
            ch_summary.append(f"{f.stem} ({wc:,}字)")

        # 伏笔
        fs_path = OUTLINE_DIR / "伏笔台账.md"
        fs_summary = "无"
        if fs_path.exists():
            content = _read_file(fs_path)
            planted = len(re.findall(r'🌱已埋', content))
            partial = len(re.findall(r'🌿部分揭露', content))
            done = len(re.findall(r'✅已回收', content))
            overdue = len(re.findall(r'⚠️逾期', content))
            fs_summary = f"已埋:{planted} / 部分揭露:{partial} / 已回收:{done} / 逾期:{overdue}"

        lines = [
            "# 📋 项目全貌",
            "",
            "## 📊 核心数据",
            f"- 总字数：{total_words:,}",
            f"- 章节数：{len(ch_files)}",
            f"- 角色数：{len(char_files)}",
            "",
            "## 👤 角色",
            ", ".join(char_names) if char_names else "暂无",
            "",
            "## 📖 章节进度",
        ]
        for s in ch_summary:
            lines.append(f"- 第{s}")
        if not ch_summary:
            lines.append("暂无")
        lines.extend([
            "",
            f"## 🎯 伏笔状态",
            fs_summary,
        ])
        result = "\n".join(lines)

    return [TextContent(type="text", text=result)]


# ==================== 启动 ====================

def main():
    import asyncio
    async def run():
        async with stdio_server() as (read, write):
            await server.run(read, write)
    asyncio.run(run())


if __name__ == "__main__":
    main()
