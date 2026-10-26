"""Тесты анализа данных."""

from datetime import datetime, timezone

from streamstats.analysis import analyze
from streamstats.models import Event, Level


def test_analyze_empty():
    """Тест: пустой поток событий даёт пустую статистику."""
    stats = analyze([])
    assert stats.total == 0
    assert stats.first_timestamp is None
    assert stats.last_timestamp is None


def test_analyze_aggregation():
    """Тест: правильный подсчёт уровней, источников и top-5."""
    e1 = Event(datetime(2024, 1, 1, 10, tzinfo=timezone.utc), Level.ERROR, "auth", "fail1")
    e2 = Event(datetime(2024, 1, 1, 11, tzinfo=timezone.utc), Level.ERROR, "auth", "fail2")
    e3 = Event(datetime(2024, 1, 1, 9, tzinfo=timezone.utc), Level.INFO, "api", "ok")

    stats = analyze([e1, e2, e3])

    assert stats.total == 3
    assert stats.by_level[Level.ERROR] == 2
    assert stats.by_level[Level.INFO] == 1
    assert stats.error_sources["auth"] == 2
    assert stats.first_timestamp == datetime(2024, 1, 1, 9, tzinfo=timezone.utc)
    assert stats.last_timestamp == datetime(2024, 1, 1, 11, tzinfo=timezone.utc)


def test_analyze_skipped():
    """Тест: None в потоке считается как пропущенная строка."""
    stats = analyze([None, None])
    assert stats.total == 0
    assert stats.skipped == 2