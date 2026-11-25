# -*- coding: utf-8 -*-
"""اختبارات الدوال. كل حالة نص عربي حقيقي صادفناه، لا بيانات مخترَعة."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import arabic_text as at


def test_basmala_uthmani_script_normalizes_to_plain():
    # البسملة بالرسم العثماني: ألف وصل ٱ + ألف خنجرية ٰ + تشكيل كامل
    assert at.normalize("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ") == "بسم الله الرحمن الرحيم"


def test_tatweel_stretched_word():
    # التطويل شائع في العناوين والمنشورات: «العــــربية»
    assert at.normalize("العــــربية") == "العربية"


def test_alef_hamza_forms_unify():
    assert at.normalize("أحمد إبراهيم آدم") == "احمد ابراهيم ادم"


def test_taa_marbuta_off_by_default():
    # ة→ه يخلط «مدرسة» و«مدرسه»؛ لذا لا يُطبَّق ما لم يُطلب
    assert at.normalize("مدرسة") == "مدرسة"
    assert at.normalize("مدرسة", taa_marbuta=True) == "مدرسه"


def test_digits_mixed_eastern_and_persian_in_one_line():
    # نصوص عربية كثيرة تخلط ٢٠١٤ (هندية) و۲۰۲۶ (فارسية) في السطر نفسه
    assert at.convert_digits("سنة ٢٠١٤ و ۲۰۲۶") == "سنة 2014 و 2026"
    assert at.convert_digits("سنة 2014", to="eastern") == "سنة ٢٠١٤"


def test_digits_rejects_unknown_target():
    with pytest.raises(ValueError):
        at.convert_digits("1", to="roman")


def test_buckwalter_roundtrip_with_diacritics_and_shadda():
    text = "مُحَمَّدٌ"
    assert at.from_buckwalter(at.to_buckwalter(text)) == text


def test_buckwalter_known_value():
    assert at.to_buckwalter("كتب") == "ktb"


def test_wikipedia_mixed_lt_rtl_stats():
    # سطر من مقال «الرعاية الملائمة في وقت مبكر»: عربي مع PH وأرقام لاتينية
    s = at.script_stats("أن يكون الرقم الهيدروجيني (PH)>أو=7.25")
    assert s["latin_letters"] == 2
    assert 0.8 < s["arabic_ratio"] < 1.0


def test_empty_text_has_zero_ratio_not_division_error():
    assert at.script_stats("")["arabic_ratio"] == 0.0


def test_split_sentences_arabic_question_mark_and_semicolon():
    assert at.split_sentences("ما اسمك؟ اسمي علي؛ وأنت؟") == ["ما اسمك؟", "اسمي علي؛", "وأنت؟"]
