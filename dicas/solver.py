import copy
import heapq
from game import movimento_valido, extrair_passaros, inserir_passaros, ramo_direita, jogo_finalizado

def heuristica_passaros_fora_do_lugar(jogo):
    contagem = {}
    for i, ramo in enumerate(jogo):
        for p in ramo:
            if p != "":
                contagem.setdefault(p, {}).setdefault(i, 0)
                contagem[p][i] += 1

    ramos_ideais = {cor: max(ramos, key=ramos.get) for cor, ramos in contagem.items()}
    fora_do_lugar = 0

    for i, ramo in enumerate(jogo):
        for p in ramo:
            if p != "" and ramos_ideais.get(p) != i:
                fora_do_lugar += 1

    return fora_do_lugar

class Node:
    def __init__(self, jogo, caminho=[], custo=0, heuristica=0):
        self.jogo = jogo
        self.caminho = caminho
        self.custo = custo
        self.heuristica = heuristica

    def __lt__(self, other):
        return (self.custo + self.heuristica) < (other.custo + other.heuristica)

def gerar_sucessores(node):
    sucessores = []
    n = len(node.jogo)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dir_i = ramo_direita(i, n)
            dir_j = ramo_direita(j, n)
            valido, qtd = movimento_valido(node.jogo[i], node.jogo[j], dir_i, dir_j)
            if valido:
                jogo_novo = copy.deepcopy(node.jogo)
                passaros, jogo_novo[i] = extrair_passaros(jogo_novo[i], dir_i, qtd)
                jogo_novo[j] = inserir_passaros(jogo_novo[j], passaros, dir_j)
                novo_caminho = node.caminho + [(i+1, j+1)]
                sucessores.append((jogo_novo, novo_caminho))
    return sucessores

def resolver(jogo_inicial, metodo='astar'):
    h_inicial = heuristica_passaros_fora_do_lugar(jogo_inicial)
    inicial = Node(jogo_inicial, [], 0, h_inicial)
    fronteira = [inicial]
    visitados = set()

    while fronteira:
        atual = heapq.heappop(fronteira)
        estado_serial = str(atual.jogo)
        if estado_serial in visitados:
            continue
        visitados.add(estado_serial)

        if jogo_finalizado(atual.jogo):
            return atual.caminho

        for novo_jogo, caminho in gerar_sucessores(atual):
            h = heuristica_passaros_fora_do_lugar(novo_jogo)
            custo = atual.custo + 1
            heur = h if metodo == 'astar' else h - custo
            heapq.heappush(fronteira, Node(novo_jogo, caminho, custo, heur))

    return None

def weighted_a_star(jogo_inicial, w=1.5):
    h_inicial = heuristica_passaros_fora_do_lugar(jogo_inicial)
    inicial = Node(jogo_inicial, [], 0, h_inicial)
    fronteira = [inicial]
    visitados = set()

    while fronteira:
        atual = heapq.heappop(fronteira)
        estado_serial = str(atual.jogo)
        if estado_serial in visitados:
            continue
        visitados.add(estado_serial)

        if jogo_finalizado(atual.jogo):
            return atual.caminho

        for novo_jogo, caminho in gerar_sucessores(atual):
            h = heuristica_passaros_fora_do_lugar(novo_jogo)
            custo = atual.custo + 1
            heur = w * h
            heapq.heappush(fronteira, Node(novo_jogo, caminho, custo, heur))
    return None
