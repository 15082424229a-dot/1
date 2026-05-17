# MCP Configuration

Full documentation: `README.md`

## Quick Reference
- **`fanfic-helper`** — custom Python server (15 tools), source at `fanfic-helper/server.py`
- **`mcp-config.json`** — all 5 server definitions; merge into `.claude/mcp.json` or `~/.claude/mcp.json`
- **Python dep**: `pip install mcp`

## Server List
| Server | Type | Source |
|--------|------|--------|
| `fanfic-helper` | Custom Python | `fanfic-helper/server.py` |
| `brave-search` | External npm | `@anthropic-ai/mcp-server-brave-search` |
| `memory` | External npm | `@modelcontextprotocol/server-memory` |
| `sequential-thinking` | External npm | `@modelcontextprotocol/server-sequential-thinking` |
| `fetch` | External npm | `@anthropic-ai/mcp-server-fetch` |
