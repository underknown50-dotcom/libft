# A-Maze-ing: Team Work Division & Peer Defense Guide

This guide details the division of responsibilities, module ownership, cross-teaching protocol, and 42 peer-evaluation preparation for **mewaysi** and **mal-jama**.

---

## 1. High-Level Architecture & Ownership Split

At 42, **both team members must understand 100% of the project**. The codebase is logically divided into two complementary halves:

- **mewaysi**: **Core Engine & Graph Algorithms** (Bitwise wall manipulation, grid coherence, Prim's spanning tree generation, Pac-Man braiding, BFS shortest path solver).
- **mal-jama**: **Architecture, Interface & Pipeline** (Configuration parser, "42" pattern masking, terminal visualizer, file exporter, CLI entrypoint, Makefile & packaging).

```
                            [ config.txt ]
                                  │
                (mal-jama) config.py (Parser & Validation)
                                  │
    ┌─────────────────────────────┴─────────────────────────────┐
    │                                                           │
 (mewaysi) grid.py & direction.py                       (mal-jama) pattern.py
(Bitwise representation)                                ("42" Masking)
    │                                                           │
    └─────────────────────────────┬─────────────────────────────┘
                                  │
                     (mewaysi) generator.py
                     (Prim's Tree + Pac-Man Braiding)
                                  │
                     (mewaysi) solver.py
                     (BFS Shortest Path)
                                  │
    ┌─────────────────────────────┴─────────────────────────────┐
    │                                                           │
(mal-jama) exporter.py                                  (mal-jama) visualizer.py
(maze.txt hex output)                                   (ANSI Terminal UI)
    └─────────────────────────────┬─────────────────────────────┘
                                  │
                    (mal-jama) a_maze_ing.py
                     (CLI Entrypoint, Makefile & Packaging)
```

---

## 2. Detailed Ownership Breakdown

### Module A: `mewaysi` (Core Engine & Graph Algorithms)

You own the mathematical representation, graph theory, maze generation, and optimal pathfinding.

| File | Responsibilities & Functions | Key Concepts to Master |
| :--- | :--- | :--- |
| `src/mazegen/direction.py` | `Direction` IntEnum | Bitmask powers of 2 (`NORTH=1`, `EAST=2`, `SOUTH=4`, `WEST=8`), coordinate deltas `(dx, dy)`, `opposite` property. |
| `src/mazegen/grid.py` | `Cell` & `Grid` classes | Bitwise operators (`&`, `\|`, `~`), dual-wall synchronization (opening South at `(x, y)` automatically opens North at `(x, y+1)`), `is_coherent()` audit. |
| `src/mazegen/generator.py` | `MazeGenerator` | **Randomized Prim’s Algorithm** (Spanning Tree, zero cycles), **Pac-Man braiding** (opening corners/centre, eliminating dead-ends), preventing $3 \times 3$ open voids (`would_create_3x3_open_area`). |
| `src/mazegen/solver.py` | `solve_bfs()` | **Breadth-First Search (BFS)** with `collections.deque`, shortest path optimality on unweighted graphs, parent-pointer path reconstruction (`"SESW..."`). |
| **Associated Tests** | `tests/test_grid.py`<br>`tests/test_generator.py`<br>`tests/test_solver.py` | Validating wall bitmasks, tree connectivity, BFS shortest path correctness. |

---

### Module B: `mal-jama` (Architecture, Interface & Pipeline)

Your teammate owns the input/output boundaries, visual presentation, pattern overlay, and distribution packaging.

| File | Responsibilities & Functions | Key Concepts to Master |
| :--- | :--- | :--- |
| `src/mazegen/config.py` | `parse_config()`, `Config` dataclass, custom exceptions | Strict key-value validation, type casting, bounds checking ($\text{width} \ge 3$, coordinates in grid, $\text{entry} \neq \text{exit}$). |
| `src/mazegen/pattern.py` | `apply_pattern_42()`, `can_fit_pattern()` | Centering formula ($7 \times 5$ bounding box), collision checks with entry/exit, graceful omission when grid is too small. |
| `src/mazegen/exporter.py` | `export_maze()`, `verify_maze_file()` | Chapter 4.5 formatting (Hex lines, empty separator, entry, exit, directional `[NESW]` string), step-by-step path audit. |
| `src/mazegen/visualizer.py` | `InteractiveVisualizer` | ANSI color escape sequences, square block aspect-ratio correction (`██`), real-time interactive menu loop (1–4). |
| `a_maze_ing.py` & Build | `main()`, `Makefile`, `pyproject.toml` | CLI arguments handling, exit codes ($0$ on success, non-zero on error), wheel packaging (`mazegen-*.whl`). |
| **Associated Tests** | `tests/test_config.py`<br>`tests/test_pattern.py`<br>`tests/test_visualizer.py`<br>`tests/test_cli_and_export.py`<br>`tests/test_package.py` | Validating edge cases: syntax errors, small grids, out-of-bounds coords, packaging compliance. |

---

## 3. Step-by-Step Cross-Teaching Protocol

Follow these 4 steps to guarantee both members master the entire project before peer evaluation:

### Step 1: Individual Deep Dive (1 Hour)
- **`mewaysi`**: Read `WALKTHROUGH.md` Section 3 (Bitwise math), Section 4 (Prim's & Pac-Man), and Section 5 (BFS Solver).
- **`mal-jama`**: Read `WALKTHROUGH.md` Section 1 (Packaging), Section 2 (Config Parsing), and Section 6 (Visualizer & Exporter).

### Step 2: Mutual Code Walkthrough (30–45 Minutes)
Sit together or share screens to teach each other your modules:

1. **`mewaysi` presents to `mal-jama` (15–20 min) — Core Engine, Math & Graph Theory**:
   - **`src/mazegen/direction.py`**:
     - Explain why `Direction` inherits from `IntEnum` (allows direct bitwise arithmetic without type casting).
     - Show the powers of 2: North ($1$), East ($2$), South ($4$), West ($8$), and why each gets its own binary column (`0001`, `0010`, `0100`, `1000`).
     - Explain `delta` coordinates: North is `(0, -1)` and South is `(0, 1)` because in 2D computer grid arrays Y increases downward.
   - **`src/mazegen/grid.py`**:
     - Explain why `walls = 15` (`1111` in binary, `0xF` in hex) means all 4 walls are closed at initialization.
     - Demonstrate bitwise operations on paper: `&` checks walls, `|` closes walls, and `&= ~` opens/carves walls.
     - Explain `remove_wall_between()` and Wall Coherence (`is_coherent()`): why carving between neighbors must symmetrically open East on Cell A and West on Cell B.
   - **`src/mazegen/generator.py`**:
     - **Randomized Prim's Algorithm**: Walk through the `candidate_walls` list (stored on Heap memory, completely avoiding recursion stack overflow), and why `if target_position in visited_cells: continue` guarantees a Spanning Tree with **zero loops**.
     - **Pac-Man Braiding (`PERFECT=False`)**: Show how the 4 corners are opened, and how dead-ends (`closed_walls_count == 3`) are eliminated by carving extra exits.
     - **The $3 \times 3$ Void Invariant**: Explain `is_3x3_box_open()` checking the 12 internal walls (6 horizontal + 6 vertical) and how `would_create_3x3_open_area()` does an atomic trial run before breaking any wall.
   - **`src/mazegen/solver.py`**:
     - Explain why **BFS** is mathematically guaranteed to find the shortest path on unweighted graphs (explores in concentric distance waves).
     - Explain why `collections.deque` is used instead of a standard Python `list` ($O(1)$ `popleft()` pointer unlinking vs slow $O(N)$ memory shifting).
     - Show how `parent_tracker` drops breadcrumbs and how `reconstruct_shortest_path()` backtracks from Exit to Entry and reverses.

2. **`mal-jama` presents to `mewaysi` (15–20 min) — Interfaces, Packaging & Architecture**:
   - **`src/mazegen/config.py`**:
     - Walk through `parse_config()`: Demonstrate strict key-value parsing (`WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`).
     - Show boundary validation ($\text{width} \ge 3$, coordinates within grid, `ENTRY != EXIT`) and custom exceptions (`ConfigValueError`, `ConfigSyntaxError`).
   - **`src/mazegen/pattern.py`**:
     - Explain the $5 \times 7$ bitmap in `PATTERN_42` and the functional set comprehension in `get_pattern_cells_at()`.
     - Explain the $+2$ clearance rule ($9 \times 7$ minimum grid) to guarantee a walkable corridor around the logo.
     - Show centering math `(width - 7) // 2` and how `can_fit_pattern()` safely omits the pattern with a notice to `sys.stderr` on collision.
   - **`src/mazegen/exporter.py`**:
     - Walk through Chapter 4.5 formatting: Hex rows, empty separator line, entry, exit, and directional solution string.
     - Explain `verify_maze_file()`: How it audits output files for wall collisions, bounds, and physical coherence.
   - **`src/mazegen/visualizer.py` & CLI**:
     - Show the interactive menu loop (Options 1–4): dynamic ANSI color rotation, path toggle (`ON`/`OFF`), and regeneration.
     - Show square block aspect-ratio handling (`██` for cells and walls).
   - **Packaging & Distribution (`pyproject.toml`, `Makefile`, `__init__.py`)**:
     - Demonstrate `make package` building `mazegen-1.0.0-py3-none-any.whl` at repo root.
     - Explain `__all__` in `__init__.py` protecting internal helpers from public namespace pollution.

### Step 3: Git Branching & Contribution Log
To ensure your Git commit history reflects both members:
1. `mewaysi` creates and commits to: `feature/algorithms-and-engine`
2. `mal-jama` creates and commits to: `feature/interface-and-config`
3. Review each other's pull requests before merging into `master`.

### Step 4: Role-Reversal Mock Defense (Practice Drill)
During practice, intentionally swap roles:
- Ask `mewaysi` questions about configuration validation, pattern placement, and packaging.
- Ask `mal-jama` questions about Prim's algorithm, BFS, and bitwise wall masks.

---

## 4. Peer Defense Cheat Sheet (Q&A for Both Members)

| Defense Question | Primary Owner | What **BOTH** of You Must Answer |
| :--- | :---: | :--- |
| **Why use powers of 2 (1, 2, 4, 8) for wall directions?** | `mewaysi` | Each wall maps to 1 bit in a 4-bit binary number ($2^0=1$ North, $2^1=2$ East, $2^2=4$ South, $2^3=8$ West). Combining them gives values $0$ to $15$, which directly maps 1-to-1 to a single hexadecimal character (`0` to `F`). |
| **Why choose Randomized Prim's over DFS (Recursive Backtracker)?** | `mewaysi` | DFS creates long, winding corridors with few branches. Prim's grows uniformly from an active frontier, creating complex, balanced labyrinths with high branching factors while guaranteeing zero cycles (Spanning Tree). |
| **Why BFS instead of DFS or A\* for pathfinding?** | `mewaysi` | On an unweighted 2D grid, BFS mathematically guarantees the **shortest path** in $O(V + E)$ time. DFS does not guarantee the shortest path, and A\* requires a heuristic while BFS is already instantaneous. |
| **How does Pac-Man mode avoid $3 \times 3$ rooms?** | `mewaysi` | Chapter 4.4 strictly forbids $3 \times 3$ open voids. `would_create_3x3_open_area` inspects all 9 possible overlapping $3 \times 3$ subgrids containing that wall before carving it. |
| **What happens if the maze is too small for the "42" pattern?** | `mal-jama` | The pattern requires a $7 \times 5$ bounding box plus margins. If the grid is smaller, or if the pattern collides with `ENTRY` or `EXIT`, `can_fit_pattern` returns `False`, prints an informative message, and safely omits it. |
| **Why validate `ENTRY != EXIT`?** | `mal-jama` | If entry and exit are the same cell, the path is 0 steps, which is a degenerate case that violates the maze problem specification. |
| **Where is the wheel package and how is it tested?** | `mal-jama` | Chapter 6 requires a `.whl` package. Run `make package`, which builds `dist/mazegen-1.0.0-py3-none-any.whl` and copies it to the repo root. It installs via `pip install mazegen-1.0.0-py3-none-any.whl`. |

---

## 5. Quick Verification Commands

```bash
# 1. Run all 46 unit tests
make test

# 2. Run strict type checking (19 files, 0 errors)
make lint-strict

# 3. Run style checks
make lint

# 4. Build wheel package to repo root
make package

# 5. Run the application with default config
make run
```
