import time
import signal
from statistics import mean, stdev
from game import Game
from algorithms import GameSolver

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException()

def run_benchmark(size, num_trials=5, timeout_seconds=30):
    """Run benchmark for a specific puzzle size.
    
    Args:
        size (int): Size of the puzzle (number of branches)
        num_trials (int): Number of times to run each algorithm
        
    Returns:
        dict: Results for each algorithm containing:
            - average_time: Mean execution time in seconds
            - std_time: Standard deviation of execution time
            - average_moves: Mean number of moves in solution
            - std_moves: Standard deviation of number of moves
            - success_rate: Percentage of successful solves
    """
    algorithms = {
        'BFS': lambda solver: solver.solve_bfs(),
        'DFS': lambda solver: solver.solve_dfs(),
        'IDDFS': lambda solver: solver.solve_iddfs(),
        'UCS': lambda solver: solver.solve_ucs(),
        'Greedy BFS': lambda solver: solver.solve_greedy_bfs(),
        'A*': lambda solver: solver.solve_astar(),
        'Weighted A*': lambda solver: solver.solve_weighted_astar()
    }
    
    results = {}
    
    for algo_name, algo_func in algorithms.items():
        print(f"\nTesting {algo_name} with size {size}...")
        times = []
        moves = []
        successes = 0
        
        for trial in range(num_trials):
            print(f"  Trial {trial + 1}/{num_trials}...", end='', flush=True)
            
            # Create new game instance
            game = Game(size)
            solver = GameSolver(game)
            
            # Set up timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_seconds)
            
            try:
                # Run algorithm and measure time
                start_time = time.time()
                solution = algo_func(solver)
                end_time = time.time()
                signal.alarm(0)  # Disable alarm
            except TimeoutException:
                print(f" Timeout ({timeout_seconds}s)")
                signal.alarm(0)  # Disable alarm
                continue
            
            if solution:
                successes += 1
                times.append(end_time - start_time)
                moves.append(len(solution))
                print(" ✓")
            else:
                print(" ✗")
        
        # Calculate statistics
        if successes > 0:
            results[algo_name] = {
                'average_time': mean(times),
                'std_time': stdev(times) if len(times) > 1 else 0,
                'average_moves': mean(moves),
                'std_moves': stdev(moves) if len(moves) > 1 else 0,
                'success_rate': (successes / num_trials) * 100
            }
        else:
            results[algo_name] = {
                'average_time': float('inf'),
                'std_time': 0,
                'average_moves': float('inf'),
                'std_moves': 0,
                'success_rate': 0
            }
    
    return results

def print_results(size_results):
    """Print benchmark results in a formatted table."""
    print("\n=== BENCHMARK RESULTS ===")
    print(f"{'Algorithm':<15} {'Avg Time (s)':<12} {'Std Time':<12} {'Avg Moves':<12} {'Std Moves':<12} {'Success %':<10}")
    print("-" * 73)
    
    for algo, stats in size_results.items():
        print(f"{algo:<15} {stats['average_time']:<12.3f} {stats['std_time']:<12.3f} "
              f"{stats['average_moves']:<12.1f} {stats['std_moves']:<12.1f} {stats['success_rate']:<10.1f}")

def main():
    # Using smaller sizes and fewer trials for quicker testing
    sizes = [4, 6, 8]  # Reduced from [6, 8, 12]
    trials = 3  # Reduced from 5
    
    # Different timeouts for different sizes
    timeouts = {
        4: 10,   # 10 seconds for size 4
        6: 20,   # 20 seconds for size 6
        8: 30    # 30 seconds for size 8
    }
    
    for size in sizes:
        print(f"\n{'='*20} Testing Size {size} {'='*20}")
        results = run_benchmark(size, trials, timeouts[size])
        print_results(results)

if __name__ == "__main__":
    main()
