from board import draw_hexagon, print_board
from game_logic import play_move, switch_player, draw_triangle, end_of_game, pass_board_state, possible_states, \
    print_states, minimax_alpha_beta
from utilities import get_depth_based_on_board_size

# Main deo aplikacije

while True:
    try:
        side_length = int(input("Unesite duzinu stranice heksagona (4-8): "))
        if 4 <= side_length <= 8:
            break
        else:
            print("Greska: Dužina stranice mora biti između 4 i 8.")
    except ValueError:
        print("Greska: Molimo unesite ceo broj.")

matrix, nodes = draw_hexagon(side_length)
xp, yp = nodes["A1"]
#print(f"Sirina matrice: {len(matrix[0])}")  # Broj kolona
#print(f"Visina matrice: {len(matrix)}")

# Izbor tipa igre
game_mode = input("Da li zelite da igrate protiv coveka ili racunara? (covek/racunar): ").strip().lower()
while game_mode not in ["covek", "racunar"]:
    game_mode = input("Unesite 'covek' ili 'racunar': ").strip().lower()

# Izbor simbola za prvog igraca
first_symbol = input("Koji simbol zelite da koristite (X/O)? ").strip().upper()
while first_symbol not in ["X", "O"]:
    first_symbol = input("Unesite 'X' ili 'O': ").strip().upper()

second_symbol = "O" if first_symbol == "X" else "X"

# Izbor ko igra prvi
first_player_choice = input("Da li zelite da igrate prvi? (da/ne): ").strip().lower()
while first_player_choice not in ["da", "ne"]:
    first_player_choice = input("Unesite 'da' ili 'ne': ").strip().lower()

# Postavljanje igraca
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
print("Igra pocinje! Nek najbolji pobedi! Uslov za pobedu je da imas vise trouglica nego protivnik!")
print_board(matrix,yp)

#ODAVDE KRECU POTEZI ZA FIKSNA STANJA ---> ZA SAD
#moves_input = "a1 d, a1 dd, a1 dl, a2 dl, a2 dd, a3 dd, a3 dl, b1 d, b1 dd, b1 dl, b2 d, b2 dd, b2 dl, b3 dl, b4 dd, b4 dl, c3 d, c3 dd, c3 dl, c3 d".strip().upper()
#moves = moves_input.split(", ")
#current_player = pass_board_state(moves, matrix, yp, nodes, first_player, second_player, symbols, side_length)
#print(f"Moguca stanja za {current_player} ({symbols[current_player]['symbol']}): ")
#states=possible_states(matrix, nodes)
#print_states(states,yp)

#GLAVNA PETLJA IGRE
while True:
    print(f"Na potezu: {current_player} ({symbols[current_player]['symbol']})")
    if current_player.startswith("covek"):
        move = input("Unesite potez (format: cvor direkcija, npr. A1 D): ").strip().upper()
        if move == "EXIT":
            break
        try:
            start, direction = move.split()
            valid = play_move(matrix, nodes, start, direction, showMessage= True)
            if valid:
                symbols[current_player]["count"] = draw_triangle(matrix, symbols[current_player]["symbol"],
                                                                     symbols[current_player]["count"])
                print_board(matrix, yp)
                print(f"Trenutni rezultat ---> {first_player}: {symbols[first_player]["count"]}"
                          f"  | {second_player}: {symbols[second_player]["count"]}")
                if end_of_game(matrix, symbols[current_player]["count"], side_length):
                    print(f"Pobedio je {current_player}!")
                    break
                current_player = switch_player(current_player, first_player, second_player)
        except ValueError:
            print("Unesite potez u ispravnom formatu! (npr. A1 D)")

    else:
        # Logika za potez racunara
        depth = get_depth_based_on_board_size(side_length)
        print("Računar razmišlja...")
        _, best_move = minimax_alpha_beta(matrix, nodes, depth, alpha=float('-inf'), beta=float('inf'),
                                            maximizing_player=True, player_symbol=symbols[current_player]["symbol"],
                                            opponent_symbol=
                                            symbols[switch_player(current_player, first_player, second_player)][
                                                "symbol"])
        if best_move:
            start, direction = best_move
            valid = play_move(matrix, nodes, start, direction, showMessage = False)
            if valid:
                symbols[current_player]["count"] = draw_triangle(matrix, symbols[current_player]["symbol"],
                                                                     symbols[current_player]["count"])
                print(f"Računar ({symbols[current_player]['symbol']}) igrao je: {start} {direction}")
                print_board(matrix, yp)
                print(f"Trenutni rezultat ---> {first_player}: {symbols[first_player]["count"]}"
                          f"  | {second_player}: {symbols[second_player]["count"]}")
                if end_of_game(matrix, symbols[current_player]["count"], side_length):
                    print(f"Pobedio je {current_player}!")
                    break
                current_player = switch_player(current_player, first_player, second_player)


