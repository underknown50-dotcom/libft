# Mewaysi's Study Notes: Graph Theory, Algorithms & Video Breakdown

> **Student**: `mewaysi` (Lead Algorithm & Mathematics Engineer)  
> **Project**: A-Maze-ing (42 Curriculum)  
> **Purpose**: Detailed breakdown of the 3 watched videos, core concepts, and direct code mappings for the 42 peer defense.

---

## Table of Contents
1. [Video 1: Computerphile — Maze Generation & Spanning Trees](#1-video-1-computerphile--maze-generation--spanning-trees)
2. [Video 2: The Coding Train — Maze Generator (Coding Challenge #10, Parts 1 & 2)](#2-video-2-the-coding-train--maze-generator-coding-challenge-10-parts-1--2)
3. [Video 3: The Coding Train — Breadth-First Search (Coding Challenge #68, Part 1)](#3-video-3-the-coding-train--breadth-first-search-coding-challenge-68-part-1)
4. [Side-by-Side Comparison: Video Code vs. Your 42 Python Code](#4-side-by-side-comparison-video-code-vs-your-42-python-code)
5. [Pen & Paper Math: Bitwise Arithmetic Proofs](#5-pen--paper-math-bitwise-arithmetic-proofs)
6. [Pac-Man Braiding & The 3x3 Void Invariant](#6-pac-man-braiding--the-3x3-void-invariant)
7. [Self-Check Defense Quiz](#7-self-check-defense-quiz)

---

## 1. Video 1: Computerphile — Maze Generation & Spanning Trees

> **Speaker**: Dr. Mike Pound (University of Nottingham)  
> **Core Topic**: Modeling mazes as mathematical graphs and spanning trees.

### Note 1.1: The Graph Representation of a Maze
- **Vertices (Nodes, $V$)**: Every cell $(x, y)$ on the grid is a node. Total nodes $V = \text{width} \times \text{height}$.
- **Edges (Passages, $E$)**: An edge is an open corridor connecting two adjacent cells (a carved wall).
- **Walls**: A wall is simply the **absence of an edge** between two neighboring nodes.
- **Code Link**: [`src/mazegen/grid.py`](src/mazegen/grid.py) (The `Cell` and `Grid` classes).

> **Defense Sentence**: *"We model the maze as an undirected graph where cells are vertices and open passages are edges."*

---

### Note 1.2: What Makes a Maze "Perfect"? (The Spanning Tree Invariant)
In graph theory, a "perfect" maze is mathematically a **Spanning Tree**:
1. **Fully Connected**: Every walkable cell can reach every other walkable cell (no trapped rooms).
2. **Acyclic (Zero Cycles)**: There are **zero loops**.
3. **The Spanning Tree Formula**:
   $$\text{Edges } E = V - 1$$
   *If a maze has $100$ cells, a perfect maze has exactly $99$ carved passages. Not $98$, not $100$.*
4. **Single Unique Path**: Because there are zero loops and full connectivity, there is **one and only one unique path** between `ENTRY` and `EXIT`.
- **Code Link**: [`src/mazegen/generator.py`: `_generate_perfect()`](src/mazegen/generator.py) (Randomized Prim's).

---

### Note 1.3: Algorithmic Biases (Why We Chose Prim's Over DFS)
Different maze generation algorithms create distinctly different visual styles ("biases"):

| Algorithm | How it Explores | Visual Bias | Gameplay / Solving Experience |
| :--- | :--- | :--- | :--- |
| **Recursive Backtracker (DFS)** | Dives as deep as possible along a single path before backtracking. | **High River Factor**: Long, winding, snake-like corridors with very few junctions. | **Trivial / Boring**: Players rarely have to make decisions; they just follow the long river. |
| **Randomized Prim's (Our Code)** | Grows outward uniformly from an active frontier of cells. | **High Branching Factor**: Short passages with numerous junctions and natural dead-ends. | **Challenging / Beautiful**: Highly engaging with realistic labyrinth complexity. |

---

### Note 1.4: The Bidirectional Wall Coherence Invariant
In an undirected graph, an edge between Node A and Node B works in both directions:
- When opening a passage between Cell 1 and Cell 2:
  - Cell 1 must open its wall towards Cell 2.
  - Cell 2 **must atomically open its reciprocal wall** towards Cell 1.
- If this is violated, you get an **invisible one-way wall** (the player can walk East, but is blocked walking West).
- **Code Link**: [`src/mazegen/grid.py`: `remove_wall_between()`](src/mazegen/grid.py):
  ```python
  cell1.open_wall(direction)
  cell2.open_wall(direction.opposite)
  ```

---

## 2. Video 2: The Coding Train — Maze Generator (Coding Challenge #10, Parts 1 & 2)

> **Speaker**: Daniel Shiffman  
> **Core Topic**: Grid setup, cell data representation, neighbor checks, and wall removal.

### Note 2.1: The Cell Object & Coordinate System
- Shiffman sets up a grid where each cell knows its row and column coordinates: $(i, j)$ in his code, $(x, y)$ in our code.
- In 2D computer graphics and grids:
  - $x$ (column) increases to the **right**.
  - $y$ (row) increases **downwards**.
  - Therefore, North is $(0, -1)$ and South is $(0, 1)$!
- **Code Link**: [`src/mazegen/direction.py`: `delta` property](src/mazegen/direction.py).

---

### Note 2.2: How Walls are Stored (Booleans vs Bitmasks)
- In the video, Shiffman creates an array of 4 booleans:
  `walls = [true, true, true, true]` (Top, Right, Bottom, Left).
- **Why our 42 code is more advanced**:
  Instead of 4 separate booleans, we use a single **4-bit integer bitmask**:
  `self.walls = 0xF` ($15 = 1111_2$).
  - North $= 1$ ($2^0$)
  - East $= 2$ ($2^1$)
  - South $= 4$ ($2^2$)
  - West $= 8$ ($2^3$)
  - *Benefits*: Uses $4\times$ less memory, executes in $O(1)$ bitwise operations, and translates directly into the single-character hexadecimal format (`0` to `F`) required by Chapter 4.5.
- **Code Link**: [`src/mazegen/grid.py`: `Cell` class](src/mazegen/grid.py).

---

### Note 2.3: Safe Neighbor Boundaries
- In Part 1, Shiffman highlights that boundary cells (on the edges of the grid) do not have 4 neighbors:
  - Top edge has no North neighbor.
  - Left edge has no West neighbor.
- You must always check bounds ($0 \le x < \text{width}$ and $0 \le y < \text{height}$) before accessing a neighbor.
- **Code Link**: [`src/mazegen/grid.py`: `get_neighbors()`](src/mazegen/grid.py).

---

### Note 2.4: Removing Walls Between Two Neighbors
- In Part 2, Shiffman computes the coordinate difference between `current` and `next`:
  - If `x - next.x == 1`: `next` is to the **West** of `current`.
  - If `x - next.x == -1`: `next` is to the **East** of `current`.
  - If `y - next.y == 1`: `next` is to the **North** of `current`.
  - If `y - next.y == -1`: `next` is to the **South** of `current`.
- Then he knocks down the wall on both cells simultaneously!
- **Code Link**: [`src/mazegen/grid.py`: `remove_wall_between()`](src/mazegen/grid.py).

---

## 3. Video 3: The Coding Train — Breadth-First Search (Coding Challenge #68, Part 1)

> **Speaker**: Daniel Shiffman  
> **Core Topic**: Queue data structure, wave expansion, and parent pointer backtracking.

### Note 3.1: The Queue (FIFO) & Expanding Rings
- BFS operates like ripples in a pond:
  1. Start at `ENTRY` (distance $0$).
  2. Visit all open neighbors at distance $1$.
  3. Visit all open neighbors at distance $2$, and so on.
- To enforce this orderly exploration, BFS requires a **Queue** (First-In, First-Out).
- **Code Link**: [`src/mazegen/solver.py`: `solve_bfs()`](src/mazegen/solver.py).

---

### Note 3.2: Why BFS Guarantees the Shortest Path
- In an unweighted maze, moving from any cell to an adjacent open cell always costs exactly **1 step**.
- Because BFS explores all paths of length $L$ before any path of length $L+1$, the **very first time** `EXIT` is popped from the queue, that path is mathematically proven to be the **shortest path**.
- *DFS does not have this property* (it explores deeply and finds an arbitrary, often huge path).

---

### Note 3.3: Parent Pointers & Backtracking
- In the video, Shiffman shows how each node remembers who discovered it:
  `parent[neighbor] = current`
- When `EXIT` is reached:
  1. Start at `EXIT`.
  2. Follow its parent pointer to the predecessor cell.
  3. Repeat until you arrive back at `ENTRY`.
  4. **Reverse the list** to get the forward path!
- In our code, we also store the cardinal direction:
  `parent[neighbor] = (current, direction)`
  allowing us to reconstruct the subject's exact `[NESW]*` move string (e.g. `"SSSEEENNNW"`).
- **Code Link**: [`src/mazegen/solver.py`: lines 44–65](src/mazegen/solver.py).

---

### Note 3.4: Performance — `deque.popleft()` vs `list.pop(0)`
- In Python, using `list.pop(0)` takes **$O(N)$ linear time** because all remaining elements shift to the left in RAM.
- We use `collections.deque.popleft()`, which takes **$O(1)$ constant time**.
- Checking `if cell in visited` uses a Python `set`, giving **$O(1)$ average lookup time**.

---

## 4. Side-by-Side Comparison: Video Code vs. Your 42 Python Code

| Feature | Daniel Shiffman's Video Code | Your 42 Python Code (`mewaysi`) | Why Your 42 Implementation is Better |
| :--- | :--- | :--- | :--- |
| **Language** | JavaScript (p5.js) | Python 3.10+ with `mypy --strict` | Type-safe, compliant with 42 curriculum standards. |
| **Wall Storage** | 4 Booleans: `[true, true, true, true]` | **Single 4-bit Integer Bitmask**: `0xF` ($1, 2, 4, 8$) | $4\times$ smaller memory footprint, $O(1)$ bitwise operations, direct 1-to-1 map to hex output (`0` to `F`). |
| **Maze Algorithm** | Recursive Backtracker (DFS) | **Randomized Prim's Algorithm** | Prim's produces a balanced branching factor with realistic dead-ends, avoiding DFS's boring "long river" corridors. |
| **Playable Arcade Mode** | None (Single tree only) | **Multi-Pass Braided Pac-Man Mode** | Eliminates dead-ends to create escape loops; strictly prevents $3 \times 3$ open rooms. |
| **Queue Implementation** | JS Array: `queue.shift()` | `collections.deque.popleft()` | $O(1)$ constant time queue removal without memory shifts. |

---

## 5. Pen & Paper Math: Bitwise Arithmetic Proofs

Evaluators often ask you to calculate bit operations by hand.

### Note 5.1: Powers of 2 as Independent Binary Flags
- **North** $= 1 = 2^0 = \mathbf{0001_2}$
- **East** $= 2 = 2^1 = \mathbf{0010_2}$
- **South** $= 4 = 2^2 = \mathbf{0100_2}$
- **West** $= 8 = 2^3 = \mathbf{1000_2}$
- **All Walls Closed**: $1 + 2 + 4 + 8 = 15 = \mathbf{1111_2} = \text{0xF}$

---

### Note 5.2: Pen & Paper Carving Proof
Suppose Cell A is at $(0, 0)$ with all walls closed (`1111` in binary).  
We want to carve open the **East** wall ($2 = `0010`$):

1. **Invert the Direction Mask** (`~Direction.EAST.value`):
   $$\sim 0010_2 = \dots 11111101_2$$
2. **Apply Bitwise AND** (`self.walls &= ~direction.value`):
   ```
       1111   (Current walls: all closed)
     & 1101   (Mask: East bit is 0, all others 1)
     ------
       1101   (= 13 in decimal = 0xD in hexadecimal)
   ```
3. **Open Reciprocal West Wall on Cell B $(1, 0)$**:
   $$\text{West} = 8 = 1000_2 \implies \sim 1000_2 = 0111_2$$
   ```
       1111   (Cell B: all closed)
     & 0111   (Mask: West bit is 0)
     ------
       0111   (= 7 in decimal = 0x7 in hexadecimal)
   ```
*Result*: Cell A has `0xD` and Cell B has `0x7`. The passage is open in both directions!

---

## 6. Pac-Man Braiding & The 3x3 Void Invariant

> **Subject Reference**: Chapter 4.4 (`PERFECT=False`)

1. **What is Braiding?**
   - A dead-end is a cell where 3 out of 4 walls are closed (`wall_count == 3`).
   - Braiding scans the grid for dead-ends and carves open an additional wall into an adjacent corridor. This creates loops, eliminating dead-ends so ghosts cannot trap players.
2. **The 3x3 Open Space Rule**:
   - The subject strictly forbids open areas $\ge 3 \times 3$. Corridors must remain $\le 2$ cells wide.
   - **How `would_create_3x3_open_area` works**: Before carving a wall between `c1` and `c2`, it inspects all 4 overlapping $3 \times 3$ subgrids that contain both cells. If opening the wall would remove all internal walls in any $3 \times 3$ block, the carving is aborted.
- **Code Link**: [`src/mazegen/generator.py`: `would_create_3x3_open_area()`](src/mazegen/generator.py).

---

## 7. Self-Check Defense Quiz

Test your memory with these quick questions:

1. **Q**: What formula proves a graph is a tree?  
   **A**: $E = V - 1$ (where $E$ is edges and $V$ is vertices), with connectivity and no cycles.
2. **Q**: Why is `collections.deque` faster than a Python `list` for BFS?  
   **A**: `deque.popleft()` is $O(1)$ constant time; `list.pop(0)` is $O(N)$ linear time because all remaining elements shift in memory.
3. **Q**: How do you calculate whether a cell has a South wall closed?  
   **A**: `bool(cell.walls & Direction.SOUTH.value)`. If the bit is 1, it evaluates to `True`.
4. **Q**: What makes Prim's mazes better for gameplay than DFS mazes?  
   **A**: Prim's has a high branching factor with short paths and many dead-ends. DFS has a high river factor with long, obvious corridors that are too easy to solve.
