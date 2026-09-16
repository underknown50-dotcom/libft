*This activity has been created as part of the 42 curriculum by mewaysi and mal-jama.*

# A-Maze-ing

An extensible, high-performance maze generation, pathfinding solver, and interactive terminal visualization suite written in Python (>=3.10) for the 42 Curriculum.

---

## Description

**A-Maze-ing** is a modular graph-theoretic maze generation system capable of producing both academic single-path perfect mazes (spanning trees) and arcade-style multi-loop playable boards (inspired by classic Pac-Man maps). The project embeds the canonical "42" pattern as fully closed obstacle blocks, guarantees physical wall coherence across all shared internal boundaries, solves for the optimal trajectory using Breadth-First Search (BFS), exports bitwise hexadecimal encodings, and renders an interactive, color-customizable ASCII/ANSI terminal display.

The maze generator is engineered as a standalone, zero-dependency Python package (`mazegen`) suitable for immediate installation and integration into downstream applications.

---

## Instructions

### Prerequisites
- Python >= 3.10
- Standard POSIX build tools (`make`) or equivalent

### 1. Installation & Environment Setup
Using the automated `Makefile`:
```bash
# Set up virtual environment and install development/linting tools
make install
```
Or manually:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 2. Execution
Run the main script with a configuration file:
```bash
make run
# or directly:
python3 a_maze_ing.py config.txt
```

### 3. Interactive Debugging
Launch the main application with Python's built-in `pdb` debugger:
```bash
make debug
```

### 4. Quality Assurance & Static Typing
Run strict PEP 8 and static type checks:
```bash
# Standard mandatory linting
make lint

# Strict type checking (mypy --strict)
make lint-strict
```

### 5. Automated Test Suite
Execute the full unit test suite:
```bash
make test
# or:
pytest -v
```

### 6. Building the Reusable Distribution Package
Build the standalone `.whl` and `.tar.gz` packages and copy them to the repository root:
```bash
make package
```

### 7. Cleaning Cache & Temporary Artifacts
Remove caches (`__pycache__`, `.mypy_cache`, `.pytest_cache`, `dist`, `build`):
```bash
make clean
```

---

## Configuration File Format

The configuration file is a plain text file containing one `KEY=VALUE` pair per line. Lines starting with `#` and empty lines are treated as comments and ignored.

### Mandatory Keys

| Key | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `WIDTH` | Integer | Maze width in number of cells ($\ge 3$) | `WIDTH=20` |
| `HEIGHT` | Integer | Maze height in number of cells ($\ge 3$) | `HEIGHT=15` |
| `ENTRY` | Coordinates | Start cell formatted as `x,y` (0-indexed) | `ENTRY=0,0` |
| `EXIT` | Coordinates | Destination cell formatted as `x,y` (0-indexed) | `EXIT=19,14` |
| `OUTPUT_FILE` | String | Target path for exported hexadecimal maze | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Boolean | `True` for single-path maze, `False` for Pac-Man board | `PERFECT=True` |

### Optional Keys

| Key | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `SEED` | Integer/String | Seed for deterministic, reproducible generation | `SEED=42` |

### Example `config.txt`
```ini
# ==========================================
# Default Configuration for A-Maze-ing
# ==========================================
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

---

## Output File Format (Hexadecimal Bitmask)

As mandated by Chapter 4.5, each cell's walls are encoded into a single hexadecimal digit (`0` through `F`), where each bit corresponds to a cardinal wall:
- **Bit 0 (LSB, 1)**: North wall closed
- **Bit 1 (2)**: East wall closed
- **Bit 2 (4)**: South wall closed
- **Bit 3 (8)**: West wall closed

A closed wall sets the bit to `1`; an open wall sets it to `0`. A fully solid cell (such as the "42" pattern) is encoded as `1 + 2 + 4 + 8 = 15 = F`.

### File Structure
1. $H$ lines of $W$ hexadecimal characters (one line per row).
2. An empty line (`\n`).
3. Entry coordinates: `x,y`.
4. Exit coordinates: `x,y`.
5. Shortest path sequence: string of directional moves (`N`, `E`, `S`, `W`).

```text
95553B957B979795557B
8153C42D144529455156
...
D555457EED6C7EC55546

0,0
19,14
SESSSSEESESSSESEEEEESESESEESEEEEE
```

---

## Maze Generation Algorithms & Rationale

### Mode 1: Academic Perfect Maze (`PERFECT=True`)
- **Algorithm**: **Randomized Prim's Algorithm**.
- **Rationale**:
  - In graph theory, a perfect maze is a **Spanning Tree**: a connected acyclic graph connecting all $V$ cells with exactly $E = V - 1$ edges.
  - While the recursive backtracker (DFS) generates long, winding paths with minimal branches, Prim's algorithm grows outwards uniformly from an active frontier. This yields complex, organic labyrinth structures with a high branching factor.
  - Because Prim's only connects visited cells to unvisited cells, it is mathematically impossible to introduce cycles.

### Mode 2: Pac-Man Playable Board (`PERFECT=False`)
- **Algorithm**: **Spanning Tree Base + Multi-Pass Braiding & Loop Influx**.
- **Rationale**:
  - In a Pac-Man game, dead-ends trap chased players, making gameplay frustrating. The board must be **braided** (rare or zero dead-ends) and feature multiple alternative circuits.
  - **Corner & Centre Openings**: Ghosts and power-pellets spawn in the four corners, while the player starts near the center. The algorithm ensures all 4 corners have at least 2 open exits and opens central corridors around the "42" pattern.
  - **Braiding**: The algorithm identifies dead-ends (degree 1, 3 closed walls) and carves passages into neighboring corridors to turn them into continuous passages or junctions.
  - **Corridor Width Constraint ($\le 2$ cells wide)**: Chapter 4.4 strictly forbids $3 \times 3$ open voids. Before any wall is carved during corner opening or braiding, `would_create_3x3_open_area` inspects all overlapping $3 \times 3$ subgrids to guarantee that no $3 \times 3$ room is ever created.

---

## Pathfinding Solver (Breadth-First Search)

To guarantee the **shortest valid path** from `ENTRY` to `EXIT`, the solver uses **Breadth-First Search (BFS)** with a FIFO queue.
- On unweighted grid graphs, BFS is mathematically guaranteed to identify the path with the minimum number of steps.
- The solver records predecessor cells in a parent dictionary (`parent[cell] = (prev_cell, direction_char)`).
- Reconstructs both the coordinate path `[(x0, y0), (x1, y1), ...]` (for visual rendering) and the directional string `[NESW]*` (for output file export).
- Validates that every move passes through an open wall and bypasses the solid "42" pattern blocks.

---

## Code Reusability & Standalone Library (`mazegen`)

The generation and solving logic is packaged into a standalone library named `mazegen-*`, installable directly via `pip`:
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Python API Example
```python
from mazegen import MazeGenerator

# 1. Instantiate with custom parameters
generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_coord=(19, 14),
    perfect=False,  # Pac-Man mode
    seed=42
)

# 2. Access the grid structure
grid = generator.generate()
cell = grid.get_cell(0, 0)
print("Cell walls bitmask:", cell.hex_char())

# 3. Retrieve the solution
path_coords, solution_string = generator.solve()
print("Optimal path length:", len(path_coords))
print("Directional string:", solution_string)
```

---

## Interactive Terminal Visualizer

When executed in an interactive terminal, `a_maze_ing.py` launches a visual display featuring:
- **Aspect-ratio corrected square blocks** (`██` characters).
- **Distinct element coloring**:
  - Entry cell: Bright Magenta (`\033[95m`)
  - Exit cell: Bright Red (`\033[91m`)
  - Solution path: Bright Cyan (`\033[96m`)
  - "42" pattern: Dark Gray (`\033[90m`)
  - Walls: Rotatable palette (White, Olive/Yellow, Green, Blue, Amber, Purple, Aqua).
- **Interactive menu**:
  ```text
  === A-Maze-ing ===
  1. Re-generate a new maze
  2. Show/Hide path from entry to exit (Currently: OFF)
  3. Rotate maze colors (Currently: Bright White)
  4. Quit
  Choice? (1-4): 
  ```

---

## Team & Project Management

### Roles & Responsibilities
- **mewaysi**: Co-Architect, Core Maze Generation Algorithms (Randomized Prim's Spanning Tree & Braided Pac-Man loops), Bitwise Grid Modeling, Pathfinding Solver (BFS).
- **mal-jama**: Co-Architect, Configuration Parser & Domain Validator, "42" Pattern Masking, Interactive ANSI Terminal Visualizer, Output File Serialization, Multi-Platform Makefile & Packaging CLI.

### Anticipated Planning vs. Actual Evolution
The project was planned across 10 focused milestones:
1. **Milestone 1**: Environment, packaging config (`pyproject.toml`), and Makefile.
2. **Milestone 2**: Strict configuration parser and domain validator.
3. **Milestone 3**: Grid representation, cardinal bitmasks, and coherence engine.
4. **Milestone 4**: Embedded "42" pattern masking and clearance verification.
5. **Milestone 5**: Dual-mode maze generation core (Prim's Spanning Tree + Braided Pac-Man).
6. **Milestone 6**: Optimal BFS pathfinding solver.
7. **Milestone 7**: Package distribution (`mazegen-*.whl` and `mazegen-*.tar.gz`).
8. **Milestone 8**: Interactive ANSI terminal visualizer with dynamic color rotation.
9. **Milestone 9**: CLI integration (`a_maze_ing.py`) and Chapter 4.5 file export.
10. **Milestone 10**: Comprehensive testing, strict type checking (`mypy --strict`), and documentation.

The milestone progression allowed testing and verifying every layer before building upon it, ensuring that zero regressions or architectural rewrites were required.

### What Worked Well & What Could Be Improved
- **What Worked Well**:
  - Adopting `mypy --strict` and `flake8` from Step 1 eliminated type bugs and formatting errors early.
  - Designing `Grid` with atomic operations (`grid.remove_wall_between`) made wall incoherence bugs impossible by construction.
  - Decoupling visualizer IO with dependency-injected input functions enabled automated testing of interactive CLI menus without hanging test runners.
- **What Could Be Improved**:
  - Adding an optional graphical renderer using Pygame or Tkinter alongside the terminal visualizer for desktop environments.

### Specific Tools Used
- **Language**: Python 3.14 (compatible with $\ge 3.10$).
- **Linters & Static Analyzers**: `flake8`, `mypy --strict`.
- **Test Framework**: `pytest` (46 unit tests covering all modules).
- **Packaging Tools**: `build`, `wheel`, `setuptools`.
- **Version Control**: `git`.

---

## Resources & AI Usage

### Classical References
- **Prim's Algorithm**: Robert C. Prim (1957), *Shortest Connection Networks and Some Generalizations*.
- **Breadth-First Search (BFS)**: Edward F. Moore (1959), *The Shortest Path Through a Maze*.
- **Maze Generation & Classification**: Jamis Buck (2015), *Mazes for Programmers: Code Your Own Twisty Little Passages*.
- **Python Packaging Authority**: PEP 517, PEP 518, and PEP 621 packaging specifications.
- **PEP 257**: Docstring Conventions.

### AI Assistance Disclosure
In compliance with the 42 AI directives (Chapter 2 & Chapter 7):
- **Ideation & Architecture**: AI was used as a pair programming partner to discuss graph invariants, compare maze generation algorithms (Prim's vs DFS backtracker for spanning trees), and review edge cases in the 42 subject specification.
- **Validation & Refactoring**: AI assisted in reviewing regexes, verifying bitmask combinations, formulating comprehensive test cases covering edge cases (such as collision detection and boundary checks), and ensuring compliance with `flake8` and `mypy --strict`.
- **Human Responsibility**: All algorithms, architectural decisions, mathematical proofs, and code implementations were critically verified, tested, and validated.
