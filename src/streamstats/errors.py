"""Кастомные исключения."""

class StreamStatsError(Exception):
    """Базовое исключение для всех ошибок streamstats."""
    
class InvalidEventError(StreamStatsError):
    """Неверное событие."""
    
class InvalidFormatError(StreamStatsError):
    """Неподдерживаемый формат."""
    
class InvalidTimestampError(StreamStatsError):
    """Неверная временная метка."""
    
class CLIError(StreamStatsError):
    """Ошибка конфигурации CLI."""