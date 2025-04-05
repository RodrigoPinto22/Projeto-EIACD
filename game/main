from game import Game
from algorithms import GameSolver
import time
from copy import deepcopy

def play_human_mode(jogo):
    """Handle human player game mode"""
    while True:
        jogo.printar_jogo()

        if jogo.jogo_finalizado():
            print("\n🎉 Parabéns! Você finalizou o jogo! 🎉")
            break

        try:
            mov = input("Digite o movimento (origem destino) ou 'sair': ")
            if mov.lower() == 'sair':
                break
            orig, dest = map(int, mov.strip().split())
            if orig < 1 or orig > jogo.size or dest < 1 or dest > jogo.size:
                raise ValueError("Os números devem estar entre 1 e o número de ramos.")

            dir_orig = jogo.ramo_direita(orig - 1)
            dir_dest = jogo.ramo_direita(dest - 1)

            valido, quantidade = jogo.movimento_valido(
                jogo.jogo[orig - 1], jogo.jogo[dest - 1], dir_orig, dir_dest
            )
            if not valido:
                print("Movimento não permitido.")
                input("Pressione Enter para continuar...")
                continue

            passaros, novo_origem = jogo.extrair_passaros(
                jogo.jogo[orig - 1], dir_orig, quantidade
            )
            jogo.jogo[orig - 1] = novo_origem
            jogo.jogo[dest - 1] = jogo.inserir_passaros(
                jogo.jogo[dest - 1], passaros, dir_dest
            )

        except ValueError as e:
            print(f"Erro: {e}")
            input("Pressione Enter para continuar...")
        except IndexError:
            print("Movimento inválido. Tente novamente.")
            input("Pressione Enter para continuar...")

def play_algorithm_mode(jogo):
    """Handle algorithm solver mode"""
    while True:
        try:
            print("Escolha o algoritmo:")
            print("  1 - BFS")
            print("  2 - DFS")
            print("  3 - IDDFS (Iterative Deepening)")
            print("  4 - UCS (Uniform Cost Search)")
            print("  5 - Greedy BFS")
            print("  6 - A*")
            print("  7 - Weighted A* (W=1.5)")
            algo_choice = int(input("Opção: "))
            # Adjust range check for 1-based indexing
            if 1 <= algo_choice <= 7:
                break
        except ValueError:
            pass
        print("Entrada inválida! Por favor, digite um número entre 1 e 7.")
    
    # Instantiate the solver *before* accessing its methods
    solver = GameSolver(jogo)
    
    algo_name = ""
    solver_method = None # Initialize solver_method
    # Map choice to algorithm name and solver method
    if algo_choice == 1:
        algo_name = "BFS"
        solver_method = solver.solve_bfs
    elif algo_choice == 2:
        algo_name = "DFS"
        solver_method = solver.solve_dfs
    elif algo_choice == 3:
        algo_name = "IDDFS"
        solver_method = solver.solve_iddfs
    elif algo_choice == 4:
        algo_name = "UCS"
        solver_method = solver.solve_ucs
    elif algo_choice == 5:
        algo_name = "Greedy BFS"
        solver_method = solver.solve_greedy_bfs
    elif algo_choice == 6:
        algo_name = "A*"
        solver_method = solver.solve_astar
    else: # algo_choice == 7
        algo_name = "Weighted A*"
        # Use a lambda to pass the weight argument
        solver_method = lambda: solver.solve_weighted_astar(weight=1.5)
        
    print(f"\nProcurando solução usando {algo_name}...")
    
    solution = None
    start_time = time.time()
    
    # Call the selected solver method
    if solver_method:
        solution = solver_method()
    else:
        print("Erro: Método de solução não definido.") # Should not happen
        
    end_time = time.time()
    
    print(f"Tempo de busca: {end_time - start_time:.4f} segundos")

    if solution:
        print(f"\nSolução encontrada com {len(solution)} passos! Mostrando passo a passo:")
        input("Pressione Enter para começar...")
        
        # Show initial state
        print("\nEstado Inicial:")
        jogo.printar_jogo()
        time.sleep(1)
        
        # Execute and show each move
        for i, (orig, dest) in enumerate(solution, 1):
            print(f"\nPasso {i}: Mover do ramo {orig} para o ramo {dest}")
            
            # Create a temporary copy to apply the move without changing the original solver state
            temp_game = deepcopy(jogo)
            temp_game.jogo = deepcopy(jogo.jogo) # Ensure jogo state is also copied
            
            dir_orig = temp_game.ramo_direita(orig - 1)
            dir_dest = temp_game.ramo_direita(dest - 1)
            
            valido, quantidade = temp_game.movimento_valido(
                temp_game.jogo[orig - 1], temp_game.jogo[dest - 1], dir_orig, dir_dest
            )
            
            # Apply move to the main game instance (jogo) for display
            if valido:
                passaros, novo_origem = jogo.extrair_passaros(
                    jogo.jogo[orig - 1], dir_orig, quantidade
                )
                jogo.jogo[orig - 1] = novo_origem
                jogo.jogo[dest - 1] = jogo.inserir_passaros(
                    jogo.jogo[dest - 1], passaros, dir_dest
                )
            else:
                print(f"Erro: Movimento inválido encontrado na solução {orig}->{dest}. Abortando.")
                break # Should not happen if solver is correct
            
            jogo.printar_jogo()
            time.sleep(1)  # Pause between moves
            input("Pressione Enter para o próximo movimento...")
        
        print("\n🎉 Solução completa! 🎉")
    else:
        print("\nNão foi possível encontrar uma solução.")

def main():
    while True:
        try:
            n = int(input("Quantos ramos deseja (4 a 12)? "))
            if 4 <= n <= 12:
                break
        except ValueError:
            pass
        print("Entrada inválida! Por favor, insira um número entre 4 e 12.")

    while True:
        try:
            mode = int(input("Escolha o modo (0 - Jogar, 1 - Resolver automático): "))
            if mode in [0, 1]:
                break
        except ValueError:
            pass
        print("Entrada inválida! Por favor, digite 0 ou 1.")

    jogo = Game(n)
    
    if mode == 0:
        play_human_mode(jogo)
    else:
        play_algorithm_mode(jogo)

if __name__ == "__main__":
    main()
