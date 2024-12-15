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
        print("Ovaj potez je vec odigran (svi cvorovi zauzeti)!")
        return False
    return True

def play_move(matrix, nodes, start, direction, helper = False):
    global zauzeti_cvorovi
    directions = {"D", "DD", "DL"}  # desno, dole desno, dole levo

    if start not in nodes or direction not in directions:
        print("Nevalidan potez!")
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

    if (all(is_valid_move(matrix, px, py) for px, py in positions) and
            matrix[last_px][last_py] == "●" and
            is_valid_rubber_band(positions)):
        # Ako je potez validan, dodaje cvorove u zauzete i azurira matricu
        if(helper == False):
            zauzeti_cvorovi.update(positions)  # Dodaj sve cvorove ovog poteza u zauzete

        positions.pop()  # Uklanja poslednju poziciju (cvor)
        for px, py in positions:
            matrix[px][py] = line
        return True
    else:
        print("Potez nije validan!")
        return False

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