from copy import deepcopy
from heapq import heappush, heappop

class GameSolver:
    def __init__(self, game):
        self.game = game
        self.visited_states = set()

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

            if self._is_solved(game_state):
                return []

            possible_moves = []
            for orig in range(len(game_state)):
                for dest in range(len(game_state)):
                    if orig != dest:
                        new_state, valid, birds_moved = self._try_move(game_state, orig, dest)
                        if valid:
                            score = self._evaluate_state(new_state)
                            possible_moves.append((score, orig, dest, new_state))

            # Prioritize moves with higher scores (more aligned birds)
            possible_moves.sort(reverse=True, key=lambda x: x[0])

            for _, orig, dest, new_state in possible_moves:
                solution = dfs(new_state, depth + 1)
                if solution is not None:
                    return [(orig + 1, dest + 1)] + solution

            self.visited_states.remove(state_tuple)
            return None

        self.visited_states.clear()
        initial_state = deepcopy(self.game.jogo)
        return dfs(initial_state)

    def _is_solved(self, state):
        """Check if game state is solved."""
        return all(
            all(b == branch[0] or b == "" for b in branch)
            for branch in state if any(b != "" for b in branch)
        )

    def _try_move(self, state, orig, dest):
        """Try a move and return new state if valid."""
        game_copy = deepcopy(self.game)
        game_copy.jogo = deepcopy(state)

        dir_orig = game_copy.ramo_direita(orig)
        dir_dest = game_copy.ramo_direita(dest)

        valid, quantidade = game_copy.movimento_valido(
            state[orig], state[dest],
            dir_orig, dir_dest
        )

        if valid:
            birds, new_orig = game_copy.extrair_passaros(
                state[orig], dir_orig, quantidade
            )
            new_state = deepcopy(state)
            new_state[orig] = new_orig
            new_state[dest] = game_copy.inserir_passaros(
                state[dest], birds, dir_dest
            )
            return new_state, True, birds

        return state, False, None

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
