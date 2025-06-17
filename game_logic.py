#OVDE SE NALAZI SVE STO SE TICE LOGIKE SAME IGRE, POTEZA I PROVERE VALIDNOSTI, KRAJA IGRE...

from utilities import max_connections
from board import print_board

# Pracenje svih zauzetih cvorova
zauzeti_cvorovi = set()

def is_valid_move(matrix, x, y):
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])

#funkcija koja proverava da se ne poklapa potez
def is_valid_rubber_band(positions):
    global zauzeti_cvorovi

    if all((px, py) in zauzeti_cvorovi for px, py in positions):
        #print("Ovaj potez je vec odigran (svi cvorovi zauzeti)!")
        return False
    return True

def play_move(matrix, nodes, start, direction, helper = False, showMessage = False):
    global zauzeti_cvorovi
    directions = {"D", "DD", "DL"}  # desno, dole desno, dole levo

    if start not in nodes or direction not in directions:
        print("Nevalidan potez! Pokusajte ponovo.")
        return False


    x, y = nodes[start]
    positions = []

    if direction == "D":
        line = "-"
        for dy in range(1, 18):
            if dy % 6 != 0:
                positions.append((x, y + dy))
        positions.append((x, y + 18))
    elif direction == "DD":
        line = "\\"
        for dx in range(1, 9):
            dy = dx
            if dx % 3 != 0:
                positions.append((x + dx, y + dy))

        positions.append((x+9, y + 9))

    elif direction == "DL":
        line = "/"
        for dx in range(1, 9):
            dy = dx
            if dx % 3 != 0:
                positions.append((x + dx, y - dy))
        positions.append((x+9, y - 9))
    last_px, last_py = positions[-1]

    if not all(is_valid_move(matrix, px, py) for px, py in positions):
        if showMessage:
            print("Nevalidan potez! Neki deo gumice izlazi van table, pokusajte ponovo.")
        return False

    if matrix[last_px][last_py] != "●":
        if showMessage:
            print("Nevalidan potez! Neki deo gumice izlazi van table, pokusajte ponovo.")
        return False

    if not is_valid_rubber_band(positions):
        if showMessage:
            print("Nevalidan potez! Ovaj potez je vec odigran, pokusajte ponovo.")
        return False

    if not helper:
        zauzeti_cvorovi.update(positions)

    positions.pop()  # Uklanja poslednju poziciju (cvor)
    for px, py in positions:
        matrix[px][py] = line

    return True

def draw_triangle(matrix, symbol, count):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == " ":
                if (is_valid_move(matrix, i - 1, j + 1) and matrix[i - 1][j + 1] == "\\" and
                        is_valid_move(matrix, i - 1, j - 1) and matrix[i - 1][j - 1] == "/" and
                        is_valid_move(matrix, i + 1, j) and matrix[i + 1][j] == "-"):
                    matrix[i][j] = symbol
                    count += 1
                else:
                    if (is_valid_move(matrix, i + 1, j - 1) and matrix[i + 1][j - 1] == "\\" and
                            is_valid_move(matrix, i + 1, j + 1) and matrix[i + 1][j + 1] == "/" and
                            is_valid_move(matrix, i - 1, j) and matrix[i - 1][j] == "-"):
                        matrix[i][j] = symbol
                        count += 1
    return count


def switch_player(current_player, player1, player2):
    return player1 if current_player == player2 else player2

def end_of_game(matrix, count, side_length):
    max_triangles = 0
    for i in range(side_length, 2 * side_length - 1):
        max_triangles += 2 * i - 1

#    print(str(max_triangles) + " Maksimalni broj trouglova")

    if count >= max_triangles:
        print(str(count) + " Kraj igre! Maksimalni broj trouglova je dostignut.")
        return True
    else:
        p = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == "●":
                    if (is_valid_move(matrix, i + 1, j - 1) and matrix[i + 1][j - 1] == "/"):
                        p += 1
                    if (is_valid_move(matrix, i + 1, j + 1) and matrix[i + 1][j + 1] == "\\"):
                        p += 1
                    if (is_valid_move(matrix, i, j + 1) and matrix[i][j + 1] == "-"):
                        p += 1
        conn =max_connections(side_length)
        if p == conn:
            print("Kraj igre! Maksimalni broj gumica je razvucen")
            return True
#        print(str(p)+" trenutne stranice")
        return False


def pass_board_state(moves, matrix, yp, nodes, player1, player2, symbols, side_length):
    current_player = player1
    for move in moves:
        try:
            start, direction = move.split()
            valid = play_move(matrix, nodes, start, direction)
            if valid:
                symbols[current_player]["count"] = draw_triangle(matrix, symbols[current_player]["symbol"],
                                                                 symbols[current_player]["count"])
                print(f"{current_player} ({symbols[current_player]['symbol']}) je igrao: {move}")
                print_board(matrix, yp)
                if end_of_game(matrix, symbols[current_player]["count"], side_length):
                    print(f"Pobedio je {current_player}!")
                    break

                current_player = switch_player(current_player, player1, player2)
            else:
                print(f"Potez {move} nije validan! Preskace se.")
        except ValueError:
            print(f"Potez {move} nije u ispravnom formatu! Preskace se.")

    return current_player

def possible_states(matrix, nodes):
    states={}
    directions = {"D", "DD", "DL"}
    helper = True
    for cvor in nodes:
        for dir in directions:
            matrix_copy = [row[:] for row in matrix]
            if not play_move(matrix_copy, nodes, cvor, dir, helper):
                continue
            states[(cvor, dir)] = matrix_copy
    return states

def print_states(states,y):
    for move, mat in states.items():
        cvor, dir = move
        print(f"Potez: Cvor = {cvor}, Pravac = {dir}")
        print("Matrica nakon poteza:")
        print_board(mat,y)
        print("-" * 20)


def evaluate_state(matrix, player_symbol, opponent_symbol):
    #inicijalni skorovi za igrace
    player_score = 0
    opponent_score = 0

    # najvise poena se ostvara na osvajanje trougla
    triangle_value = 100
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == player_symbol:
                player_score += triangle_value
            elif matrix[i][j] == opponent_symbol:
                opponent_score += triangle_value

    # bonus poeni za povezane trouglove
    connected_bonus = 20
    player_connected = count_connected_triangles(matrix, player_symbol)
    opponent_connected = count_connected_triangles(matrix, opponent_symbol)
    player_score += player_connected * connected_bonus
    opponent_score += opponent_connected * connected_bonus

    # bonus poeni za kontrolu teritorije
    territory_bonus = 10
    player_territory = evaluate_territory_control(matrix, player_symbol)
    opponent_territory = evaluate_territory_control(matrix, opponent_symbol)
    player_score += player_territory * territory_bonus
    opponent_score += opponent_territory * territory_bonus

    # bonus za potencijalne trouglove koji mogu da se osvoje u sledecim potezima
    potential_bonus = 30
    player_potential = count_possible_triangles(matrix, player_symbol)
    opponent_potential = count_possible_triangles(matrix, opponent_symbol)
    player_score += player_potential * potential_bonus
    opponent_score += opponent_potential * potential_bonus

    return player_score - opponent_score


def count_connected_triangles(matrix, symbol):
    # ova fja racuna broj povezanih trouglova istog igraca
    # povezani trouglovi dele bar jednu ivicu ili teme
    connected_count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == symbol:
                # proveri susedne trouglove (gore, dole, levo, desno)
                neighbors = [
                    (i - 2, j), (i + 2, j),  # gore/dole
                    (i, j - 2), (i, j + 2),  # levo/desno
                    (i - 1, j - 1), (i - 1, j + 1),  # gore-levo/gore-desno
                    (i + 1, j - 1), (i + 1, j + 1)  # dole-levo/dole-desno
                ]

                for ni, nj in neighbors:
                    if (0 <= ni < len(matrix) and
                            0 <= nj < len(matrix[0]) and
                            matrix[ni][nj] == symbol):
                        connected_count += 1

    return connected_count // 2  # delimo sa 2 jer smo svaku vezu brojali dvaput


def evaluate_territory_control(matrix, symbol):

    # fja kojom procenjujemo koliko teritorije kontrolise igrac
    # bonus ako je trougao blizu centra
    # bonus za slobodna polja oko sebe
    # bonus ako blokira protivnika

    territory_score = 0
    center_bonus = 2  #

    # pronalazi centar matrice
    center_i = len(matrix) // 2
    center_j = len(matrix[0]) // 2

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == symbol:
                # bonus za blizinu centru
                distance_to_center = abs(i - center_i) + abs(j - center_j)
                if distance_to_center < len(matrix) // 3:
                    territory_score += center_bonus

                #  susedi oko trougla najblizi
                neighbors = [
                    (i - 1, j), (i + 1, j),
                    (i, j - 1), (i, j + 1),
                    (i - 1, j - 1), (i + 1, j + 1)
                ]

                for ni, nj in neighbors:
                    if (0 <= ni < len(matrix) and
                            0 <= nj < len(matrix[0])):
                        if matrix[ni][nj] == " ":
                            # ako je slobodno, plus 1
                            territory_score += 1
                        elif matrix[ni][nj] not in ["-", "\\", "/", "●"]:
                            # ako se tu nalazi protivnički trougao, bonus za blokiranje
                            territory_score += 3

    return territory_score

def count_possible_triangles(matrix, player_symbol):
    #fja koja racuna koliko trouglova moze biti osvojeno u narednom potezu

    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == " ":
                # proverava da li trougao moze da se formira
                if (is_valid_move(matrix, i - 1, j + 1) and matrix[i - 1][j + 1] == "\\" and
                        is_valid_move(matrix, i - 1, j - 1) and matrix[i - 1][j - 1] == "/" and
                        is_valid_move(matrix, i + 1, j) and matrix[i + 1][j] == "-"):
                    count += 1
                elif (is_valid_move(matrix, i + 1, j - 1) and matrix[i + 1][j - 1] == "\\" and
                      is_valid_move(matrix, i + 1, j + 1) and matrix[i + 1][j + 1] == "/" and
                      is_valid_move(matrix, i - 1, j) and matrix[i - 1][j] == "-"):
                    count += 1
    return count


def minimax_alpha_beta(matrix, nodes, depth, alpha, beta, maximizing_player, player_symbol, opponent_symbol):
    # min-Max algoritam sa alfa-beta odsecanjem

    # ako smo dostigli maksimalnu dubinu ili je kraj igre mora da se evaluira stanje
    if depth == 0 or end_of_game(matrix, 0, len(matrix) // 3):
        return evaluate_state(matrix, player_symbol, opponent_symbol), None

    possible_moves = possible_states(matrix, nodes)
    best_move = None

    if maximizing_player:
        # racunar pokusava da maksimizuje svoju evaluaciju
        max_eval = float('-inf')
        for move, new_state in possible_moves.items():
            # izracunaj trenutni broj trouglova koji se mogu osvojiti ovim potezom
            current_eval = count_possible_triangles(new_state, player_symbol)

            eval_score, _ = minimax_alpha_beta(new_state, nodes, depth - 1, alpha, beta, False, player_symbol, opponent_symbol)
            total_eval = current_eval + eval_score  # dodaj trenutno osvojene trouglove

            if total_eval > max_eval:
                max_eval = total_eval
                best_move = move
            alpha = max(alpha, total_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        # protivnik minimizuje evaluaciju
        min_eval = float('inf')
        for move, new_state in possible_moves.items():
            eval_score, _ = minimax_alpha_beta(new_state, nodes, depth - 1, alpha, beta, True, player_symbol, opponent_symbol)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

