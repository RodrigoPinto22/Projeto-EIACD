from copy import deepcopy
from heapq import heappush, heappop
from collections import deque
import sys # Needed for IDDFS max depth

# Increase Python's recursion depth limit for potentially deep searches
# Be cautious with this, depends on system resources
try:
    sys.setrecursionlimit(2000)
except Exception as e:
    print(f"Warning: Could not set recursion depth limit. {e}")

class GameSolver:
    def __init__(self, game):
        self.game = game
        # Restore visited_states for DFS compatibility
        self.visited_states = set()
        # Note: visited_states might not be ideal for IDDFS as states are revisited
        # We'll manage visited states within each DLS call

    def solve_dfs(self, max_depth=200):
        """DFS implementation to find a solution with improved pruning and priority handling."""
        def state_to_tuple(state):
            return tuple(tuple(branch) for branch in state)

        def dfs(game_state, depth=0):
            if depth >= max_depth:
                return None

            state_tuple = state_to_tuple(game_state)
            if state_tuple in self.visited_states:
                return None

            self.visited_states.add(state_tuple)
            
            game_copy = deepcopy(self.game) # Use a copy to check if solved
            game_copy.jogo = deepcopy(game_state)
            if game_copy.jogo_finalizado():
                 # If solved, clear visited_states for potential future calls if needed
                 # self.visited_states.clear() # Optional: depends if solver instance is reused
                 return []

            possible_moves = []
            for orig in range(len(game_state)):
                for dest in range(len(game_state)):
                    if orig != dest:
                        # Use _try_move which handles copying
                        new_state, valid, _ = self._try_move(game_state, orig, dest)
                        if valid:
                            score = self._evaluate_state(new_state) # Evaluate potential move
                            possible_moves.append((score, orig, dest, new_state))

            # Prioritize moves with higher scores (more aligned birds)
            possible_moves.sort(reverse=True, key=lambda x: x[0])

            for _, orig, dest, new_state in possible_moves:
                solution = dfs(new_state, depth + 1)
                if solution is not None:
                    return [(orig + 1, dest + 1)] + solution
            
            # Backtrack: Remove state if no solution found down this path
            # This is crucial for DFS to explore other branches correctly
            if state_tuple in self.visited_states:
                 self.visited_states.remove(state_tuple)
            return None

        # Start DFS
        self.visited_states.clear() # Clear before starting a new search
        initial_state = deepcopy(self.game.jogo)
        result = dfs(initial_state)
        # self.visited_states.clear() # Optional: Clear after search if instance might be reused
        return result

    def solve_bfs(self, max_depth=300):
        """BFS implementation to find a solution."""
        def state_to_tuple(state):
            return tuple(tuple(branch) for branch in state)
        
        # Create a copy of the game to check for solution
        game_copy = deepcopy(self.game)
        
        # Start with initial state
        initial_state = deepcopy(self.game.jogo)
        
        # Queue holds (state, path_so_far)
        queue = deque([(initial_state, [])])
        
        # Track visited states
        visited = set()
        
        # Add initial state to visited
        visited.add(state_to_tuple(initial_state))
        
        while queue:
            current_state, path = queue.popleft()
            
            # Check if we've reached max depth
            if len(path) >= max_depth:
                continue
            
            # Check if this state is a solution
            game_copy.jogo = deepcopy(current_state)
            if game_copy.jogo_finalizado():
                return path
            
            # Try all possible moves from this state
            for orig in range(len(current_state)):
                for dest in range(len(current_state)):
                    if orig == dest:
                        continue
                    
                    # Set up game to check if move is valid
                    game_copy.jogo = deepcopy(current_state)
                    dir_orig = game_copy.ramo_direita(orig)
                    dir_dest = game_copy.ramo_direita(dest)
                    
                    # Check if move is valid
                    valid, quantidade = game_copy.movimento_valido(
                        current_state[orig], current_state[dest], 
                        dir_orig, dir_dest
                    )
                    
                    if valid:
                        # Apply the move
                        birds, new_orig = game_copy.extrair_passaros(
                            current_state[orig], dir_orig, quantidade
                        )
                        new_state = deepcopy(current_state)
                        new_state[orig] = new_orig
                        new_state[dest] = game_copy.inserir_passaros(
                            current_state[dest], birds, dir_dest
                        )
                        
                        # Check if new state has been visited
                        new_state_tuple = state_to_tuple(new_state)
                        if new_state_tuple not in visited:
                            # Mark as visited
                            visited.add(new_state_tuple)
                            
                            # Add to queue with updated path
                            new_path = path + [(orig + 1, dest + 1)]
                            queue.append((new_state, new_path))
                            
                            # Check if this new state is a solution
                            game_copy.jogo = deepcopy(new_state)
                            if game_copy.jogo_finalizado():
                                return new_path
        
        return None  # No solution found
    
    def solve_ucs(self, max_depth=500):
        """Uniform Cost Search implementation to find the optimal solution."""
        def state_to_tuple(state):
            return tuple(tuple(branch) for branch in state)
    
        game_copy = deepcopy(self.game) # For checking solution state
        initial_state = deepcopy(self.game.jogo)
        initial_state_tuple = state_to_tuple(initial_state)
        
        # Priority queue stores: (cost, path, state)
        pq = [(0, [], initial_state)]  
        
        # Visited stores the minimum cost found so far to reach a state
        # For UCS, we only need to know if visited, but storing cost helps 
        # if we wanted to potentially update paths (though standard UCS doesn't)
        visited = {initial_state_tuple: 0} 
    
        while pq:
            cost, path, current_state = heappop(pq)
            current_state_tuple = state_to_tuple(current_state)

            # Optimization: If we found a shorter path already, skip
            if cost > visited.get(current_state_tuple, float('inf')):
                continue
            
            # Check if the current state is a solution
            game_copy.jogo = deepcopy(current_state)
            if game_copy.jogo_finalizado():
                return path
                
            # Check max depth/cost
            if cost >= max_depth:
                continue

            # Explore neighbors
            for orig in range(len(current_state)):
                for dest in range(len(current_state)):
                    if orig == dest:
                        continue
    
                    # Use _try_move which handles copies appropriately
                    new_state, valid, _ = self._try_move(current_state, orig, dest)
                    
                    if valid:
                        new_state_tuple = state_to_tuple(new_state)
                        new_cost = cost + 1  # Uniform cost
                        
                        # Add to queue only if it's a new state or found via a cheaper path
                        if new_cost < visited.get(new_state_tuple, float('inf')):
                           visited[new_state_tuple] = new_cost
                           new_path = path + [(orig + 1, dest + 1)]
                           heappush(pq, (new_cost, new_path, new_state))
    
        return None  # No solution found

    def solve_astar(self, max_depth=500):
        """A* search implementation to find a solution."""
        def state_to_tuple(state):
            return tuple(tuple(branch) for branch in state)
        
        game_copy = deepcopy(self.game)
        initial_state = deepcopy(self.game.jogo)
        initial_state_tuple = state_to_tuple(initial_state)

        # Priority queue stores: (priority, cost, path, state)
        # priority = cost + heuristic
        # cost = len(path)
        pq = [(self._heuristic(initial_state), 0, [], initial_state)]
        
        # Visited stores the minimum cost found so far to reach a state
        visited = {initial_state_tuple: 0}
        
        while pq:
            priority, cost, path, current_state = heappop(pq)
            
            # Check if goal state
            game_copy.jogo = deepcopy(current_state)
            if game_copy.jogo_finalizado():
                return path
                
            # Check max depth
            if cost >= max_depth:
                continue
                
            # Check if we found a shorter path to this state already
            current_state_tuple = state_to_tuple(current_state)
            if cost > visited.get(current_state_tuple, float('inf')):
                 continue

            # Explore neighbors
            for orig in range(len(current_state)):
                for dest in range(len(current_state)):
                    if orig == dest:
                        continue

                    # Use game copy to simulate move
                    game_copy.jogo = deepcopy(current_state)
                    dir_orig = game_copy.ramo_direita(orig)
                    dir_dest = game_copy.ramo_direita(dest)

                    valid, quantidade = game_copy.movimento_valido(
                        current_state[orig], current_state[dest], dir_orig, dir_dest
                    )

                    if valid:
                        # Apply move
                        birds, new_orig = game_copy.extrair_passaros(
                            current_state[orig], dir_orig, quantidade
                        )
                        new_state = deepcopy(current_state)
                        new_state[orig] = new_orig
                        new_state[dest] = game_copy.inserir_passaros(
                            current_state[dest], birds, dir_dest
                        )
                        
                        new_state_tuple = state_to_tuple(new_state)
                        new_cost = cost + 1
                        
                        # Check if this state was visited with a higher cost
                        if new_cost < visited.get(new_state_tuple, float('inf')):
                            visited[new_state_tuple] = new_cost
                            heuristic_cost = self._heuristic(new_state)
                            new_priority = new_cost + heuristic_cost
                            new_path = path + [(orig + 1, dest + 1)]
                            heappush(pq, (new_priority, new_cost, new_path, new_state))
                            
        return None # No solution found
        
    def _heuristic(self, state):
        """Heuristic function for A*. Estimates moves needed."""
        # Heuristic: Count birds not in a completed/final branch.
        # A completed branch is full (4 birds) and has only one color.
        misplaced_birds = 0
        for branch in state:
            birds = [b for b in branch if b != ""]
            if not birds:
                continue # Empty branch is fine
            
            # Check if branch is completed (4 birds, same color)
            is_complete = (len(birds) == 4 and len(set(birds)) == 1)
            
            if not is_complete:
                # All birds in an incomplete branch are considered misplaced
                misplaced_birds += len(birds)
                
        # Simple estimate: each move can potentially place 1-3 birds correctly.
        # Dividing by a number (e.g., 2 or 3) might give a slightly more informed heuristic.
        # Let's start simple: just return the count.
        return misplaced_birds

    def _is_solved(self, state):
        """Check if game state is solved (used by heuristic/DFS)."""
        game_copy = deepcopy(self.game)
        game_copy.jogo = deepcopy(state)
        return game_copy.jogo_finalizado()

    def _try_move(self, state, orig, dest):
        """Try a move and return new state if valid."""
        # Create a fresh copy for move simulation
        game_copy = deepcopy(self.game)
        game_copy.jogo = deepcopy(state)

        dir_orig = game_copy.ramo_direita(orig)
        dir_dest = game_copy.ramo_direita(dest)

        valid, quantidade = game_copy.movimento_valido(
            game_copy.jogo[orig], game_copy.jogo[dest], # Use game_copy's state
            dir_orig, dir_dest
        )

        if valid:
            birds, new_orig = game_copy.extrair_passaros(
                game_copy.jogo[orig], dir_orig, quantidade # Use game_copy's state
            )
            # Apply move to the state that will be returned
            new_state = deepcopy(state)
            new_state[orig] = new_orig
            new_state[dest] = game_copy.inserir_passaros(
                new_state[dest], birds, dir_dest # Insert into the new_state copy
            )
            return new_state, True, birds

        return state, False, None # Return original state if move invalid

    def _evaluate_state(self, state):
        """Evaluate the state to prioritize better moves."""
        score = 0
        for branch in state:
            cores = [p for p in branch if p != ""]
            if len(cores) == 0:
                continue
            if len(set(cores)) == 1:  # All birds are of the same color
                score += len(cores) ** 2  # Encourage complete stacks
            else:
                consecutive = 1
                max_consecutive = 1
                for i in range(1, len(cores)):
                    if cores[i] == cores[i-1]:
                        consecutive += 1
                        max_consecutive = max(max_consecutive, consecutive)
                    else:
                        consecutive = 1
                score += max_consecutive ** 2  # Reward longer consecutive sequences

        return score

    def solve_iddfs(self, initial_max_depth=0, depth_increment=1, max_iterations=100):
        """Iterative Deepening Depth-First Search (IDDFS)."""
        def state_to_tuple(state):
            return tuple(tuple(branch) for branch in state)
            
        initial_state = deepcopy(self.game.jogo)
        depth_limit = initial_max_depth
        game_copy = deepcopy(self.game) # For checking solution state
        
        for iteration in range(max_iterations):
            print(f"IDDFS: Trying depth limit {depth_limit}...")
            visited_in_dls = set() # Visited set for the current depth-limited search
            solution = self._dls(initial_state, [], depth_limit, visited_in_dls, game_copy)
            if solution is not None:
                print(f"IDDFS: Solution found at depth {len(solution)}")
                return solution
            depth_limit += depth_increment
            
        print(f"IDDFS: No solution found within {max_iterations} iterations (max depth explored: {depth_limit - depth_increment})")
        return None

    def _dls(self, current_state, path, limit, visited_in_dls, game_copy):
        """Depth-Limited Search helper for IDDFS."""
        def state_to_tuple(state):
             return tuple(tuple(branch) for branch in state)
             
        current_depth = len(path)
        state_tuple = state_to_tuple(current_state)

        # Check if goal state
        game_copy.jogo = deepcopy(current_state)
        if game_copy.jogo_finalizado():
            return path
            
        # Check depth limit
        if current_depth >= limit:
            return None
            
        # Check if visited *in this specific DLS iteration* to prevent cycles
        if state_tuple in visited_in_dls:
            return None
        visited_in_dls.add(state_tuple)

        # Explore neighbors (similar logic to DFS/BFS/A* move generation)
        possible_moves = []
        for orig in range(len(current_state)):
            for dest in range(len(current_state)):
                if orig == dest:
                    continue

                # Use a temporary game copy to check validity without altering game_copy used for solution check
                temp_game = deepcopy(self.game) 
                temp_game.jogo = deepcopy(current_state)
                dir_orig = temp_game.ramo_direita(orig)
                dir_dest = temp_game.ramo_direita(dest)

                valid, quantidade = temp_game.movimento_valido(
                    current_state[orig], current_state[dest], dir_orig, dir_dest
                )

                if valid:
                    # Apply move to get new state
                    birds, new_orig = temp_game.extrair_passaros(
                        current_state[orig], dir_orig, quantidade
                    )
                    new_state = deepcopy(current_state)
                    new_state[orig] = new_orig
                    new_state[dest] = temp_game.inserir_passaros(
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
        """Greedy Best-First Search implementation."""
        def state_to_tuple(state):
            return tuple(tuple(branch) for branch in state)

        game_copy = deepcopy(self.game)
        initial_state = deepcopy(self.game.jogo)
        initial_state_tuple = state_to_tuple(initial_state)

        # Priority queue stores: (heuristic, path, state)
        pq = [(self._heuristic(initial_state), [], initial_state)]
        
        # Visited set to prevent cycles
        visited = {initial_state_tuple}
        path_len = 0
        
        while pq:
            heuristic, path, current_state = heappop(pq)
            path_len = len(path)
            
            # Check if goal state
            game_copy.jogo = deepcopy(current_state)
            if game_copy.jogo_finalizado():
                return path
                
            # Check max depth (using path length as proxy)
            if path_len >= max_depth:
                continue

            # Explore neighbors
            for orig in range(len(current_state)):
                for dest in range(len(current_state)):
                    if orig == dest:
                        continue

                    new_state, valid, _ = self._try_move(current_state, orig, dest)

                    if valid:
                        new_state_tuple = state_to_tuple(new_state)
                        
                        if new_state_tuple not in visited:
                            visited.add(new_state_tuple)
                            new_heuristic = self._heuristic(new_state)
                            new_path = path + [(orig + 1, dest + 1)]
                            heappush(pq, (new_heuristic, new_path, new_state))
                            
        return None # No solution found
        
    def solve_weighted_astar(self, weight=1.5, max_depth=500):
        """Weighted A* search implementation."""
        def state_to_tuple(state):
            return tuple(tuple(branch) for branch in state)
        
        game_copy = deepcopy(self.game)
        initial_state = deepcopy(self.game.jogo)
        initial_state_tuple = state_to_tuple(initial_state)

        # Priority queue stores: (priority, cost, path, state)
        # priority = cost + weight * heuristic
        initial_heuristic = self._heuristic(initial_state)
        pq = [(weight * initial_heuristic, 0, [], initial_state)] # Initial priority uses 0 cost
        
        # Visited stores the minimum cost found so far to reach a state
        visited = {initial_state_tuple: 0}
        
        while pq:
            _, cost, path, current_state = heappop(pq) # Priority not needed after popping
            
            # Check if goal state
            game_copy.jogo = deepcopy(current_state)
            if game_copy.jogo_finalizado():
                return path
                
            # Check max depth
            if cost >= max_depth:
                continue
                
            # Check if we found a shorter path to this state already
            current_state_tuple = state_to_tuple(current_state)
            if cost > visited.get(current_state_tuple, float('inf')):
                 continue

            # Explore neighbors
            for orig in range(len(current_state)):
                for dest in range(len(current_state)):
                    if orig == dest:
                        continue

                    new_state, valid, _ = self._try_move(current_state, orig, dest)

                    if valid:
                        new_state_tuple = state_to_tuple(new_state)
                        new_cost = cost + 1
                        
                        # Check if this state was visited with a higher cost
                        if new_cost < visited.get(new_state_tuple, float('inf')):
                            visited[new_state_tuple] = new_cost
                            heuristic_cost = self._heuristic(new_state)
                            # Weighted priority calculation
                            new_priority = new_cost + weight * heuristic_cost 
                            new_path = path + [(orig + 1, dest + 1)]
                            heappush(pq, (new_priority, new_cost, new_path, new_state))
                            
        return None # No solution found
