import time
import signal
from statistics import mean, stdev
from datetime import datetime
from pathlib import Path
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

def format_results(size_results):
    """Format benchmark results as a string table."""
    lines = []
    lines.append("=== BENCHMARK RESULTS ===")
    header = f"{'Algorithm':<15} {'Avg Time (s)':<12} {'Std Time':<12} {'Avg Moves':<12} {'Std Moves':<12} {'Success %':<10}"
    lines.append(header)
    lines.append("-" * 73)
    
    for algo, stats in size_results.items():
        line = (f"{algo:<15} {stats['average_time']:<12.3f} {stats['std_time']:<12.3f} "
                f"{stats['average_moves']:<12.1f} {stats['std_moves']:<12.1f} {stats['success_rate']:<10.1f}")
        lines.append(line)
    
    return "\n".join(lines)

def save_results(all_results, sizes, trials, timeouts):
    """Save benchmark results to a file.
    
    Args:
        all_results (dict): Results for each size
        sizes (list): List of tested sizes
        trials (int): Number of trials per algorithm
        timeouts (dict): Timeout settings for each size
    """
    # Create results directory if it doesn't exist
    results_dir = Path("benchmark_results")
    results_dir.mkdir(exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = results_dir / f"benchmark_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        # Write header
        f.write("BIRD SORT PUZZLE BENCHMARK RESULTS\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Number of trials per algorithm: {trials}\n\n")
        
        # Write configuration
        f.write("Configuration:\n")
        f.write("-" * 20 + "\n")
        for size in sizes:
            f.write(f"Size {size}: timeout = {timeouts[size]} seconds\n")
        f.write("\n")
        
        # Write results for each size
        for size in sizes:
            f.write(f"\n{'='*20} Size {size} {'='*20}\n")
            f.write(format_results(all_results[size]))
            f.write("\n")
        
    print(f"\nResults saved to: {filename}")

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
    
    all_results = {}
    for size in sizes:
        print(f"\n{'='*20} Testing Size {size} {'='*20}")
        results = run_benchmark(size, trials, timeouts[size])
        print(format_results(results))
        all_results[size] = results
    
    # Save all results to file
    save_results(all_results, sizes, trials, timeouts)

if __name__ == "__main__":
    main()
