import random

def create_board():
    cores = ["vermelho", "verde", "azul", "amarelo"]

    while True:
        todas_cores = cores * 4
        random.shuffle(todas_cores)
        ramos = [todas_cores[i * 4:(i + 1) * 4] for i in range(4)]
        # Check that no ramo is made up of the same color
        if not any(len(set(ramo)) == 1 for ramo in ramos):
            break

    positions = sorted(random.sample(range(len(ramos) + 1), 2))
    for offset, pos in enumerate(positions):
        ramos.insert(pos + offset, [" "] * 4)

    ramos = [alinhar_ramo(ramo) for ramo in ramos]

    return ramos

def alinhar_ramo(ramo):
    j = 0
    for i in range(len(ramo)):
        if ramo[i] != " ":
            ramo[j] = ramo[i]
            if j != i:
                ramo[i] = " "
            j += 1
    return ramo