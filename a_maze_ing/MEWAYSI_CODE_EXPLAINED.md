# Mewaysi's Deep Code Guide: Line-by-Line Architecture & Explanations

> **Author / Student**: `mewaysi` (Lead Algorithm & Mathematics Engineer)  
> **Project**: A-Maze-ing (42 Curriculum)  
> **Purpose**: A comprehensive, simple yet deep architectural manual explaining every line of code you own, why it was written that way, and how to defend it during peer evaluation.

---

## Table of Contents
1. [Module 1: `src/mazegen/direction.py` (The Universal Compass & Vectors)](#1-module-1-srcmazegendirectionpy-the-universal-compass--vectors)
2. [Module 2: `src/mazegen/grid.py` (Cells, Wall Bitmasks & Coherence)](#2-module-2-srcmazegengridpy-cells-wall-bitmasks--coherence) *(Upcoming)*
3. [Module 3: `src/mazegen/pattern.py` (The 5x7 "42" Template & Clearance)](#3-module-3-srcmazegenpatternpy-the-5x7-42-template--clearance) *(Upcoming)*
4. [Module 4: `src/mazegen/generator.py` (Prim's Spanning Tree & Pac-Man Braiding)](#4-module-4-srcmazegeneratorpy-prims-spanning-tree--pac-man-braiding) *(Upcoming)*
5. [Module 5: `src/mazegen/solver.py` (BFS Shortest Path & Queue)](#5-module-5-srcmazegensolverpy-bfs-shortest-path--queue) *(Upcoming)*

---

# 1. Module 1: `src/mazegen/direction.py` (The Universal Compass & Vectors)

> **File Location**: [`src/mazegen/direction.py`](src/mazegen/direction.py)  
> **Lines**: 108  
> **Role**: The foundational compass of the entire project. It defines how walls are numbered in binary, how coordinates change when moving, and how opposite walls mirror each other.

---

### 1.1 Why `IntEnum`? (Design Decision)

```python
from enum import IntEnum

class Direction(IntEnum):
    NORTH = 1
    EAST  = 2
    SOUTH = 4
    WEST  = 8
```

#### Why not a standard string (`"NORTH"`)?
- Strings take more memory and require string comparisons (`"NORTH" == "NORTH"`).
- If you make a typo like `"NROTH"`, Python will not catch it until runtime.
- With an Enum, `mypy --strict` catches any invalid direction at compile time!

#### Why not a standard Python `Enum`?
- A standard Python `Enum` is a distinct object type that **cannot** participate in mathematical operations without explicitly casting: `int(Direction.NORTH.value)`.
- An **`IntEnum` (Integer Enum)** is a subclass of both `int` and `Enum`.
- **The Advantage**: `Direction.NORTH` is simultaneously a readable enum member AND the integer `1`. You can directly do bitwise arithmetic like `walls & Direction.NORTH` cleanly!

---

### 1.2 Why Powers of Two? ($1, 2, 4, 8$) & Binary Representation

Notice that the directions are assigned $1, 2, 4, 8$:

```
Binary Column:    [Bit 3]   [Bit 2]   [Bit 1]   [Bit 0]
Direction:         WEST      SOUTH     EAST      NORTH
Weight:              8         4         2         1
```

- **NORTH** = $2^0 = \mathbf{0001_2}$ (only bit 0 is set)
- **EAST**  = $2^1 = \mathbf{0010_2}$ (only bit 1 is set)
- **SOUTH** = $2^2 = \mathbf{0100_2}$ (only bit 2 is set)
- **WEST**  = $2^3 = \mathbf{1000_2}$ (only bit 3 is set)

#### Why is this mathematical genius for mazes?
Because each direction occupies **its own independent column** in binary, any combination of closed walls produces a completely unique sum from $0$ to $15$:

| Combination of Closed Walls | Calculation | Binary | Hexadecimal |
| :--- | :---: | :---: | :---: |
| **No walls** (open room) | $0$ | `0000` | `0x0` |
| **North only** | $1$ | `0001` | `0x1` |
| **East only** | $2$ | `0010` | `0x2` |
| **North + East** | $1 + 2 = 3$ | `0011` | `0x3` |
| **West only** | $8$ | `1000` | `0x8` |
| **North + South + West** | $1 + 4 + 8 = 13$ | `1101` | `0xD` |
| **All 4 walls closed** | $1 + 2 + 4 + 8 = 15$ | `1111` | `0xF` |

**Zero Collision**: No two combinations can ever produce the same number! All 4 walls are stored in a single 4-bit nibble.

---

### 1.3 The `delta` Property: Moving in 2D Coordinates

```python
@property
def delta(self) -> Tuple[int, int]:
    if self == Direction.NORTH:
        return (0, -1)
    if self == Direction.EAST:
        return (1, 0)
    if self == Direction.SOUTH:
        return (0, 1)
    return (-1, 0)
```

#### Why is North `(0, -1)` and South `(0, 1)`?
In mathematics class, the Y-axis goes upwards.  
**In computer memory, 2D arrays, and graphics grids, the Y-axis goes DOWNWARDS!**

```
             y = 0  ┌─────────────┐
             y = 1  │   (0, -1)   │  [NORTH: decrease y]
                    │      ▲      │
             y = 2  │ ◄──(x,y)──► │  [WEST: -1 x | EAST: +1 x]
                    │      ▼      │
             y = 3  │   (0, +1)   │  [SOUTH: increase y]
                    └─────────────┘
```

- Moving **NORTH** moves towards the top row $\rightarrow$ **decrease $y$**: `(x, y - 1)`.
- Moving **SOUTH** moves towards the bottom row $\rightarrow$ **increase $y$**: `(x, y + 1)`.
- Moving **EAST** moves right $\rightarrow$ **increase $x$**: `(x + 1, y)`.
- Moving **WEST** moves left $\rightarrow$ **decrease $x$**: `(x - 1, y)`.

---

### 1.4 The `opposite` Property: Reciprocal Symmetry

```python
@property
def opposite(self) -> "Direction":
    if self == Direction.NORTH: return Direction.SOUTH
    if self == Direction.EAST:  return Direction.WEST
    if self == Direction.SOUTH: return Direction.NORTH
    return Direction.EAST
```

#### Why is this necessary?
Every wall in a maze is shared between two adjacent cells:
- If Cell A looks **East** at Cell B...
- Then Cell B looks **West** at Cell A!

```
[ Cell A ]  ──(EAST)──►  [ Cell B ]
[ Cell A ]  ◄──(WEST)──  [ Cell B ]
```

When carving a doorway between two cells, you must open `direction` on Cell A and `direction.opposite` on Cell B simultaneously.

---

### 1.5 The Helper Factory Methods

#### 1. `from_char(char: str) -> Direction`
```python
c = char.upper()
if c == "N": return cls.NORTH
if c == "E": return cls.EAST
if c == "S": return cls.SOUTH
if c == "W": return cls.WEST
raise ValueError(f"Unknown direction character: '{char}'.")
```
- Converts output characters back into safe `Direction` objects.
- If someone passes an invalid character like `'Z'`, it throws a clear `ValueError` instead of causing a silent crash later.

#### 2. `from_delta(dx: int, dy: int) -> Direction`
```python
if dx == 0 and dy == -1: return cls.NORTH
if dx == 1 and dy == 0:  return cls.EAST
if dx == 0 and dy == 1:  return cls.SOUTH
if dx == -1 and dy == 0: return cls.WEST
raise ValueError(f"Invalid direction delta: ({dx}, {dy}).")
```
- Automatically identifies which direction was moved given two coordinate pairs:
  $$\text{Cell A}(2, 3) \rightarrow \text{Cell B}(3, 3) \implies dx = 3 - 2 = 1, dy = 0 \implies \text{EAST}$$

---

### 1.6 The 30-Second Evaluator Speech for `direction.py`

If an evaluator points to `direction.py`, say this:

> *"We chose an `IntEnum` with powers of two ($1, 2, 4, 8$) so that each cardinal direction acts as an independent bit in a 4-bit binary flag.*  
> *This allows any wall combination to be stored in a single 4-bit number ($0\text{xF}$), enabling $O(1)$ bitwise operations and directly mapping 1-to-1 with the project's hexadecimal file format.*  
> *The `delta` property provides coordinate offsets accounting for the screen coordinate convention where Y increases downwards, and the `opposite` property guarantees reciprocal two-way wall carving."*

---

### 1.7 Quick Verification Exercise

**Scenario**: You are at cell $(4, 5)$ and move in `Direction.NORTH`.
- `Direction.NORTH.delta` is `(0, -1)`.
- The new coordinate is $(4 + 0, 5 - 1) = \mathbf{(4, 4)}$.
