def print_jogo(jogo, board_size):
    mid_index = int(board_size/2)
    linha_superior = jogo[:mid_index]  # Pegamos os 3 primeiros ramos (lado esquerdo)
    linha_inferior = jogo[mid_index:]  # Pegamos os 3 últimos ramos (lado direito)

    print("-----------------------------------------")

    for i in range(mid_index):  # Percorre cada "coluna" do jogo
        print(f"{linha_superior[i][::-1]}    |    {linha_inferior[i]}")  # Mantemos as colunas corretas
