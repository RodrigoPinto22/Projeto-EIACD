from collections import deque
import heapq
import copy
from game import ramo_direita, movimento_valido, extrair_passaros, inserir_passaros, jogo_finalizado

def gerar_sucessores_estado(jogo):
    n = len(jogo)
    sucessores = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dir_i = ramo_direita(i, n)
            dir_j = ramo_direita(j, n)
            valido, qtd = movimento_valido(jogo[i], jogo[j], dir_i, dir_j)
            if valido:
                novo_jogo = copy.deepcopy(jogo)
                passaros, novo_jogo[i] = extrair_passaros(novo_jogo[i], dir_i, qtd)
                novo_jogo[j] = inserir_passaros(novo_jogo[j], passaros, dir_j)
                sucessores.append((novo_jogo, (i+1, j+1)))
    return sucessores

def bfs(jogo_inicial):
    fila = deque()
    fila.append((jogo_inicial, []))
    visitados = set()

    while fila:
        jogo, caminho = fila.popleft()
        estado = str(jogo)
        if estado in visitados:
            continue
        visitados.add(estado)

        if jogo_finalizado(jogo):
            return caminho

        for novo, mov in gerar_sucessores_estado(jogo):
            fila.append((novo, caminho + [mov]))
    return None

def dfs(jogo_inicial, limite=float('inf')):
    pilha = [(jogo_inicial, [], 0)]
    visitados = set()

    while pilha:
        jogo, caminho, profundidade = pilha.pop()
        estado = str(jogo)
        if estado in visitados or profundidade > limite:
            continue
        visitados.add(estado)

        if jogo_finalizado(jogo):
            return caminho

        for novo, mov in reversed(gerar_sucessores_estado(jogo)):
            pilha.append((novo, caminho + [mov], profundidade + 1))
    return None

def uniform_cost(jogo_inicial):
    fila = [(0, jogo_inicial, [])]
    visitados = set()

    while fila:
        custo, jogo, caminho = heapq.heappop(fila)
        estado = str(jogo)
        if estado in visitados:
            continue
        visitados.add(estado)

        if jogo_finalizado(jogo):
            return caminho

        for novo, mov in gerar_sucessores_estado(jogo):
            heapq.heappush(fila, (custo + 1, novo, caminho + [mov]))
    return None

def dls(jogo_inicial, limite):
    return dfs(jogo_inicial, limite=limite)

def ids(jogo_inicial, max_prof=20):
    for profundidade in range(max_prof):
        resultado = dls(jogo_inicial, limite=profundidade)
        if resultado is not None:
            return resultado
    return None
