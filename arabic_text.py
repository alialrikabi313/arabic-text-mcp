# -*- coding: utf-8 -*-
"""معالجة النص العربي: دوال نقية بلا حالة ولا شبكة. الخادم (server.py) يغلّفها فقط."""

import re

from config import (
    ALEF_VARIANTS,
    BUCKWALTER,
    DIACRITICS,
    EASTERN_DIGITS,
    PERSIAN_DIGITS,
    TATWEEL,
    WESTERN_DIGITS,
)

_DIACRITICS_RE = re.compile(f"[{DIACRITICS}]")
_FROM_BUCKWALTER = {v: k for k, v in BUCKWALTER.items()}
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?؟؛])\s+|\n+")


def strip_diacritics(text: str) -> str:
    return _DIACRITICS_RE.sub("", text)


def normalize(
    text: str,
    *,
    alef: bool = True,
    yaa: bool = True,
    taa_marbuta: bool = False,
    hamza_on_carrier: bool = False,
) -> str:
    # الشدّة والتشكيل والتطويل يُحذفون دائماً؛ الباقي اختياري لأنه يفقد تمييزاً لغوياً
    out = strip_diacritics(text).replace(TATWEEL, "")
    if alef:
        out = re.sub(f"[{ALEF_VARIANTS}]", "ا", out)
    if yaa:
        out = out.replace("ى", "ي")
    # ة→ه افتراضه False: يدمج «مدرسة» و«مدرسه» لكنه يخلط أيضاً كلمات مختلفة
    if taa_marbuta:
        out = out.replace("ة", "ه")
    if hamza_on_carrier:
        out = out.replace("ؤ", "و").replace("ئ", "ي")
    return out


def convert_digits(text: str, to: str = "western") -> str:
    if to == "western":
        table = str.maketrans(EASTERN_DIGITS + PERSIAN_DIGITS, WESTERN_DIGITS * 2)
    elif to == "eastern":
        table = str.maketrans(WESTERN_DIGITS + PERSIAN_DIGITS, EASTERN_DIGITS * 2)
    else:
        raise ValueError(f"to يجب أن تكون 'western' أو 'eastern' وليس {to!r}")
    return text.translate(table)


def to_buckwalter(text: str) -> str:
    return "".join(BUCKWALTER.get(ch, ch) for ch in text)


def from_buckwalter(text: str) -> str:
    return "".join(_FROM_BUCKWALTER.get(ch, ch) for ch in text)


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_SPLIT_RE.split(text) if s.strip()]


def script_stats(text: str) -> dict[str, float | int]:
    letters = [ch for ch in text if ch.isalpha()]
    arabic = sum("؀" <= ch <= "ۿ" or "ݐ" <= ch <= "ݿ" for ch in letters)
    latin = sum("a" <= ch.lower() <= "z" for ch in letters)
    return {
        "letters": len(letters),
        "arabic_letters": arabic,
        "latin_letters": latin,
        "diacritics": len(_DIACRITICS_RE.findall(text)),
        "arabic_ratio": round(arabic / len(letters), 4) if letters else 0.0,
        "words": len(text.split()),
    }
