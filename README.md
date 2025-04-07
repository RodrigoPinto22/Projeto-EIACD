# Projeto-EIACD

## Sobre o Projeto
Bird Sort Puzzle é um jogo de puzzle onde o objetivo é organizar pássaros coloridos em ramos, agrupando-os por cores. O projeto implementa tanto um modo de jogo manual como vários algoritmos de pesquisa para resolução automática.

## Como Executar
Para executar o projeto, execute o seguinte comando no terminal: python3 main.py

### Escolher um dos seguintes Modos de Jogo
1. **Modo Manual**: Jogar manualmente
2. **Jogar com dicas** (hint e undo)
3. **Modo Automático**: Resolvido por um algoritmo

### Tamanho do Tabuleiro
- Pode escolher entre diferentes tamanhos (4 a 12 ramos)

## Instruções do Jogo Manual
### Objetivo
- Agrupar todos os pássaros da mesma cor no mesmo ramo
- Cada ramo pode ter no máximo 4 pássaros

### Como Jogar
1. Digite o número do ramo de origem
2. Digite o número do ramo de destino
3. O jogo irá mover automaticamente o máximo de pássaros possível

### Regras de Movimento
- Só é possível mover pássaros da mesma cor
- Movimentos seguem direções específicas:
  - **Ramos da Esquerda**:
    - Extração: direita → esquerda
    - Inserção: esquerda → direita
  - **Ramos da Direita**:
    - Extração: esquerda → direita
    - Inserção: direita → esquerda

## Modo Automático
### Algoritmos Disponíveis
1. **BFS** (Breadth-First Search)
   - Encontra a solução mais curta
   - Mais lento em puzzles grandes

2. **DFS** (Depth-First Search)
   - Rápido em encontrar uma solução
   - Pode não ser a solução mais curta

3. **IDDFS** (Iterative Deepening DFS)
   - Combina eficiência do DFS com otimalidade do BFS
   - Bom equilíbrio entre memória e qualidade

4. **UCS** (Uniform Cost Search)
   - Similar ao BFS neste puzzle
   - Todos os movimentos têm custo igual

5. **Greedy BFS**
   - Muito rápido
   - Soluções podem ser subótimas

6. **A***
   - Equilibra velocidade e qualidade
   - Usa heurísticas inteligentes

7. **Weighted A*** (W=1.5)
   - Mais rápido que A*
   - Sacrifica um pouco da qualidade

## Condições de Vitória
- Todos os pássaros da mesma cor agrupados no mesmo ramo
- Ramos devem estar ou completamente cheios (4 pássaros) ou vazios

## Modificações Possíveis
1. Alterar tamanho do puzzle (4-12 ramos)
2. Escolher diferentes algoritmos de resolução
3. Ajustar parâmetros dos algoritmos (ex: peso do Weighted A*)

## Análise de Desempenho (benchmark.py)
O projeto inclui uma ferramenta de análise de desempenho que permite comparar a eficiência dos diferentes algoritmos:

### Como Executar
Para executar o projeto executar o seguinte comando no terminal: python3 benchmark.py


### Funcionalidades
- Executa cada algoritmo múltiplas vezes para diferentes tamanhos de puzzle
- Mede e regista:
  - Tempo médio de execução
  - Desvio padrão do tempo
  - Número médio de movimentos
  - Desvio padrão dos movimentos
  - Taxa de sucesso

### Configurações Predefinidas
- Tamanhos de puzzle testados: 4, 6 e 8 ramos
- 3 tentativas por algoritmo
- Tempos limite:
  - Tamanho 4: 10 segundos
  - Tamanho 6: 20 segundos
  - Tamanho 8: 30 segundos

### Resultados
- Os resultados são guardados na pasta `benchmark_results`
- Cada ficheiro de resultados inclui:
  - Data e hora da execução
  - Configurações utilizadas
  - Resultados detalhados para cada tamanho
- Nome do ficheiro: `benchmark_AAAAMMDD_HHMMSS.txt`

## Estrutura do Projeto
```
.
├── main.py          # Ponto de entrada do programa
├── game.py          # Implementação do jogo
├── solver.py        # Algoritmos de resolução não informados
└── uninformed.py    # Algoritmos de resolução informados
└── benchmark.py     # Script de benchmark (opcional)
└── benchmark.txt    # Resultados do benchmark.py
```
