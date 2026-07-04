# EIACD Project

## About the Project

Bird Sort Puzzle is a puzzle game where the objective is to organize colored birds on branches by grouping birds of the same color together. This project implements several classical search algorithms to automatically solve randomly generated puzzle instances and provides benchmarking tools to compare their performance.

## How to Run

To run the project, execute:

```bash
python3 main.py
```

### Configuration

When the program starts, you will be prompted to:

1. Select the board size (4–12 branches).
2. Choose one of the available search algorithms.

The selected algorithm will then compute and display a step-by-step solution to the puzzle.

## Available Algorithms

1. **Breadth-First Search (BFS)**

   * Finds the shortest solution.
   * Computationally expensive for larger puzzles.

2. **Depth-First Search (DFS)**

   * Quickly finds a solution.
   * Does not guarantee the shortest solution.

3. **Iterative Deepening Depth-First Search (IDDFS)**

   * Combines the space efficiency of DFS with the completeness of BFS.
   * Suitable for exploring increasing search depths.

4. **Uniform Cost Search (UCS)**

   * Expands states according to path cost.
   * Equivalent to BFS in this problem since all moves have equal cost.

5. **Greedy Best-First Search**

   * Prioritizes states using a heuristic function.
   * Very fast, although solutions may be suboptimal.

6. **A\***

   * Combines path cost and heuristic information.
   * Provides a good balance between solution quality and execution time.

7. **Weighted A\***

   * Variant of A* using a weighted heuristic.
   * Faster than standard A* while potentially sacrificing optimality.

## Goal State

A solution is reached when:

* Each branch is either empty or contains four birds of the same color.
* All birds of the same color are grouped together.

## Performance Analysis (`benchmark.py`)

The project includes a benchmarking script for comparing the performance of the implemented search algorithms.

### Running the Benchmark

```bash
python3 benchmark.py
```

### Metrics

For each algorithm and board size, the benchmark reports:

* Average execution time
* Standard deviation of execution time
* Average solution length
* Standard deviation of solution length
* Success rate

### Default Configuration

* Board sizes: 4, 6 and 8 branches
* Three executions per algorithm
* Time limits:
  * Size 4: 10 seconds
  * Size 6: 20 seconds
  * Size 8: 30 seconds

Benchmark results are automatically saved in the `benchmark_results` directory.

## Project Structure

```text
.
├── main.py          # Program entry point
├── game.py          # Bird Sort game implementation
├── algorithms.py    # Search algorithm implementations
├── benchmark.py     # Benchmarking script
├── benchmark.txt    # Example benchmark results
└── README.md
```
