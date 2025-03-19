def check_move(b1, b2, board):
    #while True:
    print(board[0])
    consecutive_values = get_consecutive(board[b1])
    if board[b2][0] != 0:
        print("Impossible Move! Try another one")
        return
    elif board[b2][3] == 0:
        i = 0
        while board[b1][i] == 0:
            continue
        c = 0
        board[b2][3] = board[b1][0]



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

