from game import Game


def main():
    while True:
        try:
            n = int(input("Quantos ramos deseja (4 a 12)? "))
            if 4 <= n <= 12:
                break
        except ValueError:
            pass
        print("Entrada inválida! Por favor, insira um número entre 4 e 12.")

    jogo = Game(n)

    while True:
        jogo.printar_jogo()

        if jogo.jogo_finalizado():
            print("\n🎉 Parabéns! Você finalizou o jogo! 🎉")
            break

        try:
            mov = input("Digite o movimento (origem destino) ou 'sair': ")
            if mov.lower() == 'sair':
                break
            # Ensure the input is two integers separated by a space
            orig, dest = map(int, mov.strip().split())
            if orig < 1 or orig > n or dest < 1 or dest > n:
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
            print("Movimento inválido. Tente novamente.")
            input("Pressione Enter para continuar...")
        except IndexError:
            print("Movimento inválido. Tente novamente.")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
