"""Парсеры файлов JSONL и CSV."""

import csv
import json
import logging

from .errors import InvalidEventError, InvalidFormatError, InvalidTimestampError
from .models import validation


def parse_jsonl(f, filename, skip_invalid=False):
    """Парсер для json."""
    for num_line, line in enumerate(f, 1):
        line = line.strip()
        if not(line):
            continue
        try:
            data = json.loads(line)
        except ValueError as exc:
            if skip_invalid:
                logging.warning(f"{filename}:{num_line}: {exc}")
                yield None
                continue
            raise InvalidFormatError(f"{filename}:{num_line}: Некорректный JSON: {line!r}") from exc
        
        try:
            event = validation(data)
        except InvalidTimestampError as exc:
            if skip_invalid:
                logging.warning(f"{filename}:{num_line}: {exc}")
                yield None  
                continue   
            raise InvalidTimestampError(f"{filename}:{num_line}: {exc}") from exc
        except InvalidEventError as exc:
            if skip_invalid:
                logging.warning(f"{filename}:{num_line}: {exc}")
                yield None
                continue
            raise InvalidEventError(f"{filename}:{num_line}: {exc}") from exc
        
        yield event
        
def parse_csv(f, filename, skip_invalid=False):
    """Аналогичный для csv."""
    reader = csv.DictReader(f)          
    for row in reader:                    
        num_line = reader.line_num        
        try:
            event = validation(row)     
        except InvalidTimestampError as exc:
            if skip_invalid:
                logging.warning(f"{filename}:{num_line}: {exc}")
                yield None
                continue
            raise InvalidTimestampError(f"{filename}:{num_line}: {exc}") from exc
        except InvalidEventError as exc:
            if skip_invalid:
                logging.warning(f"{filename}:{num_line}: {exc}")
                yield None
                continue
            raise InvalidEventError(f"{filename}:{num_line}: {exc}") from exc
        
        yield event