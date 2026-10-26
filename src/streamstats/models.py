"""Модель события и валидация."""

from datetime import datetime
from enum import Enum

from .errors import InvalidEventError, InvalidTimestampError


class Level(Enum):
    """Все варианты level."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    
class Event:
    """Вид события."""

    def __init__(self, timestamp, level, source, message):
        """Инициализация event."""
        self.timestamp = timestamp
        self.level = Level(level)
        self.source = source
        self.message = message
        
    def __repr__(self):
        """Строковое представление."""
        return f"Event(timestamp={self.timestamp!r}, level={self.level!r}, source={self.source!r}, message={self.message!r})"
    
    def __eq__(self, other):
        """Сравнить с другим event."""
        if not isinstance(other, Event):
            return NotImplemented
        return (self.timestamp == other.timestamp and self.level == other.level and self.source == other.source and self.message == other.message)

    
def validation(val: dict) -> Event:
    """Проверка на корректность event."""
    if "timestamp" not in val:
        raise InvalidEventError(f"Нет поля timestamp {val!r}")
    elif "level" not in val:
        raise InvalidEventError(f"Нет поля level {val!r}")
    elif "source" not in val:
        raise InvalidEventError(f"Нет поля source {val!r}")
    elif "message" not in val:
        raise InvalidEventError(f"Нет поля message {val!r}")
    
    timestamp = parse_time(val["timestamp"])
    
    try:
        level = Level(val['level'])
    except ValueError as exc:
        raise InvalidEventError(f"поле 'level': Некорректное выражение: {val!r}") from exc
    
    if not isinstance(val['source'], str):
        raise InvalidEventError(f"поле 'source': Не является строкой: {val!r}")
    
    if not val['source'].strip():
        raise InvalidEventError(f"поле 'source': Пустая строка: {val!r}")
    
    if not isinstance(val['message'], str):
        raise InvalidEventError(f"поле 'message': Не является строкой: {val!r}")
    
    return Event(timestamp, level, val['source'].strip(), val['message'])
    
    

    
def parse_time(date: str) -> datetime:
    """Парсит ISO 8601 в datetime."""
    if not isinstance(date, str):
        raise InvalidTimestampError(f"поле 'timestamp': Некорректный тип: {date!r}")
    
    if date.strip() == "":
        raise InvalidTimestampError(f"поле 'timestamp': Пустая строка: {date!r}")
    
    new_f = date.replace("Z", "+00:00")
    
    try:
        return datetime.fromisoformat(new_f)                          
    except ValueError as exc:
        raise InvalidTimestampError(f"поле 'timestamp': Некорректный формат ISO 8601: {date!r}") from exc