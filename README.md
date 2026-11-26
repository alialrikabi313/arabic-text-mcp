# arabic-text-mcp

A small [MCP](https://modelcontextprotocol.io) server that gives any agent **deterministic Arabic text tools** — no model calls, no network, no state. Useful because LLMs are unreliable at exact character-level work (stripping diacritics, unifying alef forms, converting digits).

[![tests](https://github.com/alialrikabi313/arabic-text-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/alialrikabi313/arabic-text-mcp/actions/workflows/test.yml)

> **TL;DR** — Seven deterministic Arabic text tools for any MCP client; tested end-to-end through a real stdio MCP session.

## Tools

| Tool | What it does |
|---|---|
| `normalize` | Strips tashkeel and tatweel; optionally unifies alef (أإآٱ→ا), yaa (ى→ي), taa marbuta (ة→ه), hamza carriers (ؤئ) |
| `strip_diacritics` | Removes harakat, shadda, sukun and the dagger alef (ٰ) only |
| `convert_digits` | Western ↔ Eastern Arabic-Indic digits; Persian digits (۰-۹) folded in, since real text mixes them |
| `to_buckwalter` / `from_buckwalter` | Lossless Buckwalter transliteration |
| `split_sentences` | Splits on `. ! ? ؟ ؛` and newlines |
| `script_stats` | Arabic/Latin letter counts, diacritics, words, Arabic ratio |

Design choice: `taa_marbuta` normalization is **off by default** — it merges `مدرسة`/`مدرسه` but also conflates distinct words, so it must be requested.

## Use

```bash
pip install -r requirements.txt

# Claude Code
claude mcp add arabic-text -- python /path/to/server.py
```

Or in any MCP client config: `{"command": "python", "args": ["/path/to/server.py"]}` (stdio).

## Tests

```bash
pytest tests
```

Includes an end-to-end test that spawns the server as a real process and calls a tool through an MCP client over stdio. Test cases come from real text (Uthmani-script basmala, tatweel-stretched headlines, mixed Eastern/Persian digits, a Wikipedia line mixing LTR and RTL).

Built on `mcp` 2.x (`MCPServer`, formerly `FastMCP`).

## Scope

Intentionally excludes dialect identification and diacritization: those need models and honest accuracy numbers, not rules. Planned as separate, evaluated modules.
