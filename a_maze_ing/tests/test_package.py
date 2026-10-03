"""Tests for package artifact structure and public API surface."""

import glob
from pathlib import Path
import zipfile
from mazegen import MazeGenerator


def test_wheel_exists_at_repo_root() -> None:
    """Verify that mazegen-*.whl is present at the repository root."""
    wheels = glob.glob("mazegen-*.whl")
    assert len(wheels) >= 1, "Expected mazegen-*.whl at root of repository."
    wheel_path = Path(wheels[0])
    assert wheel_path.is_file()
    assert wheel_path.name.startswith("mazegen-")
    assert wheel_path.name.endswith(".whl")


def test_wheel_contents_contain_all_modules_and_license() -> None:
    """Verify wheel archive bundles all required package files and metadata."""
    wheels = glob.glob("mazegen-*.whl")
    wheel_path = wheels[0]

    with zipfile.ZipFile(wheel_path, "r") as zf:
        namelist = zf.namelist()
        required_files = [
            "mazegen/__init__.py",
            "mazegen/config.py",
            "mazegen/direction.py",
            "mazegen/generator.py",
            "mazegen/grid.py",
            "mazegen/pattern.py",
            "mazegen/solver.py",
            "mazegen/py.typed",
        ]
        for req in required_files:
            assert req in namelist, f"Missing required file in wheel: {req}"

        # Verify license is bundled
        assert any(
            "LICENSE" in name for name in namelist
        ), "License not found in wheel archive."


def test_public_api_generation_and_solving() -> None:
    """Verify clean public API usage as documented in Chapter 6."""
    gen = MazeGenerator(
        width=16,
        height=12,
        entry=(0, 0),
        exit_coord=(15, 11),
        perfect=True,
        seed=999,
    )
    grid = gen.generate()
    assert grid.width == 16
    assert grid.height == 12

    # Access cell structure
    cell = grid.get_cell(0, 0)
    assert cell.hex_char() in "0123456789ABCDEF"

    # Access solution
    sol_str = gen.get_solution()
    assert len(sol_str) > 0
    assert set(sol_str).issubset({"N", "E", "S", "W"})
