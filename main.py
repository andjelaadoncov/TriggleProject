from board import draw_hexagon, print_board, parse_matrix
from game_logic import play_move, switch_player, draw_triangle, end_of_game

# Main deo aplikacije

# matrix_str = """          ●-----●-----●-----●
#          / \\
#         / O \\
#        ●-----●-----●-----●     ●
#       / \\ O / \\ X /
#      / O \\ / X \\ /
#     ●-----●-----●-----●     ●     ●
#    /     / \\ O / \\
#   /     /   \\ /   \\
#  ●     ●     ●     ●     ●     ●     ●
#       /     / \\
#      /     /   \\
#     ●     ●     ●     ●     ●     ●
#
#
#        ●     ●     ●     ●     ●
#
#
#           ●     ●     ●     ● """
# # Parsiraj matricu
#
# matrix, nodes = parse_matrix(matrix_str)
# print_board(matrix,9)
# print(f"Širina matrice: {len(matrix[0])}")  # Broj kolona
# print(f"Visina matrice: {len(matrix)}")
#
side_length = int(input("Unesite dužinu stranice heksagona: "))
if 3 < side_length < 9:
    matrix, nodes = draw_hexagon(side_length)
    xp, yp = nodes["A1"]
    print(f"Širina matrice: {len(matrix[0])}")  # Broj kolona
    print(f"Visina matrice: {len(matrix)}")

    # Izbor tipa igre
    game_mode = input("Da li želite da igrate protiv čoveka ili računara? (covek/racunar): ").strip().lower()
    while game_mode not in ["covek", "racunar"]:
        game_mode = input("Unesite 'covek' ili 'racunar': ").strip().lower()

    # Izbor simbola za prvog igrača
    first_symbol = input("Koji simbol želite da koristite (X/O)? ").strip().upper()
    while first_symbol not in ["X", "O"]:
        first_symbol = input("Unesite 'X' ili 'O': ").strip().upper()

    second_symbol = "O" if first_symbol == "X" else "X"

    # Izbor ko igra prvi
    first_player_choice = input("Da li želite da igrate prvi? (da/ne): ").strip().lower()
    while first_player_choice not in ["da", "ne"]:
        first_player_choice = input("Unesite 'da' ili 'ne': ").strip().lower()

    # Postavljanje igrača
    player1 = "covek1"
    player2 = "racunar" if game_mode == "racunar" else "covek2"

    if first_player_choice == "da":
        first_player = player1
        second_player = player2
    else:
        first_player = player2
        second_player = player1

    symbols = {
        first_player: {"symbol": first_symbol if first_player == player1 else second_symbol, "count": 0},
        second_player: {"symbol": second_symbol if first_player == player1 else first_symbol, "count": 0}
    }

    current_player = first_player
    print_board(matrix,yp)

    while True:
        print(f"Na potezu: {current_player} ({symbols[current_player]['symbol']})")
        if current_player.startswith("covek"):
            move = input("Unesite potez (format: čvor direkcija, npr. A1 D): ").strip().upper()
            if move == "EXIT":
                break
            try:
                start, direction = move.split()
                valid = play_move(matrix, nodes, start, direction)
                if valid:
                    symbols[current_player]["count"] = draw_triangle(matrix, symbols[current_player]["symbol"],
                                                                     symbols[current_player]["count"])
                    print_board(matrix, yp)
                    if end_of_game(matrix, symbols[current_player]["count"], side_length):
                        print(f"Pobedio je {current_player}!")
                        break
                    current_player = switch_player(current_player, first_player, second_player)
            except ValueError:
                print("Unesite potez u ispravnom formatu!")
        else:
            # Logika za potez računara
            # Ovde može biti implementirana logika za računara -----> za sada idalje implementirana kao za obicnog coveka NEDOVRSENOOO
            move = input("Unesite potez (format: čvor direkcija, npr. A1 D): ").strip().upper()
            if move == "EXIT":
                break
            try:
                start, direction = move.split()
                valid = play_move(matrix, nodes, start, direction)
                if valid:
                    symbols[current_player]["count"] = draw_triangle(matrix, symbols[current_player]["symbol"],
                                                                     symbols[current_player]["count"])
                    print_board(matrix, yp)
                    if end_of_game(matrix, symbols[current_player]["count"], side_length):
                        print(f"Pobedio je {current_player}!")
                        break
                    current_player = switch_player(current_player, first_player, second_player)
            except ValueError:
                print("Unesite potez u ispravnom formatu!")
else:
    print("Tabla nije odgovarajuce velicine!")

