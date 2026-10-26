"""Тесты паесрера."""

from io import StringIO

import pytest

from streamstats.errors import InvalidFormatError, InvalidTimestampError
from streamstats.models import Level
from streamstats.parsers import parse_csv, parse_jsonl


def test_parse_jsonl_valid():
    """Тест: валидный JSONL парсится."""
    fake_file = StringIO('{"timestamp": "2024-01-01T10:00:00Z", "level": "ERROR", "source": "auth", "message": "fail"}\n')
    events = list(parse_jsonl(fake_file, filename="test.jsonl"))

    assert len(events) == 1
    assert events[0].level == Level.ERROR
    assert events[0].source == "auth"


def test_parse_jsonl_invalid_json():
    """Тест: битый JSON вызывает InvalidFormatError."""
    fake_file = StringIO('это вообще не json\n')
    with pytest.raises(InvalidFormatError):
        list(parse_jsonl(fake_file, filename="test.jsonl"))


def test_parse_jsonl_invalid_timestamp():
    """Тест: неверная дата вызывает InvalidTimestampError."""
    fake_file = StringIO('{"timestamp": "вчера", "level": "ERROR", "source": "auth", "message": "fail"}\n')
    with pytest.raises(InvalidTimestampError):
        list(parse_jsonl(fake_file, filename="test.jsonl"))


def test_parse_jsonl_skip_invalid():
    """Тест: с флагом skip_invalid битые строки заменяются на None."""
    content = (
        '{"timestamp": "2024-01-01T10:00:00Z", "level": "INFO", "source": "api", "message": "ok"}\n'
        'битая строка\n'
        '{"timestamp": "2024-01-01T11:00:00Z", "level": "ERROR", "source": "auth", "message": "fail"}\n'
    )
    events = list(parse_jsonl(StringIO(content), filename="test.jsonl", skip_invalid=True))

    assert len(events) == 3
    assert events[1] is None  # Битая строка стала None


def test_parse_csv_valid():
    """Тест: валидный CSV парсится."""
    content = (
        "timestamp,level,source,message\n"
        "2024-01-01T10:00:00Z,ERROR,auth,fail\n"
    )
    events = list(parse_csv(StringIO(content), filename="test.csv"))

    assert len(events) == 1
    assert events[0].level == Level.ERROR