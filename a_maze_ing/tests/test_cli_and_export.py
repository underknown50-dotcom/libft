"""Tests for CLI entrypoint and output file exporter."""

from pathlib import Path
import pytest
from a_maze_ing import main
from mazegen import (
    MazeGenerator,
    export_maze,
    verify_maze_file,
)


def test_export_maze_and_verify(tmp_path: Path) -> None:
    """Verify file structure and integrity conforming to Chapter 4.5."""
    gen = MazeGenerator(
        width=15,
        height=10,
        entry=(0, 0),
        exit_coord=(14, 9),
        perfect=True,
        seed=123,
    )
    grid = gen.generate()
    sol_str = gen.get_solution()

    out_file = tmp_path / "test_maze.txt"
    export_maze(out_file, grid, (0, 0), (14, 9), sol_str)

    # 1. Inspect raw file structure
    raw_text = out_file.read_text(encoding="utf-8")
    lines = raw_text.splitlines()

    # 10 rows + 1 empty line + 1 entry + 1 exit + 1 path = 14 lines
    assert len(lines) == 14
    assert all(len(line) == 15 for line in lines[:10])
    assert lines[10] == ""
    assert lines[11] == "0,0"
    assert lines[12] == "14,9"
    assert lines[13] == sol_str

    # 2. Audit with verification engine
    valid, _, entry, exit_coord, path, err = verify_maze_file(out_file)
    assert valid is True, err
    assert entry == (0, 0)
    assert exit_coord == (14, 9)
    assert path == sol_str


def test_cli_missing_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify CLI error on missing arguments."""
    code = main(["a_maze_ing.py"])
    assert code == 1
    err = capsys.readouterr().err
    assert "Usage:" in err


def test_cli_too_many_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify CLI error on too many arguments."""
    code = main(["a_maze_ing.py", "cfg1.txt", "cfg2.txt"])
    assert code == 1
    err = capsys.readouterr().err
    assert "Usage:" in err


def test_cli_missing_config_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify CLI error on non-existent config file."""
    code = main(["a_maze_ing.py", "non_existent_file.txt"])
    assert code == 1
    err = capsys.readouterr().err
    assert "Configuration File Error" in err


def test_cli_successful_default_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify end-to-end execution of main() on default config."""
    temp_out = tmp_path / "out_maze.txt"
    cfg_content = (
        f"WIDTH=16\nHEIGHT=12\nENTRY=0,0\nEXIT=15,11\n"
        f"OUTPUT_FILE={temp_out.as_posix()}\nPERFECT=True\nSEED=42\n"
    )
    cfg_path = tmp_path / "run_cfg.txt"
    cfg_path.write_text(cfg_content, encoding="utf-8")

    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    exit_code = main(["a_maze_ing.py", str(cfg_path)])
    assert exit_code == 0
    assert temp_out.is_file()

    valid, _, _, _, _, err = verify_maze_file(temp_out)
    assert valid is True, err
