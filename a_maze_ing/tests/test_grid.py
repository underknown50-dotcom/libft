"""Tests for Direction, Cell, and Grid data structures."""

import pytest
from mazegen.direction import Direction
from mazegen.grid import Cell, Grid


def test_direction_properties() -> None:
    """Verify bitwise values, deltas, opposites, and character conversions."""
    assert Direction.NORTH.value == 1
    assert Direction.EAST.value == 2
    assert Direction.SOUTH.value == 4
    assert Direction.WEST.value == 8

    assert Direction.NORTH.opposite == Direction.SOUTH
    assert Direction.SOUTH.opposite == Direction.NORTH
    assert Direction.EAST.opposite == Direction.WEST
    assert Direction.WEST.opposite == Direction.EAST

    assert Direction.NORTH.delta == (0, -1)
    assert Direction.EAST.delta == (1, 0)
    assert Direction.SOUTH.delta == (0, 1)
    assert Direction.WEST.delta == (-1, 0)

    assert Direction.NORTH.char == "N"
    assert Direction.from_char("N") == Direction.NORTH
    assert Direction.from_delta(0, -1) == Direction.NORTH


def test_cell_wall_operations() -> None:
    """Verify cell bitmask manipulations and hex character output."""
    cell = Cell(0, 0)
    assert cell.walls == 15
    assert cell.hex_char() == "F"
    for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
        assert cell.has_wall(d) is True

    # Open South and West (subject example: 3 / binary 0011)
    cell.open_wall(Direction.SOUTH)
    cell.open_wall(Direction.WEST)
    assert cell.walls == 3
    assert cell.hex_char() == "3"
    assert cell.has_wall(Direction.NORTH) is True
    assert cell.has_wall(Direction.EAST) is True
    assert cell.has_wall(Direction.SOUTH) is False
    assert cell.has_wall(Direction.WEST) is False

    # Close South and West, open North and South (subject example: A / 1010)
    cell.close_wall(Direction.SOUTH)
    cell.close_wall(Direction.WEST)
    cell.open_wall(Direction.NORTH)
    cell.open_wall(Direction.SOUTH)
    assert cell.walls == 10
    assert cell.hex_char() == "A"


def test_grid_initialization_and_coherence() -> None:
    """Verify that a fresh grid is fully enclosed and internally coherent."""
    grid = Grid(5, 4)
    assert grid.width == 5
    assert grid.height == 4

    coherent, err = grid.is_coherent()
    assert coherent is True
    assert err is None

    # Invalid dimension test
    with pytest.raises(ValueError):
        Grid(2, 5)


def test_remove_wall_between_neighbors() -> None:
    """Verify coherent wall removal between orthogonal neighbors."""
    grid = Grid(4, 4)
    c1 = grid.get_cell(1, 1)
    c2 = grid.get_cell(2, 1)  # East of c1

    grid.remove_wall_between(c1, c2)
    assert c1.has_wall(Direction.EAST) is False
    assert c2.has_wall(Direction.WEST) is False

    coherent, err = grid.is_coherent()
    assert coherent is True
    assert err is None


def test_remove_wall_non_neighbors() -> None:
    """Verify error when attempting to remove wall between distant cells."""
    grid = Grid(4, 4)
    c1 = grid.get_cell(0, 0)
    c2 = grid.get_cell(2, 2)
    with pytest.raises(ValueError):
        grid.remove_wall_between(c1, c2)


def test_coherence_failure_on_border_breach() -> None:
    """Verify that opening an external boundary wall fails coherence check."""
    grid = Grid(4, 4)
    cell = grid.get_cell(0, 0)
    cell.open_wall(Direction.NORTH)

    coherent, err = grid.is_coherent()
    assert coherent is False
    assert err is not None
    assert "Border breach" in err


def test_coherence_failure_on_one_sided_wall() -> None:
    """Verify that opening a wall unilaterally without neighbor fails coherence."""
    grid = Grid(4, 4)
    cell = grid.get_cell(1, 1)
    cell.open_wall(Direction.EAST)  # Neighbor at (2,1) still has West wall closed!

    coherent, err = grid.is_coherent()
    assert coherent is False
    assert err is not None
    assert "Wall incoherence" in err


def test_hex_lines_export_and_import() -> None:
    """Verify roundtrip conversion to and from hexadecimal row strings."""
    grid = Grid(4, 3)
    c1 = grid.get_cell(1, 1)
    c2 = grid.get_cell(1, 2)
    grid.remove_wall_between(c1, c2)

    lines = grid.to_hex_lines()
    assert len(lines) == 3
    assert all(len(line) == 4 for line in lines)

    reconstructed = Grid.from_hex_lines(lines)
    assert reconstructed.width == 4
    assert reconstructed.height == 3
    assert reconstructed.to_hex_lines() == lines
