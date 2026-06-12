# EIACD Project

## About the Project

Bird Sort Puzzle is a puzzle game where the objective is to organize colored birds on branches by grouping birds of the same color together. The project implements both a manual gameplay mode and several search algorithms for automatic solving.

## How to Run

To run the project, execute the following command in the terminal:

```bash
python3 main.py
```

### Choose One of the Following Game Modes

1. **Manual Mode**: Play the game manually
2. **Play with Hints** (hint and undo)
3. **Automatic Mode**: Solved by an algorithm

### Board Size

* You can choose between different board sizes (4 to 12 branches)

## Manual Game Instructions

### Objective

* Group all birds of the same color on the same branch
* Each branch can hold a maximum of 4 birds

### How to Play

1. Enter the source branch number
2. Enter the destination branch number
3. The game will automatically move the maximum number of birds possible

### Movement Rules

* Only birds of the same color can be moved together
* Moves follow specific directions:

  * **Left Branches**:

    * Removal: right → left
    * Insertion: left → right
  * **Right Branches**:

    * Removal: left → right
    * Insertion: right → left

## Automatic Mode

### Available Algorithms

1. **BFS (Breadth-First Search)**

   * Finds the shortest solution
   * Slower on larger puzzles

2. **DFS (Depth-First Search)**

   * Quickly finds a solution
   * May not find the shortest solution

3. **IDDFS (Iterative Deepening DFS)**

   * Combines the efficiency of DFS with the optimality of BFS
   * Good balance between memory usage and solution quality

4. **UCS (Uniform Cost Search)**

   * Similar to BFS for this puzzle
   * All moves have equal cost

5. **Greedy BFS**

   * Very fast
   * Solutions may be suboptimal

6. **A***

   * Balances speed and solution quality
   * Uses intelligent heuristics

7. **Weighted A* (W = 1.5)**

   * Faster than A*
   * Sacrifices some solution quality for speed

## Victory Conditions

* All birds of the same color must be grouped on the same branch
* Branches must be either completely full (4 birds) or empty

## Possible Modifications

1. Change the puzzle size (4–12 branches)
2. Select different solving algorithms
3. Adjust algorithm parameters (e.g., the weight used in Weighted A*)

## Performance Analysis (benchmark.py)

The project includes a performance analysis tool that allows comparison of the efficiency of different algorithms.

### How to Run

To execute the benchmark, run the following command in the terminal:

```bash
python3 benchmark.py
```

### Features

* Runs each algorithm multiple times on different puzzle sizes
* Measures and records:

  * Average execution time
  * Standard deviation of execution time
  * Average number of moves
  * Standard deviation of moves
  * Success rate

### Default Settings

* Puzzle sizes tested: 4, 6, and 8 branches
* 3 runs per algorithm
* Time limits:

  * Size 4: 10 seconds
  * Size 6: 20 seconds
  * Size 8: 30 seconds

### Results

* Results are stored in the `benchmark_results` folder
* Each results file includes:

  * Date and time of execution
  * Configuration used
  * Detailed results for each puzzle size
* File naming format:

```text
benchmark_YYYYMMDD_HHMMSS.txt
```

## Project Structure

```text
.
├── main.py          # Program entry point
├── game.py          # Game implementation
├── solver.py        # Uninformed search algorithms
├── uninformed.py    # Informed search algorithms
├── benchmark.py     # Benchmark script (optional)
└── benchmark.txt    # Benchmark results
```
