"""Анализ и сбор статистики."""

from collections import Counter

from .models import Level


class Stats:
    """Контейнер для статистики."""

    def __init__(self):
        """Инициализация счётчики."""
        self.total = 0
        self.by_level = Counter()
        self.by_source = Counter()
        self.error_sources = Counter()
        self.first_timestamp = None
        self.last_timestamp = None
        self.skipped = 0

def analyze(events):
    """Подсчет статистики по потоку событий."""
    stats = Stats()
    for ev in events:
        if ev is None:
            stats.skipped +=1
            continue
        stats.total += 1
        stats.by_level[ev.level] += 1
        stats.by_source[ev.source] += 1

        if ev.level == Level.ERROR or ev.level == Level.CRITICAL:
            stats.error_sources[ev.source] += 1

        if stats.first_timestamp is None or ev.timestamp < stats.first_timestamp:
            stats.first_timestamp = ev.timestamp

        if stats.last_timestamp is None or ev.timestamp > stats.last_timestamp:
            stats.last_timestamp = ev.timestamp
    return stats