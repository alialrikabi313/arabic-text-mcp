# -*- coding: utf-8 -*-
"""اختبار شامل: يشغّل server.py عملية فعلية ويستدعي أدواته عبر عميل MCP على stdio."""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_ROOT = Path(__file__).resolve().parent.parent


async def _call(tool: str, args: dict):
    params = StdioServerParameters(
        command=sys.executable, args=[str(_ROOT / "server.py")], cwd=str(_ROOT)
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            names = [t.name for t in (await session.list_tools()).tools]
            result = await session.call_tool(tool, args)
            return names, result


def test_server_lists_tools_and_normalizes_basmala_over_stdio():
    names, result = asyncio.run(
        _call("normalize", {"text": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"})
    )
    assert {"normalize", "to_buckwalter", "convert_digits", "script_stats"} <= set(names)
    assert result.content[0].text == "بسم الله الرحمن الرحيم"
