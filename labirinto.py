import heapq
from collections import deque

labirinto = [
    "I..............",
    ".##.###.####.#.",
    ".##.###.#....#.",
    ".##...#.####.#.",
    ".####.#.#....#.",
    ".####.#.#.####.",
    ".####.#.#....#.",
    ".##...#.####.##",
    ".##.###.#....##",
    ".#..###.#.#####",
    ".#..###.#....##",
    ".#....#.####.##",
    ".####.#.#....##",
    ".####.###.#####",
    ".......F..#####",
]

DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def achar(lab, simbolo):
    for i, linha in enumerate(lab):
        if simbolo in linha:
            return (i, linha.index(simbolo))


def livre(lab, i, j):
    dentro = 0 <= i < len(lab) and 0 <= j < len(lab[0])
    return dentro and lab[i][j] != '#'


def montar_grafo(lab):
    grafo = {}
    for i in range(len(lab)):
        for j in range(len(lab[0])):
            if not livre(lab, i, j):
                continue
            grafo[(i, j)] = []
            for di, dj in DIRECOES:
                if livre(lab, i + di, j + dj):
                    grafo[(i, j)].append((i + di, j + dj))
    return grafo


def desenhar(lab, caminho):
    grade = [list(linha) for linha in lab]
    for i, j in caminho:
        if grade[i][j] == '.':
            grade[i][j] = '*'
    for linha in grade:
        print(''.join(linha))


def desenhar_exploracao(lab, caminho, visitadas):
    grade = [list(linha) for linha in lab]
    for i, j in visitadas:
        if grade[i][j] == '.':
            grade[i][j] = 'o'
    for i, j in caminho:
        if grade[i][j] in '.o':
            grade[i][j] = '*'
    for linha in grade:
        print(''.join(linha))


def reconstruir(veio_de, saida):
    if saida not in veio_de:
        return []
    caminho = [saida]
    while veio_de[caminho[-1]] is not None:
        caminho.append(veio_de[caminho[-1]])
    return caminho[::-1]


def dfs(grafo, inicio, saida):
    veio_de = {inicio: None}
    visitadas = []

    def descer(v):
        visitadas.append(v)
        if v == saida:
            return True
        for w in grafo[v]:
            if w not in veio_de:
                veio_de[w] = v
                if descer(w):
                    return True
        return False

    descer(inicio)
    return reconstruir(veio_de, saida), visitadas


def bfs(grafo, inicio, saida):
    veio_de = {inicio: None}
    fila = deque([inicio])
    visitadas = []

    while fila:
        v = fila.popleft()
        visitadas.append(v)
        if v == saida:
            break
        for w in grafo[v]:
            if w not in veio_de:
                veio_de[w] = v
                fila.append(w)

    return reconstruir(veio_de, saida), visitadas


def h(v, saida):
    return abs(v[0] - saida[0]) + abs(v[1] - saida[1])


def gulosa(grafo, inicio, saida):
    veio_de = {inicio: None}
    ordem_de_entrada = 0
    fronteira = [(h(inicio, saida), ordem_de_entrada, inicio)]
    visitadas = []

    while fronteira:
        _, _, v = heapq.heappop(fronteira)
        visitadas.append(v)
        if v == saida:
            break
        for w in grafo[v]:
            if w not in veio_de:
                veio_de[w] = v
                ordem_de_entrada += 1
                heapq.heappush(fronteira, (h(w, saida), ordem_de_entrada, w))

    return reconstruir(veio_de, saida), visitadas


if __name__ == "__main__":
    grafo = montar_grafo(labirinto)
    inicio = achar(labirinto, 'I')
    saida = achar(labirinto, 'F')

    tabela = []
    for nome, busca in [("DFS", dfs), ("BFS", bfs), ("Gulosa", gulosa)]:
        caminho, visitadas = busca(grafo, inicio, saida)
        tabela.append((nome, len(caminho) - 1, len(visitadas)))

        print(f"\n=== {nome} ===")
        desenhar(labirinto, caminho)
        print(f"caminho: {len(caminho) - 1} passos | casas visitadas: {len(visitadas)}")

        print(f"\n{nome} - o que foi explorado (o = visitada fora do caminho)")
        desenhar_exploracao(labirinto, caminho, visitadas)

        if nome == "Gulosa":
            fora = [v for v in visitadas if v not in caminho]
            isca = min(fora, key=lambda v: h(v, saida))
            print(f"casa visitada fora do caminho com menor h: {isca} (h = {h(isca, saida)})")

    print(f"\n{'busca':<8}| {'caminho (passos)':>16} | {'casas visitadas':>15}")
    print("-" * 46)
    for nome, passos, visitadas in tabela:
        print(f"{nome:<8}| {passos:>16} | {visitadas:>15}")
    print(f"(casas livres no labirinto: {len(grafo)})")
