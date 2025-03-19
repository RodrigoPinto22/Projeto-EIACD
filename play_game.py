from show_board import print_jogo
from move_check import check_move
from collections import deque

def make_move(board_info):
    board = board_info[0]
    board_size = board_info[1]
    #INDEX de 1 - 7
    while True:
        print_jogo(board, board_size)

        try:
            idx1 = int(input("Select the first branch: "))
            idx2 = int(input("Select the second branch: "))
            if idx1 >= board_size or idx2 >= board_size:
                print("Unexpected value, try again")
                continue
            check_move(idx1, idx2, board)
        except ValueError:
            print("Unexpected value, try again")



