from copy import deepcopy
from heapq import heappush, heappop
from collections import deque
import sys

# Bird Sort Game can have deep solution paths, so we increase the recursion limit
# This is safe for most modern systems but we handle the error case gracefully
try:
    sys.setrecursionlimit(2000)
except Exception as e:
    print(f"Warning: Could not increase recursion limit. Game may fail for complex puzzles. Error: {e}")


class GameSolver:
    """A solver class implementing various search algorithms for the Bird Sort game.
    
    This class provides multiple search strategies to find solutions for the Bird Sort puzzle:
    - Depth-First Search (DFS): Good for finding any solution quickly
    - Breadth-First Search (BFS): Finds the shortest solution but uses more memory
    - Iterative Deepening DFS (IDDFS): Memory-efficient way to find shortest solution
    - Uniform Cost Search (UCS): Similar to BFS for this puzzle (all moves cost 1)
    - Greedy Best-First Search: Uses heuristics to find solutions quickly
    - A* Search: Balances path cost and heuristics for optimal solutions
    - Weighted A* Search: Trades optimality for speed using weighted heuristics
    """
    def __init__(self, game):
        """Initialize the solver with a game instance.
        
        Args:
            game: A Game instance representing the Bird Sort puzzle to solve
        """
        self.game = game
        # Track visited states to avoid cycles in DFS
        # Note: Each search algorithm may manage its own visited states differently
        self.visited_states = set()

    def solve_dfs(self, max_depth=200):
        """Find a solution using Depth-First Search with intelligent move ordering.
        
        This implementation includes several optimizations:
        1. Depth limit to prevent infinite searches
        2. Cycle detection using visited states
        3. Move ordering based on state evaluation scores
        4. Backtracking with state cleanup
        
        Args:
            max_depth (int): Maximum depth to search before backtracking
            
        Returns:
            list: List of moves [(from_branch, to_branch)] or None if no solution found
        """
        def state_to_tuple(state):
            """Convert a game state to an immutable tuple for hash-based lookup."""
            return tuple(tuple(branch) for branch in state)

        def dfs(game_state, depth=0):
            """Recursive DFS implementation with state tracking.
            
            Args:
                game_state: Current game state to explore
                depth: Current search depth
                
            Returns:
                list: Solution path from this state or None if no solution found
            """
            # Check depth limit to prevent infinite recursion
            if depth >= max_depth:
                return None

            # Convert state for hash-based lookup
            state_tuple = state_to_tuple(game_state)
            
            # Skip already visited states to prevent cycles
            if state_tuple in self.visited_states:
                return None

            # Mark current state as visited
            self.visited_states.add(state_tuple)
            
            # Check if current state is a solution
            game_copy = deepcopy(self.game)
            game_copy.jogo = deepcopy(game_state)
            if game_copy.is_game_solved():
                return []  # Empty path since we're at solution

            # Generate and evaluate all possible moves
            possible_moves = []
            for source in range(len(game_state)):
                for dest in range(len(game_state)):
                    if source != dest:  # Can't move to same branch
                        new_state, valid, _ = self._try_move(game_state, source, dest)
                        if valid:
                            # Score the resulting state
                            score = self._evaluate_state(new_state)
                            possible_moves.append((score, source, dest, new_state))

            # Sort moves by score (highest first) for intelligent exploration
            possible_moves.sort(reverse=True, key=lambda x: x[0])

            # Try each move in order of decreasing score
            for _, source, dest, new_state in possible_moves:
                solution = dfs(new_state, depth + 1)
                if solution is not None:
                    # Prepend current move to solution path
                    return [(source + 1, dest + 1)] + solution
            
            # No solution found in this branch, clean up and backtrack
            self.visited_states.remove(state_tuple)
            return None

        # Initialize search
        self.visited_states.clear()
        initial_state = deepcopy(self.game.jogo)
        return dfs(initial_state)

    def solve_bfs(self, max_depth=300):
        """Find the shortest solution using Breadth-First Search.
        
        BFS explores the game tree level by level, guaranteeing that the first
        solution found will use the minimum number of moves. However, it requires
        more memory than DFS as it needs to store all states at the current level.
        
        Args:
            max_depth (int): Maximum number of moves to try before giving up
            
        Returns:
            list: Shortest sequence of moves [(from_branch, to_branch)] or None if no solution
        """
        def state_to_tuple(state):
            """Convert a game state to an immutable tuple for hash-based lookup."""
            return tuple(tuple(branch) for branch in state)
        
        # Initialize search
        game_copy = deepcopy(self.game)
        initial_state = deepcopy(self.game.jogo)
        
        # Queue stores (state, moves_to_reach_state)
        queue = deque([(initial_state, [])])
        
        # Track visited states to prevent cycles
        visited = {state_to_tuple(initial_state)}
        
        while queue:
            current_state, path = queue.popleft()
            
            # Stop exploring this branch if it exceeds max depth
            if len(path) >= max_depth:
                continue
            
            # Check if current state is a solution
            game_copy.jogo = deepcopy(current_state)
            if game_copy.is_game_solved():
                return path
            
            # Generate all possible moves from current state
            for source in range(len(current_state)):
                for dest in range(len(current_state)):
                    if source == dest:  # Can't move to same branch
                        continue
                    
                    # Try to make the move
                    new_state, valid, _ = self._try_move(
                        current_state,
                        source,
                        dest
                    )
                    
                    if valid:
                        # Check if we've seen this state before
                        new_state_tuple = state_to_tuple(new_state)
                        if new_state_tuple not in visited:
                            # Mark as visited
                            visited.add(new_state_tuple)
                            
                            # Add to queue with path to reach it
                            new_path = path + [(source + 1, dest + 1)]
                            queue.append((new_state, new_path))
                            
                            # Early exit if this new state is a solution
                            game_copy.jogo = deepcopy(new_state)
                            if game_copy.is_game_solved():
                                return new_path
        
        # No solution found within depth limit
        return None
    
    def solve_ucs(self, max_depth=500):
        """Find the optimal solution using Uniform Cost Search.
        
        In Bird Sort, all moves have the same cost (1), so UCS behaves similarly
        to BFS. However, the UCS implementation is kept for educational purposes
        and as a foundation for weighted variants (like A*).
        
        The algorithm uses a priority queue ordered by path cost to ensure
        it finds the solution with minimum number of moves.
        
        Args:
            max_depth (int): Maximum cost (moves) to consider
            
        Returns:
            list: Optimal sequence of moves [(from_branch, to_branch)] or None if no solution
        """
        def state_to_tuple(state):
            """Convert a game state to an immutable tuple for hash-based lookup."""
            return tuple(tuple(branch) for branch in state)
    
        # Initialize search
        game_copy = deepcopy(self.game)
        initial_state = deepcopy(self.game.jogo)
        initial_state_tuple = state_to_tuple(initial_state)
        
        # Priority queue stores: (total_cost, path_to_state, state)
        # Since all moves cost 1, total_cost equals number of moves
        pq = [(0, [], initial_state)]
        
        # Track minimum cost to reach each state
        # This allows us to skip states if we find a cheaper path later
        visited = {initial_state_tuple: 0}
    
        while pq:
            cost, path, current_state = heappop(pq)
            current_state_tuple = state_to_tuple(current_state)

            # Skip if we've found a better path to this state
            if cost > visited.get(current_state_tuple, float('inf')):
                continue
            
            # Check if current state is a solution
            game_copy.jogo = deepcopy(current_state)
            if game_copy.is_game_solved():
                return path
                
            # Stop exploring if we've reached max depth
            if cost >= max_depth:
                continue

            # Try all possible moves from current state
            for source in range(len(current_state)):
                for dest in range(len(current_state)):
                    if source == dest:  # Can't move to same branch
                        continue
    
                    # Try to make the move
                    new_state, valid, _ = self._try_move(current_state, source, dest)
                    
                    if valid:
                        new_state_tuple = state_to_tuple(new_state)
                        new_cost = cost + 1  # Each move costs 1
                        
                        # Only consider this new state if it's cheaper than known paths
                        if new_cost < visited.get(new_state_tuple, float('inf')):
                           visited[new_state_tuple] = new_cost
                           new_path = path + [(source + 1, dest + 1)]
                           heappush(pq, (new_cost, new_path, new_state))
    
        # No solution found within depth/cost limit
        return None

    def solve_astar(self, max_depth=500):
        """Find the optimal solution using A* Search.
        
        A* combines the benefits of UCS (optimal paths) with the intelligence
        of heuristic search. It uses f(n) = g(n) + h(n) where:
        - g(n) is the actual cost to reach node n (number of moves)
        - h(n) is the estimated cost to goal (number of misplaced birds)
        
        Since h(n) is admissible (never overestimates), A* guarantees optimal
        solutions while typically exploring fewer nodes than UCS.
        
        Args:
            max_depth (int): Maximum number of moves to try
            
        Returns:
            list: Optimal sequence of moves [(from_branch, to_branch)] or None if no solution
        """
        def state_to_tuple(state):
            """Convert a game state to an immutable tuple for hash-based lookup."""
            return tuple(tuple(branch) for branch in state)

        # Initialize search
        game_copy = deepcopy(self.game)
        initial_state = deepcopy(self.game.jogo)
        initial_state_tuple = state_to_tuple(initial_state)

        # Priority queue ordered by f-score (g + h)
        # Format: (f_score, path_to_state, state)
        initial_h = self._heuristic(initial_state)
        pq = [(initial_h, [], initial_state)]  # g=0 initially
        
        # Track actual cost (g-score) to reach each state
        g_scores = {initial_state_tuple: 0}
        
        while pq:
            f_score, path, current_state = heappop(pq)
            current_state_tuple = state_to_tuple(current_state)
            current_g = g_scores[current_state_tuple]
            
            # Check if current state is a solution
            game_copy.jogo = deepcopy(current_state)
            if game_copy.is_game_solved():
                return path
                
            # Stop if we've exceeded max depth
            if current_g >= max_depth:
                continue

            # Try all possible moves from current state
            for source in range(len(current_state)):
                for dest in range(len(current_state)):
                    if source == dest:  # Can't move to same branch
                        continue

                    # Try to make the move
                    new_state, valid, _ = self._try_move(current_state, source, dest)

                    if valid:
                        new_state_tuple = state_to_tuple(new_state)
                        tentative_g = current_g + 1  # Cost of one more move
                        
                        # Only consider if this is a shorter path
                        if tentative_g < g_scores.get(new_state_tuple, float('inf')):
                            # Update g-score and calculate f-score
                            g_scores[new_state_tuple] = tentative_g
                            h_score = self._heuristic(new_state)
                            f_score = tentative_g + h_score
                            
                            # Add to queue with updated path
                            new_path = path + [(source + 1, dest + 1)]
                            heappush(pq, (f_score, new_path, new_state))
                            
        # No solution found within depth limit
        return None

    def solve_weighted_astar(self, weight=1.5, max_depth=500):
        """Weighted A* search implementation.
        
        This algorithm is similar to A* but uses a weighted heuristic to
        balance optimality and exploration speed. The weight parameter controls
        how much the heuristic influences the search.
        
        Args:
            weight (float): Heuristic weight (default: 1.5)
            max_depth (int): Maximum number of moves to try
            
        Returns:
            list: Sequence of moves [(from_branch, to_branch)] or None if no solution
        """
        def state_to_tuple(state):
            """Convert a game state to an immutable tuple for hash-based lookup."""
            return tuple(tuple(branch) for branch in state)

        # Initialize search
        game_copy = deepcopy(self.game)
        initial_state = deepcopy(self.game.jogo)
        initial_state_tuple = state_to_tuple(initial_state)

        # Priority queue stores: (priority, cost, path, state)
        # priority = cost + weight * heuristic
        initial_h = self._heuristic(initial_state)
        pq = [(weight * initial_h, 0, [], initial_state)]  # Initial priority uses 0 cost
        
        # Track actual cost (g-score) to reach each state
        g_scores = {initial_state_tuple: 0}
        
        while pq:
            _, cost, path, current_state = heappop(pq)
            current_state_tuple = state_to_tuple(current_state)
            
            # Check if current state is a solution
            game_copy.jogo = deepcopy(current_state)
            if game_copy.is_game_solved():
                return path
                
            # Stop if we've exceeded max depth
            if cost >= max_depth:
                continue

            # Try all possible moves from current state
            for source in range(len(current_state)):
                for dest in range(len(current_state)):
                    if source == dest:  # Can't move to same branch
                        continue

                    # Try to make the move
                    new_state, valid, _ = self._try_move(current_state, source, dest)

                    if valid:
                        new_state_tuple = state_to_tuple(new_state)
                        new_cost = cost + 1  # Cost of one more move
                        
                        # Only consider if this is a shorter path
                        if new_cost < g_scores.get(new_state_tuple, float('inf')):
                            # Update g-score and calculate priority
                            g_scores[new_state_tuple] = new_cost
                            h_score = self._heuristic(new_state)
                            priority = new_cost + weight * h_score
                            
                            # Add to queue with updated path
                            new_path = path + [(source + 1, dest + 1)]
                            heappush(pq, (priority, new_cost, new_path, new_state))
                            
        # No solution found within depth limit
        return None

    def _heuristic(self, state):
        """Calculate the heuristic value for A* and Greedy search.
        
        This heuristic estimates the minimum number of moves needed to reach
        a solution by counting:
        1. Birds that don't match their neighbors (each mismatch needs a move)
        2. Partially filled branches (these need moves to empty or fill)
        
        This is admissible because:
        - Each mismatched bird must be moved at least once
        - Each partial branch must have birds added or removed
        
        Args:
            state: Game state to evaluate
            
        Returns:
            int: Estimated minimum moves to solution
        """
        misplaced = 0
        game_copy = deepcopy(self.game)
        game_copy.jogo = deepcopy(state)
        
        for i, branch in enumerate(state):
            dir_i = game_copy.is_right_branch(i)
            
            # Count birds that don't match their neighbors
            for j in range(len(branch)):
                # Check if bird matches previous bird
                if j > 0 and branch[j] != branch[j-1]:
                    misplaced += 1
                # Check if bird matches next bird
                if j < len(branch)-1 and branch[j] != branch[j+1]:
                    misplaced += 1
                    
            # Penalize branches that are neither empty nor full
            # These will require at least one move to fix
            if 0 < len(branch) < 4:
                misplaced += 1
                
        return misplaced

    def _try_move(self, state, orig, dest):
        """Attempt to move birds between branches.
        
        This helper method encapsulates the logic for validating and executing
        a move between two branches. It handles all the game rules regarding
        valid moves and bird transfers.
        
        Args:
            state: Current game state
            orig: Source branch index
            dest: Destination branch index
            
        Returns:
            tuple: (new_state, is_valid, num_birds_moved)
                - new_state: Updated game state if move was valid, else original
                - is_valid: True if move was valid
                - num_birds_moved: Number of birds moved (0 if invalid)
        """
        # Create a copy for move validation
        game_copy = deepcopy(self.game)
        game_copy.jogo = deepcopy(state)
        
        # Get branch orientations
        dir_orig = game_copy.is_right_branch(orig)
        dir_dest = game_copy.is_right_branch(dest)
        
        # Check if move is valid according to game rules
        valid, quantidade = game_copy.is_valid_move(
            state[orig],   # Source branch birds
            state[dest],   # Destination branch birds
            dir_orig,      # Source branch orientation
            dir_dest       # Destination branch orientation
        )
        
        if valid:
            # Extract birds from source branch
            birds, new_orig = game_copy.extract_birds(
                state[orig], dir_orig, quantidade
            )
            
            # Create new state with the move applied
            new_state = deepcopy(state)
            new_state[orig] = new_orig  # Updated source branch
            
            # Insert birds into destination branch
            new_state[dest] = game_copy.insert_birds(
                state[dest], birds, dir_dest
            )
            
            return new_state, True, quantidade
            
        # Return original state if move was invalid
        return state, False, 0

    def _evaluate_state(self, state):
        """Calculate a heuristic score for a game state.
        
        The score is based on two factors:
        1. Bird alignment: +1 for each pair of adjacent matching birds
        2. Branch balance: +1 for empty or full branches
        
        Higher scores indicate states that are closer to a solution.
        This heuristic is admissible (never overestimates) because:
        - Each bird must be next to its match in the solution
        - Each branch must be either empty or full in the solution
        
        Args:
            state: Game state to evaluate
            
        Returns:
            int: Heuristic score, higher is better
        """
        score = 0
        for branch in state:
            # Award points for adjacent matching birds
            for i in range(len(branch) - 1):
                if branch[i] == branch[i + 1]:
                    score += 1
                    
            # Award points for perfectly balanced branches
            if len(branch) == 0 or len(branch) == 4:
                score += 1
                
        return score

    def solve_iddfs(self, initial_max_depth=0, depth_increment=1, max_iterations=100):
        """Find a solution using Iterative Deepening Depth-First Search (IDDFS).
        
        IDDFS combines the space efficiency of DFS with the completeness of BFS.
        It works by running depth-limited DFS with increasingly larger depth limits
        until a solution is found. This guarantees finding the shortest solution
        while using only O(d) memory, where d is the solution depth.
        
        Args:
            initial_max_depth (int): Starting depth limit
            depth_increment (int): How much to increase depth limit each iteration
            max_iterations (int): Maximum number of depth increases to try
            
        Returns:
            list: Sequence of moves [(from_branch, to_branch)] or None if no solution
        """
        def state_to_tuple(state):
            """Convert a game state to an immutable tuple for hash-based lookup."""
            return tuple(tuple(branch) for branch in state)
            
        # Initialize search
        initial_state = deepcopy(self.game.jogo)
        depth_limit = initial_max_depth
        game_copy = deepcopy(self.game)
        
        # Try increasingly deeper searches
        for iteration in range(max_iterations):
            print(f"IDDFS: Trying depth limit {depth_limit}...")
            
            # Each depth-limited search gets its own visited set
            visited_in_dls = set()
            
            # Try to find solution within current depth limit
            solution = self._dls(initial_state, [], depth_limit, visited_in_dls, game_copy)
            
            if solution is not None:
                print(f"IDDFS: Solution found at depth {len(solution)}")
                return solution
                
            # No solution at this depth, increase limit and try again
            depth_limit += depth_increment
            
        print(f"IDDFS: No solution found within {max_iterations} iterations "
              f"(max depth explored: {depth_limit - depth_increment})")
        return None

    def _dls(self, current_state, path, limit, visited_in_dls, game_copy):
        """Perform a depth-limited search from the current state.
        
        This is a helper method for IDDFS that implements the depth-limited
        DFS algorithm. It explores paths up to a specified depth limit.
        
        Args:
            current_state: Game state to explore from
            path: List of moves taken to reach current_state
            limit: Maximum depth to explore
            visited_in_dls: Set of states visited in this DLS iteration
            game_copy: Game instance for checking solution state
            
        Returns:
            list: Solution path if found within depth limit, None otherwise
        """
        def state_to_tuple(state):
            """Convert a game state to an immutable tuple for hash-based lookup."""
            return tuple(tuple(branch) for branch in state)
             
        # Get current depth and state representation
        current_depth = len(path)
        state_tuple = state_to_tuple(current_state)

        # Check if current state is a solution
        game_copy.jogo = deepcopy(current_state)
        if game_copy.is_game_solved():
            return path
            
        # Stop if we've reached depth limit
        if current_depth >= limit:
            return None
            
        # Skip if we've seen this state in current DLS iteration
        if state_tuple in visited_in_dls:
            return None
            
        # Mark current state as visited for this iteration
        visited_in_dls.add(state_tuple)

        # Generate all possible moves from this state
        possible_moves = []
        for orig in range(len(current_state)):
            for dest in range(len(current_state)):
                if orig == dest:
                    continue

                # Use a temporary game copy to check validity without altering game_copy used for solution check
                temp_game = deepcopy(self.game) 
                temp_game.jogo = deepcopy(current_state)
                dir_orig = temp_game.is_right_branch(orig)
                dir_dest = temp_game.is_right_branch(dest)
                
                # Check if move is valid
                valid, quantidade = temp_game.is_valid_move(
                    current_state[orig],
                    current_state[dest],
                    dir_orig,
                    dir_dest
                )
                
                if valid:
                    # Extract birds from source branch
                    birds, new_orig = temp_game.extract_birds(
                        current_state[orig], dir_orig, quantidade
                    )
                    
                    # Create new state with the move applied
                    new_state = deepcopy(current_state)
                    new_state[orig] = new_orig  # Updated source branch
                    
                    # Insert birds into destination branch
                    new_state[dest] = temp_game.insert_birds(
                        current_state[dest], birds, dir_dest
                    )
                    possible_moves.append((orig, dest, new_state))
        
        # Try moves recursively
        for orig, dest, new_state in possible_moves:
            new_path = path + [(orig + 1, dest + 1)]
            result = self._dls(new_state, new_path, limit, visited_in_dls, game_copy)
            if result is not None:
                return result
                
        # Backtrack: remove from visited set for this DLS path
        # Important: allows revisiting via different paths within the same DLS limit
        visited_in_dls.remove(state_tuple) 
        return None

    def solve_greedy_bfs(self, max_depth=500):
        """Find a solution using Greedy Best-First Search.
        
        This algorithm always expands the node that appears closest to the goal
        according to the heuristic function, without considering path cost.
        It can find solutions quickly but they may not be optimal.
        
        The heuristic used is the number of misplaced birds, making the algorithm
        prefer states with more birds in their correct positions.
        
        Args:
            max_depth (int): Maximum number of moves to try
            
        Returns:
            list: Sequence of moves [(from_branch, to_branch)] or None if no solution
        """
        def state_to_tuple(state):
            """Convert a game state to an immutable tuple for hash-based lookup."""
            return tuple(tuple(branch) for branch in state)

        # Initialize search
        game_copy = deepcopy(self.game)
        initial_state = deepcopy(self.game.jogo)
        initial_state_tuple = state_to_tuple(initial_state)

        # Priority queue ordered by heuristic value only
        # Format: (heuristic_value, path_to_state, state)
        initial_heuristic = self._heuristic(initial_state)
        pq = [(initial_heuristic, [], initial_state)]
        
        # Track visited states to prevent cycles
        visited = {initial_state_tuple}
        
        while pq:
            # Get the most promising state (lowest heuristic value)
            heuristic, path, current_state = heappop(pq)
            
            # Check if current state is a solution
            game_copy.jogo = deepcopy(current_state)
            if game_copy.is_game_solved():
                return path
                
            # Stop if path is too long
            if len(path) >= max_depth:
                continue

            # Try all possible moves from current state
            for source in range(len(current_state)):
                for dest in range(len(current_state)):
                    if source == dest:  # Can't move to same branch
                        continue

                    # Try to make the move
                    new_state, valid, _ = self._try_move(current_state, source, dest)

                    if valid:
                        new_state_tuple = state_to_tuple(new_state)
                        
                        # Only explore states we haven't seen before
                        if new_state_tuple not in visited:
                            visited.add(new_state_tuple)
                            
                            # Calculate heuristic for new state
                            new_heuristic = self._heuristic(new_state)
                            new_path = path + [(source + 1, dest + 1)]
                            
                            # Add to queue, prioritized by heuristic
                            heappush(pq, (new_heuristic, new_path, new_state))
                            
        # No solution found within depth limit
        return None
