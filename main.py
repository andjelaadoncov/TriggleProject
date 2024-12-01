from board import draw_hexagon, print_board, parse_matrix
from game_logic import play_move, switch_player, draw_triangle, end_of_game

# Main deo aplikacije


#
# matrix_str = """          ●-----●-----●-----●
#           / \
#          / O \
#        ●-----●-----●-----●     ●
#        / \ O / \ X /
#       / O \ / X \ /
#     ●-----●-----●-----●     ●     ●
#     /     / \ O / \
#    /     /   \ /   \
#  ●     ●     ●     ●     ●     ●     ●
#        /     / \
#       /     /   \
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
# #
side_length = int(input("Unesite dužinu stranice heksagona: "))
if 3 < side_length < 9:
    matrix, nodes = draw_hexagon(side_length)
    xp, yp = nodes["A1"]
    print_board(matrix,yp)
    print(f"Širina matrice: {len(matrix[0])}")  # Broj kolona
    print(f"Visina matrice: {len(matrix)}")

    player_choice = input("Ko igra prvi (čovek/računar)? ").strip().lower()
    while player_choice not in ["covek", "racunar"]:
        player_choice = input("Unesite 'čovek' ili 'računar': ").strip().lower()

    first_symbol = input("Koji simbol igra prvi (X/O)? ").strip().upper()
    while first_symbol not in ["X", "O"]:
        first_symbol = input("Unesite 'X' ili 'O': ").strip().upper()

    second_symbol = "O" if first_symbol == "X" else "X"
    current_player = player_choice
    symbols = {
        "covek": {"symbol": first_symbol, "count": 0},
        "racunar": {"symbol": second_symbol, "count": 0}
    }

    while True:
        print(f"Na potezu: {current_player} ({symbols[current_player]})")
        move = input("Unesite potez (format: čvor direkcija, npr. A1 D): ").strip().upper()
        if move == "EXIT":
            break
        if current_player == "covek":
            try:
                start, direction = move.split()
                valid = play_move(matrix, nodes, start, direction)
                if valid:
                    symbols[current_player]["count"]=draw_triangle(matrix, symbols[current_player]["symbol"],symbols[current_player]["count"])  # Dodavanje simbola
                    print_board(matrix,yp)
                    if end_of_game(matrix, symbols[current_player]["count"], side_length):
                        print(f"Pobedio je {current_player}!")
                        break
                    current_player = switch_player(current_player)
            except ValueError:
                print("Unesite potez u ispravnom formatu!")
        else:
            #ovo je deo kad kompjuter igra -->sl faza izmena
            try:
                start, direction = move.split()
                valid = play_move(matrix, nodes, start, direction)
                if valid:
                    symbols[current_player]["count"]= draw_triangle(matrix, symbols[current_player]["symbol"],symbols[current_player]["count"])  # Dodavanje simbola
                    print_board(matrix,yp)
                    if end_of_game(matrix, symbols[current_player]["count"], side_length):
                        print(f"Pobedio je {current_player}!")
                        break
                    current_player = switch_player(current_player)
            except ValueError:
                print("Unesite potez u ispravnom formatu!")
else:
    print("Tabla nije odgovarajuce velicine!")

