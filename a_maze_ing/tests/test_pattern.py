"""Tests for embedded '42' pattern generation and boundary masking."""

from mazegen.grid import Grid
from mazegen.pattern import (
    PATTERN_42,
    PATTERN_HEIGHT,
    PATTERN_WIDTH,
    apply_pattern_42,
    can_fit_pattern,
    get_pattern_cells_at,
)


def test_pattern_dimensions_and_bitmap() -> None:
    """Verify standard dimensions and active cell count of '42' bitmap."""
    assert len(PATTERN_42) == PATTERN_HEIGHT
    assert all(len(row) == PATTERN_WIDTH for row in PATTERN_42)

    active_cells = sum(row.count(1) for row in PATTERN_42)
    # 9 cells in '4' + 11 cells in '2' = 20 fully closed cells
    assert active_cells == 20

    # Also verify get_pattern_cells_at returns the exact 20 coordinates
    coords = get_pattern_cells_at(0, 0)
    assert len(coords) == 20


def test_can_fit_pattern_valid() -> None:
    """Verify centered positioning in a normal-sized grid."""
    width, height = 20, 15
    entry, exit_coord = (0, 0), (19, 14)
    fits, offset, reason = can_fit_pattern(width, height, entry, exit_coord)

    assert fits is True
    assert offset == ((20 - 7) // 2, (15 - 5) // 2)
    assert offset == (6, 5)


def test_pattern_omitted_when_grid_too_small() -> None:
    """Verify graceful omission when maze dimensions are smaller than required."""
    width, height = 8, 6  # Minimum required is 9x7
    entry, exit_coord = (0, 0), (7, 5)
    fits, offset, reason = can_fit_pattern(width, height, entry, exit_coord)

    assert fits is False
    assert offset is None
    assert "too small" in reason.lower()

    grid = Grid(8, 6)
    applied = apply_pattern_42(grid, entry, exit_coord, verbose=False)
    assert applied is False


def test_pattern_omitted_on_entry_collision() -> None:
    """Verify collision detection when entry coincides with a pattern cell."""
    width, height = 15, 11
    # Center offset is ((15-7)//2, (11-5)//2) = (4, 3)
    # The cell at (4, 3) is row 0, col 0 of '4', which is 1 (closed)
    entry = (4, 3)
    exit_coord = (14, 10)

    fits, offset, reason = can_fit_pattern(width, height, entry, exit_coord)
    assert fits is False
    assert "collision" in reason.lower()

    grid = Grid(width, height)
    applied = apply_pattern_42(grid, entry, exit_coord, verbose=False)
    assert applied is False


def test_apply_pattern_marks_cells_and_preserves_coherence() -> None:
    """Verify that applying pattern marks cells as 0xF and keeps grid coherent."""
    grid = Grid(17, 13)
    applied = apply_pattern_42(grid, (0, 0), (16, 12), verbose=False)
    assert applied is True

    pattern_cells = [c for c in grid.all_cells() if c.is_pattern]
    assert len(pattern_cells) == 20
    assert all(c.walls == 15 for c in pattern_cells)
    assert all(c.hex_char() == "F" for c in pattern_cells)

    coherent, err = grid.is_coherent()
    assert coherent is True
    assert err is None
