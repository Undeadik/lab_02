"""Точка входа для CLI."""

import argparse
import json
import sys

from .analysis import analyze
from .errors import InvalidFormatError, StreamStatsError
from .parsers import parse_csv, parse_jsonl
from .report import stats_dict, write_reports


def build_parser():
    """Парсер для обработки сообщения с терминала."""
    parser = argparse.ArgumentParser(
        prog="streamstats",
        description="CLI streamstats analyze: потоковый анализ файлов",
    )
    sub = parser.add_subparsers(dest='command', required=True)
    
    analyze_p = sub.add_parser('analyze')
    analyze_p.add_argument('input', nargs='+')
    analyze_p.add_argument('--format', choices=['csv', 'jsonl'], required=True)
    analyze_p.add_argument('--output', required=False)
    analyze_p.add_argument('--skip-invalid', action="store_true")
    return parser

def iter_events(paths, format, skip_invalid):
    """Генерация ивентов."""
    for path in paths:
        if format == "jsonl":
            parser = parse_jsonl
        elif format == "csv":
            parser = parse_csv
        else:
            raise InvalidFormatError("Пeредан не csv/jsonl формат")
        with open(path, encoding="utf-8") as f:
            yield from parser(f, filename=path, skip_invalid=skip_invalid) 
    
def cmd_analyze(args):
    """Просмотор условий куда и и с какими условиями должны конвертироваться данные парсера."""
    events = iter_events(args.input, args.format, args.skip_invalid)
    stats = analyze(events)
    if args.output is None:
        print(json.dumps(stats_dict(stats), ensure_ascii=False))
    else:
        write_reports(stats, args.output)
    return 0
        

def main(argv: list[str] | None = None):
    """Запустить программу."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "analyze":
            return cmd_analyze(args)
    except StreamStatsError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2

    return 0

if __name__ == "__main__":
    sys.exit(main())