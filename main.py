from create_board import create_board
from game import make_move

def main():

    board_info = create_board()
    make_move(board_info)

if __name__ == '__main__':
    main()
