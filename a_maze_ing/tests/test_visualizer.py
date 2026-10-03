"""Tests for interactive terminal visualizer."""

from typing import List
from mazegen.generator import MazeGenerator
from mazegen.visualizer import (
    COLOR_ENTRY,
    COLOR_EXIT,
    COLOR_PATH,
    InteractiveVisualizer,
    render_ascii_grid,
)


def test_render_ascii_grid_dimensions() -> None:
    """Verify canvas has (2H+1) lines and (2W+1)*2 characters per line."""
    gen = MazeGenerator(
        width=10,
        height=8,
        entry=(0, 0),
        exit_coord=(9, 7),
        perfect=True,
        seed=42,
    )
    grid = gen.generate()
    rendered = render_ascii_grid(
        grid=grid,
        entry=(0, 0),
        exit_coord=(9, 7),
        use_ansi=False,
    )
    lines = rendered.split("\n")
    # 2*8 + 1 = 17 lines
    assert len(lines) == 17
    # (2*10 + 1) * 2 chars = 42 characters per line
    assert all(len(line) == 42 for line in lines)


def test_render_colors_and_path_toggle() -> None:
    """Verify entry, exit, and solution path ANSI sequences appear in rendering."""
    gen = MazeGenerator(
        width=12,
        height=9,
        entry=(0, 0),
        exit_coord=(11, 8),
        perfect=True,
        seed=123,
    )
    grid = gen.generate()
    path = gen.get_solution_path()

    # Without path
    no_path_render = render_ascii_grid(
        grid=grid,
        entry=(0, 0),
        exit_coord=(11, 8),
        path=None,
        use_ansi=True,
    )
    assert COLOR_ENTRY in no_path_render
    assert COLOR_EXIT in no_path_render
    assert COLOR_PATH not in no_path_render

    # With path
    with_path_render = render_ascii_grid(
        grid=grid,
        entry=(0, 0),
        exit_coord=(11, 8),
        path=path,
        use_ansi=True,
    )
    assert COLOR_PATH in with_path_render


def test_visualizer_state_controls() -> None:
    """Verify toggle_path, rotate_color, and regenerate methods."""
    gen = MazeGenerator(
        width=10,
        height=8,
        entry=(0, 0),
        exit_coord=(9, 7),
        perfect=True,
        seed=50,
    )
    vis = InteractiveVisualizer(gen)
    assert vis.show_path is False
    assert vis.toggle_path() is True
    assert vis.show_path is True
    assert vis.toggle_path() is False

    initial_color_idx = vis.color_index
    new_color_name = vis.rotate_color()
    assert vis.color_index == initial_color_idx + 1
    assert isinstance(new_color_name, str)

    old_hex = gen.get_grid().to_hex_lines()
    vis.regenerate()
    new_hex = gen.get_grid().to_hex_lines()
    assert old_hex != new_hex


def test_interactive_menu_loop_execution() -> None:
    """Verify menu loop processes user commands and terminates cleanly."""
    gen = MazeGenerator(
        width=10,
        height=8,
        entry=(0, 0),
        exit_coord=(9, 7),
        perfect=True,
        seed=1,
    )
    vis = InteractiveVisualizer(gen, use_ansi=False)

    # Sequence of user inputs: toggle path (2), rotate color (3), regen (1), quit (4)
    user_inputs = ["2", "3", "1", "4"]
    output_messages: List[str] = []

    def mock_input(prompt: str) -> str:
        return user_inputs.pop(0)

    def mock_print(msg: str = "") -> None:
        output_messages.append(str(msg))

    vis.run_menu_loop(input_fn=mock_input, print_fn=mock_print)

    assert vis.show_path is True
    assert vis.color_index == 1
    assert any("Goodbye!" in m for m in output_messages)


def test_interactive_menu_loop_handles_interrupt() -> None:
    """Verify menu loop handles KeyboardInterrupt gracefully."""
    gen = MazeGenerator(
        width=10,
        height=8,
        entry=(0, 0),
        exit_coord=(9, 7),
        perfect=True,
        seed=1,
    )
    vis = InteractiveVisualizer(gen, use_ansi=False)

    def mock_interrupt(prompt: str) -> str:
        raise KeyboardInterrupt()

    output_messages: List[str] = []
    vis.run_menu_loop(
        input_fn=mock_interrupt, print_fn=lambda m: output_messages.append(m)
    )

    assert any("Exiting visualizer" in m for m in output_messages)
