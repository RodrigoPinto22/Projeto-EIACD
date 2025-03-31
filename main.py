from game import Game
from algorithms import GameSolver
import time

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
    print("\nProcurando solução usando DFS...")
    solver = GameSolver(jogo)
    solution = solver.solve_dfs()
    
    if solution:
        print("\nSolução encontrada! Mostrando passo a passo:")
        input("Pressione Enter para começar...")
        
        # Show initial state
        print("\nEstado Inicial:")
        jogo.printar_jogo()
        time.sleep(1)
        
        # Execute and show each move
        for i, (orig, dest) in enumerate(solution, 1):
            print(f"\nPasso {i}: Mover do ramo {orig} para o ramo {dest}")
            
            dir_orig = jogo.ramo_direita(orig - 1)
            dir_dest = jogo.ramo_direita(dest - 1)
            
            _, quantidade = jogo.movimento_valido(
                jogo.jogo[orig - 1], jogo.jogo[dest - 1], dir_orig, dir_dest
            )
            
            passaros, novo_origem = jogo.extrair_passaros(
                jogo.jogo[orig - 1], dir_orig, quantidade
            )
            jogo.jogo[orig - 1] = novo_origem
            jogo.jogo[dest - 1] = jogo.inserir_passaros(
                jogo.jogo[dest - 1], passaros, dir_dest
            )
            
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
