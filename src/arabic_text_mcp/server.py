# -*- coding: utf-8 -*-
"""خادم MCP لأدوات النص العربي: تطبيع، تشكيل، أرقام، Buckwalter، جمل، إحصاءات.

يعمل عبر stdio. أضفه لأي عميل MCP بالأمر: arabic-text-mcp  (أو python -m arabic_text_mcp)
"""

from mcp.server.mcpserver import MCPServer

from . import core as at

mcp = MCPServer(
    "arabic-text",
    instructions="Deterministic Arabic text utilities: normalization, diacritics, digits, Buckwalter, sentences.",
)


@mcp.tool()
def normalize(
    text: str,
    alef: bool = True,
    yaa: bool = True,
    taa_marbuta: bool = False,
    hamza_on_carrier: bool = False,
) -> str:
    """Normalize Arabic for search/matching: strips diacritics and tatweel, optionally unifies alef/yaa/taa-marbuta/hamza carriers."""
    return at.normalize(
        text, alef=alef, yaa=yaa, taa_marbuta=taa_marbuta, hamza_on_carrier=hamza_on_carrier
    )


@mcp.tool()
def strip_diacritics(text: str) -> str:
    """Remove tashkeel (harakat, shadda, sukun, dagger alef) and keep letters as-is."""
    return at.strip_diacritics(text)


@mcp.tool()
def convert_digits(text: str, to: str = "western") -> str:
    """Convert between Western (0-9) and Eastern Arabic-Indic (٠-٩) digits; Persian digits are folded in. `to` is 'western' or 'eastern'."""
    return at.convert_digits(text, to)


@mcp.tool()
def to_buckwalter(text: str) -> str:
    """Transliterate Arabic to Buckwalter ASCII (lossless, reversible)."""
    return at.to_buckwalter(text)


@mcp.tool()
def from_buckwalter(text: str) -> str:
    """Transliterate Buckwalter ASCII back to Arabic."""
    return at.from_buckwalter(text)


@mcp.tool()
def split_sentences(text: str) -> list[str]:
    """Split Arabic text into sentences on . ! ? ؟ ؛ and newlines."""
    return at.split_sentences(text)


@mcp.tool()
def script_stats(text: str) -> dict[str, float | int]:
    """Count Arabic/Latin letters, diacritics and words; arabic_ratio is Arabic letters over all letters."""
    return at.script_stats(text)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
