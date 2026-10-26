"""Написание отчёта."""

import json


def write_reports(stats, output):
    """Пишет отчет."""
    data = stats_dict(stats)
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=True)
        

def stats_dict(stats):
    """Приводит данные в тот формат, который json может обработать."""
    top5 = sorted(stats.error_sources.items(), key=lambda x: (-x[1], x[0]))[:5]
    res_level = {level.value: count for level, count in stats.by_level.items()}
    res_source = dict(stats.by_source)
    res = {
        'total' : stats.total,
        'level_count': res_level,
        'source_count' : res_source,
        'error_sources_top5': [{'source': src, 'count': cnt} for src, cnt in top5],
        'first_timestamp': stats.first_timestamp.isoformat()
        if stats.first_timestamp else None,
        'last_timestamp': stats.last_timestamp.isoformat()
        if stats.last_timestamp else None,
        'skipped' : stats.skipped,
    }
    return res
        
    
