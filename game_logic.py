#OVDE SE NALAZI SVE STO SE TICE LOGIKE SAME IGRE, POTEZA I PROVERE VALIDNOSTI, KRAJA IGRE...
from utilities import max_connections

def is_valid_move(matrix, x, y):
    """Provera da li je koordinata (x, y) unutar granica matrice i da li postoji čvor"""
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])

def play_move(matrix, nodes, start, direction):
    # Directions defined as matrix moves
    directions = {"D", "DD", "DL"}  # Right, Down-Right, Down-Left

    if start not in nodes or direction not in directions:
        print("Nevalidan potez!")
        return False

    # Get initial coordinates
    x, y = nodes[start]
    positions = []

    if direction == "D":
        line = "-"
        for dy in range(1, 18):  # Start from 1 to skip initial node
            if dy % 6 != 0:
                positions.append((x, y + dy))
        positions.append((x, y + 18))
    elif direction == "DD":
        line = "\\"
        for dx in range(1, 9):  # Start from 1 to skip initial node
            dy = dx  # Equal step for Down-Right
            if dx % 3 != 0:
                positions.append((x + dx, y + dy))

        positions.append((x+9, y + 9))

    elif direction == "DL":
        line = "/"
        for dx in range(1, 9):  # Start from 1 to skip initial node
            dy = dx  # Equal step for Down-Left
            if dx % 3 != 0:
                positions.append((x + dx, y - dy))
        positions.append((x+9, y - 9))
    last_px, last_py = positions[-1]
    # Validate all positions and update the matrix if valid
    if all(is_valid_move(matrix, px, py) for px, py in positions) and  matrix[last_px][last_py] == "●":
        positions.pop()
        for px, py in positions:
            matrix[px][py] = line
        return True
    else:
        print("Potez izlazi izvan granica ili prelazi nepostojeći čvor!")
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


def switch_player(current_player):
    return "racunar" if current_player == "covek" else "covek"

def end_of_game(matrix, count, side_length):
    max_triangles = 0
    for i in range(side_length, 2 * side_length - 1):
        max_triangles += 2 * i - 1

    print(str(max_triangles) + " Maksimalni broj trouglova je.")

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
        print(str(p)+" trenutne stranice")
        return False