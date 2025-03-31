import random
import os

EMOJIS = {
    "1": "🔴", "2": "🟠", "3": "🟡", "4": "🟢", "5": "🔵",
    "6": "🟣", "7": "⚫️", "8": "⚪️", "9": "🟤", "10": "🧿",
    "": "  "
}


class Game:
    def __init__(self, size):
        self.size = size
        self.jogo = self.gerar_estado_inicial(size)

    def gerar_estado_inicial(self, n_ramos):
        n_cores = n_ramos - 2
        cores = [str(i + 1) for i in range(n_cores) for _ in range(4)]
        random.shuffle(cores)

        ramos = [["" for _ in range(4)] for _ in range(n_ramos)]
        idx = 0
        for i in range(n_ramos):
            if i >= n_ramos - 2: 
                continue
            for j in range(4):
                ramos[i][j] = cores[idx]
                idx += 1
        return ramos

    def limpar_tela(self):
        try:
            if os.name == 'nt':  
                os.system('cls')
            else:  
                os.system('clear')
        except OSError:
            print("\n" * 30) 

    def printar_jogo(self):
        self.limpar_tela()
        total_ramos = len(self.jogo)
        metade = (total_ramos + 1) // 2
        esquerda = self.jogo[:metade]
        direita = self.jogo[metade:]

        linhas = max(len(esquerda), len(direita))
        print()
        for i in range(linhas):
            if i < len(esquerda):
                ramo_esq = esquerda[i]
                num_esq = f"{i + 1:>2} |"
                emj_esq = ''.join(f" {EMOJIS[c]}" for c in ramo_esq)
            else:
                num_esq = "   |"
                emj_esq = " 🪹 🪹 🪹 🪹 "

            if i < len(direita):
                ramo_dir = direita[i]
                num_dir = f"| {metade + i + 1:<2}"
                emj_dir = ''.join(f" {EMOJIS[c]}" for c in ramo_dir)
            else:
                num_dir = ""
                emj_dir = ""

            if emj_dir:
                print(f"{num_esq}{emj_esq}      {emj_dir} {num_dir}")
            else:
                print(f"{num_esq}{emj_esq}")

    def ramo_direita(self, indice):
        metade = (self.size + 1) // 2
        return indice >= metade

    def movimento_valido(self, origem, destino, dir_orig, dir_dest):
        if all(p == "" for p in origem):
            return False, 0

        passaros, _ = self.extrair_passaros(origem, dir_orig, 4)
        if not passaros:
            return False, 0

        cor = passaros[0]

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

        if espaco > 0:
            quantidade = min(len(passaros), espaco)
            return True, quantidade
        return False, 0

    def extrair_passaros(self, ramo, direita, quantidade):
        novos = ramo[:]
        passaros = []

        if direita:
            lado = 0
            while lado < 4 and ramo[lado] == "":
                lado += 1
            if lado == 4:
                return [], ramo

            cor = ramo[lado]
            count = 1
            while lado + count < 4 and ramo[lado + count] == cor:
                count += 1
            count = min(count, quantidade)
            passaros = [cor] * count
            for i in range(count):
                novos[lado + i] = ""
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
            count = min(count, quantidade)
            passaros = [cor] * count
            for i in range(count):
                novos[lado - i] = ""

        return passaros, novos

    def inserir_passaros(self, ramo, passaros, direita):
        novos = ramo[:]

        if direita:
            lado = 3
            while lado >= 0 and novos[lado] != "":
                lado -= 1
            for p in reversed(passaros):
                if lado < 0:
                    break
                novos[lado] = p
                lado -= 1
        else:
            lado = 0
            while lado < 4 and novos[lado] != "":
                lado += 1
            for p in passaros:
                if lado >= 4:
                    break
                novos[lado] = p
                lado += 1

        return novos

    def jogo_finalizado(self):
        for ramo in self.jogo:
            cores = set(p for p in ramo if p != "")
            if len(cores) > 1 or ramo.count("") not in [0, 4]:
                return False
        return True
