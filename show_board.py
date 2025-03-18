def print_jogo(jogo):
    linha_superior = jogo[:3]  # Pegamos os 3 primeiros ramos (lado esquerdo)
    linha_inferior = jogo[3:]  # Pegamos os 3 últimos ramos (lado direito)

    print("-----------------------------------------")

    for i in range(3):  # Percorre cada "coluna" do jogo
        print(f"{linha_superior[i]}    |    {linha_inferior[i]}")  # Mantemos as colunas corretas
