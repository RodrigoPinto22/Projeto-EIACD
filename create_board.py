import random

def create_board():
    while True:
        try:
            board_size = int(input("Select the number of branches (6/8/10): "))
            if board_size in [6, 8, 10]:
                num_colors = [num for num in range(1, board_size - 1)]  # RANGE começa em 1!!!!!!!!
                break
        except ValueError:
            print("Unexpected value for board size, try again")
            continue
        print("Unexpected value for board size, try again")

    while True:
        todas_cores = num_colors * 4
        random.shuffle(todas_cores)
        ramos = [todas_cores[i * 4:(i + 1) * 4] for i in range(board_size-2)]
        # Check that no ramo is made up of the same color
        if not any(len(set(ramo)) == 1 for ramo in ramos):
            break

    ramos = [alinhar_ramo(ramo) for ramo in ramos]
    ramos.insert((int(board_size/2)-1),[0] * 4)  # Tubo vazio 1
    ramos.append([0] * 4)  # Tubo vazio 2
    return ramos, board_size

def alinhar_ramo(ramo):
    j = 0
    for i in range(len(ramo)):
        if ramo[i] != " ":
            ramo[j] = ramo[i]
            if j != i:
                ramo[i] = " "
            j += 1
    return ramo
