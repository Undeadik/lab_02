"""Тесты CLI."""

import json

from streamstats.__main__ import main


def test_cli_integration(tmp_path):
    """Тест: полный цикл CLI от файла до отчёта."""
    input_file = tmp_path / "input.jsonl"
    input_file.write_text(
        '{"timestamp": "2024-01-01T10:00:00Z", "level": "ERROR", "source": "xyz", "message": "fail"}\n'
        '{"timestamp": "2024-01-01T11:00:00Z", "level": "INFO", "source": "xyz", "message": "ok"}\n',
        encoding="utf-8"
    )

    output_file = tmp_path / "report.json"
    
    exit_code = main([
        "analyze",
        str(input_file),
        "--format", "jsonl",
        "--output", str(output_file)
    ])

    assert exit_code == 0
    assert output_file.exists()

    with open(output_file, encoding="utf-8") as f:
        report = json.load(f)

        assert report["total"] == 2
        assert report["level_count"]["ERROR"] == 1
        assert report["source_count"]["xyz"] == 2
    
    
def test_cli_many_files(tmp_path):
    """Тест: несколько файлов агрегируются в один отчёт."""
    file1 = tmp_path / "input1.jsonl"
    file1.write_text('{"timestamp": "2024-01-01T10:00:00Z", "level": "ERROR", "source": "auth", "message": "fail"}\n', encoding="utf-8")

    file2 = tmp_path / "input2.jsonl"
    file2.write_text('{"timestamp": "2024-01-01T11:00:00Z", "level": "INFO", "source": "api", "message": "ok"}\n', encoding="utf-8")

    output_file = tmp_path / "report.json"

    exit_code = main(["analyze", str(file1), str(file2), "--format", "jsonl", "--output", str(output_file)])

    assert exit_code == 0
    with open(output_file, "r", encoding="utf-8") as f:
        report = json.load(f)
        assert report["total"] == 2  