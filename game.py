from collections import deque

def print_jogo(jogo, board_size):
    mid_index = int(board_size/2)
    linha_superior = jogo[:mid_index]  # Pegamos os 3 primeiros ramos (lado esquerdo)
    linha_inferior = jogo[mid_index:]  # Pegamos os 3 últimos ramos (lado direito)

    print("-----------------------------------------")

    for i in range(mid_index):  # Percorre cada "coluna" do jogo
        print(f"{linha_superior[i][::-1]}    |    {linha_inferior[i]}")  # Mantemos as colunas corretas


def make_move(board_info):
    board = board_info[0]
    board_size = board_info[1]
    #INDEX de 1 - 8
    while True:
        print_jogo(board, board_size)

        try:
            idx1 = int(input("Select the first branch: "))
            idx2 = int(input("Select the second branch: "))
            if idx1 > board_size or idx2 > board_size:
                print("Unexpected value, try again")
                continue
            check_move(idx1-1, idx2-1, board)
        except ValueError:
            print("Unexpected value, try again")


def check_move(b1, b2, board):
    print(board[0])
    consecutive_values = get_consecutive(board[b1])
    if board[b2][0] != 0:
        print("Impossible Move! Try another one")
        return
    elif board[b2][3] == 0:
        print(f"consec = {consecutive_values}")
        board[b2][3] = board[b1][0]
        board[b1][0] = 0

    return b1, b2

def get_consecutive(arr):
    i = 0
    while arr[i] == 0:
        i +=1
    if arr[i] == arr[i+1]:
        if arr[i] == arr[i+2]:
            return 2
        return 1
    return 0




