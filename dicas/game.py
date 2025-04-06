import random
import os

EMOJIS = {
    "1": "🔴", "2": "🟠", "3": "🟡", "4": "🟢", "5": "🔵",
    "6": "🟣", "7": "⚫️", "8": "⚪️", "9": "🟤", "10": "🧿",
    "": "▪️ "
}

# Função para embaralhar os pássaros
def gerar_estado_inicial(n_ramos):
    n_cores = n_ramos - 2
    cores = [str(i+1) for i in range(n_cores) for _ in range(4)]
    random.shuffle(cores)

    ramos = [["" for _ in range(4)] for _ in range(n_ramos)]
    idx = 0
    for i in range(n_ramos):
        if i >= n_ramos - 2:
            continue  # últimos dois ficam vazios
        for j in range(4):
            ramos[i][j] = cores[idx]
            idx += 1
    return ramos

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para printar o jogo com emojis e alinhamento visual
def printar_jogo(jogo):
    limpar_tela()
    total_ramos = len(jogo)
    # Ajuste para dividir corretamente os ramos entre esquerda e direita
    metade = (total_ramos + 1) // 2  # Arredonda para cima para a esquerda ter mais ramos se ímpar
    esquerda = jogo[:metade]  # Ramos da esquerda
    direita = jogo[metade:]   # Ramos da direita

    # Número de linhas é baseado no lado com mais ramos
    linhas = max(len(esquerda), len(direita))
    print()
    for i in range(linhas):
        # Ramo da esquerda
        if i < len(esquerda):
            ramo_esq = esquerda[i]
            num_esq = f"{i+1:>2} |"
            emj_esq = ''.join(f" {EMOJIS[c]}" for c in ramo_esq)
        else:
            num_esq = "   |"
            emj_esq = " 🪹 🪹 🪹 🪹 "

        # Ramo da direita (só exibe se houver ramo correspondente)
        if i < len(direita):
            ramo_dir = direita[i]
            num_dir = f"| {metade+i+1:<2}"
            emj_dir = ''.join(f" {EMOJIS[c]}" for c in ramo_dir)
        else:
            num_dir = ""
            emj_dir = ""

        # Se não houver ramo à direita, não exibe o número da direita
        if emj_dir:
            print(f"{num_esq}{emj_esq}      {emj_dir} {num_dir}")
        else:
            print(f"{num_esq}{emj_esq}")

def ramo_direita(indice, total):
    metade = (total + 1) // 2
    return indice >= metade

# Função para extrair pássaros a mover do ramo
def extrair_passaros(ramo, direita, quantidade):
    if direita:
        lado = 0
        while lado < 4 and ramo[lado] == "":
            lado += 1
        if lado == 4:
            return [], ramo
        cor = ramo[lado]
        # Extrai apenas a quantidade especificada ou o número de pássaros consecutivos da mesma cor
        count = 1
        while lado + count < 4 and ramo[lado + count] == cor:
            count += 1
        count = min(count, quantidade)  # Limita ao número que será transferido
        novos = ramo[:]
        for i in range(count):
            novos[lado + i] = ""
        return [cor] * count, novos
    else:
        lado = 3
        while lado >= 0 and ramo[lado] == "":
            lado -= 1
        if lado == -1:
            return [], ramo
        cor = ramo[lado]
        count = 1
        while lado - count >= 0 and ramo[lado - count] == cor:
            count += 1
        count = min(count, quantidade)  # Limita ao número que será transferido
        novos = ramo[:]
        for i in range(count):
            novos[lado - i] = ""
        return [cor] * count, novos

# Função para inserir pássaros no ramo de destino
def inserir_passaros(ramo, passaros, direita):
    novos = ramo[:]
    if direita:
        lado = 3
        while lado >= 0 and novos[lado] != "":
            lado -= 1
        for i in range(len(passaros)):
            if lado - i < 0:
                break
            novos[lado - i] = passaros[-(i+1)]
    else:
        lado = 0
        while lado < 4 and novos[lado] != "":
            lado += 1
        for i in range(len(passaros)):
            if lado + i > 3:
                break
            novos[lado + i] = passaros[i]
    return novos

# Verifica se pode mover de origem pra destino
def movimento_valido(origem, destino, dir_orig, dir_dest):
    # Verificar se origem está vazia
    if all(p == "" for p in origem):
        return False, 0

    passaros, _ = extrair_passaros(origem, dir_orig, 4)  # Extrai o máximo possível para verificar a cor
    if not passaros:
        return False, 0

    cor = passaros[0]
    # Verifica se destino é compatível
    if all(p == "" for p in destino):
        espaco = 4
    else:
        topo = None
        if dir_dest:
            for p in destino:
                if p != "":
                    topo = p
                    break
        else:
            for p in reversed(destino):
                if p != "":
                    topo = p
                    break
        if topo != cor:
            return False, 0
        espaco = destino.count("")

    # Se há pelo menos 1 espaço e a cor é compatível, o movimento é válido
    if espaco > 0:
        # Calcula quantos pássaros podem ser transferidos
        quantidade = min(len(passaros), espaco)
        return True, quantidade
    return False, 0

# Verifica se jogo terminou
def jogo_finalizado(jogo):
    for ramo in jogo:
        cores = set(p for p in ramo if p != "")
        if len(cores) > 1:
            return False
        if ramo.count("") not in [0, 4]:
            return False
    return True

# Função principal do jogo
def jogar():
    while True:
        try:
            n = int(input("Quantos ramos deseja (4 a 12)? "))
            if 4 <= n <= 12:
                break
        except:
            pass
        print("Entrada inválida!")

    jogo = gerar_estado_inicial(n)

    while True:
        printar_jogo(jogo)

        if jogo_finalizado(jogo):
            print("\n🎉 Parabéns! Você finalizou o jogo! 🎉")
            break

        try:
            mov = input("Digite o movimento (origem destino) ou 'sair': ")
            if mov.lower() == 'sair':
                break
            orig, dest = map(int, mov.strip().split())
            if orig < 1 or dest < 1 or orig > n or dest > n or orig == dest:
                raise ValueError
        except:
            print("Movimento inválido. Tente novamente.")
            input("Pressione Enter para continuar...")
            continue

        dir_orig = ramo_direita(orig-1, n)
        dir_dest = ramo_direita(dest-1, n)

        valido, quantidade = movimento_valido(jogo[orig-1], jogo[dest-1], dir_orig, dir_dest)
        if not valido:
            print("Movimento não permitido.")
            input("Pressione Enter para continuar...")
            continue

        passaros, novo_origem = extrair_passaros(jogo[orig-1], dir_orig, quantidade)
        jogo[orig-1] = novo_origem
        jogo[dest-1] = inserir_passaros(jogo[dest-1], passaros, dir_dest)

if __name__ == "__main__":
    jogar()