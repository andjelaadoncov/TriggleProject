from collections import OrderedDict
def parse_matrix(matrix_str):
    rows = matrix_str.split("\n")
    matrix = [list(row) for row in rows]
    side_length = matrix_str[0].count("●")
    height = 3 * (2 * side_length - 2) + 1
    width = 6 * (2 * side_length - 2) + 1  # Širina matrice
    nodes = {}
    dots = side_length - 1
    start = int(width / 4) + 3
    end = int(3 * width / 4) - 2
    hpom = height - 1 + 3
    ii = 0
    for i in range(0, int(height / 2), 3):
        dots += 1
        start -= 3
        end += 3
        hpom -= 3
        jj = 1
        for j in range(start, end, 6):
            matrix[i][j] = "●"
            matrix[hpom][j] = "●"

            row_label = chr(65 + ii)
            node_label = f"{row_label}{jj}"
            nodes[node_label] = (i, j)

            row_label = chr(65 + (2 * side_length - 2 - ii))
            node_label = f"{row_label}{jj}"
            nodes[node_label] = (height - 1 - i, j)
            jj += 1
        ii += 1
    jj = 1
    for j in range(0, width, 6):
        matrix[int(height / 2)][j] = "●"
        row_label = chr(65 + ii)
        node_label = f"{row_label}{jj}"
        nodes[node_label] = (int(height / 2), j)
        jj += 1

    nodes = OrderedDict(sorted(nodes.items()))
    print("Pozicije tačaka u matrici:")
    for node_label, (i, j) in nodes.items():
        print(f"{node_label}: red = {i}, kolona = {j}")
    return matrix, nodes


def draw_hexagon(side_length):
    # Ukupna visina matrice (gornji deo + donji deo - 1, jer sredina se ponavlja)

    height = 3*(2*side_length-2)+1
    width = 6*(2*side_length-2)+1 # Širina matrice

    # Kreiraj matricu dimenzija height x width ispunjenu praznim karakterima
    matrix = [[" " for _ in range(width)] for _ in range(height)]

    # Lista za čuvanje čvorova (sa slovima za redove)
    nodes = {}
    dots =side_length-1
    start=int(width/4)+3
    end = int(3*width/4) -2
    hpom=height-1+3
    ii=0
    for i in range(0,int(height / 2) ,3):
        dots+=1
        start-=3
        end+=3
        hpom-=3
        jj = 1
        for j in range(start,end,6):
            matrix[i][j] = "●"
            matrix[hpom][j] = "●"

            row_label = chr(65 + ii)
            node_label=f"{row_label}{jj}"
            nodes[node_label]=(i,j)

            row_label = chr(65 + (2*side_length-2-ii))
            node_label = f"{row_label}{jj}"
            nodes[node_label] = (height-1-i,j)
            jj+=1
        ii+=1
    jj=1
    for j in range(0, width, 6):
        matrix[int(height/2)][j] = "●"
        row_label = chr(65 + ii)
        node_label = f"{row_label}{jj}"
        nodes[node_label] = (int(height/2), j)
        jj+=1

    nodes = OrderedDict(sorted(nodes.items()))
    print("Pozicije tačaka u matrici:")
    for node_label, (i, j) in nodes.items():
        print(f"{node_label}: red = {i}, kolona = {j}")
    return matrix, nodes

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
    elif direction == "DD":
        line = "\\"
        for dx in range(1, 9):  # Start from 1 to skip initial node
            dy = dx  # Equal step for Down-Right
            if dx % 3 != 0:
                positions.append((x + dx, y + dy))
    elif direction == "DL":
        line = "/"
        for dx in range(1, 9):  # Start from 1 to skip initial node
            dy = dx  # Equal step for Down-Left
            if dx % 3 != 0:
                positions.append((x + dx, y - dy))

    # Validate all positions and update the matrix if valid
    if all(is_valid_move(matrix, px, py) for px, py in positions):
        for px, py in positions:
            matrix[px][py] = line
        return True
    else:
        print("Potez izlazi izvan granica ili prelazi nepostojeći čvor!")
        return False

def draw_triangle(matrix, symbol, count,max_triangles):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if count >= max_triangles:
                print("Kraj igre! Maksimalni broj trouglova je dostignut.")
                return count
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


def print_board(matrix,y):
    first_row = [" "] * (y + 3)  # Prva prazna mesta do x+2
    col_num = 1
    for i in range(y + 3, y+3+len(matrix[0])):  # Numeracija počinje od x+3 na svakom 6. mestu
        if (i - (y + 3)) % 6 == 0:  # Dodajemo broj na svakom 6. mestu
            first_row.append(str(col_num))
            col_num += 1
        else:
            first_row.append(" ")

    print("  " + "".join(first_row))
    for index, row in enumerate(matrix):
        row = [str(cell) for cell in row]  # Obezbeđujemo da su svi elementi stringovi

        if index % 3 == 0:
            print(chr(65 + index // 3) + " " + "".join(row))  # Ispisujemo red sa oznakom
        else:
            print("  " + "".join(row))

def switch_player(current_player):
    return "racunar" if current_player == "covek" else "covek"



# Main

# matrix_str = """          ●-----●-----●-----●
#           / \\
#          / O \\
#        ●-----●-----●-----●     ●
#        / \\ O / \\ X /
#       / O \\ / X \\ /
#     ●-----●-----●-----●     ●     ●
#     /     / \\ O / \\
#    /     /   \\ /   \\
#  ●     ●     ●     ●     ●     ●     ●
#        /     / \\
#       /     /   \\
#     ●     ●     ●     ●     ●     ●
#
#
#        ●     ●     ●     ●     ●
#
#
#           ●     ●     ●     ● """
#
# # Parsiraj matricu
#
# matrix, nodes = parse_matrix(matrix_str)
# print_board(matrix,9)
# print(f"Širina matrice: {len(matrix[0])}")  # Broj kolona
# print(f"Visina matrice: {len(matrix)}")

side_length = int(input("Unesite dužinu stranice heksagona: "))
if 3 < side_length < 9:
    matrix, nodes = draw_hexagon(side_length)
    xp, yp = nodes["A1"]
    print_board(matrix,yp)
    print(f"Širina matrice: {len(matrix[0])}")  # Broj kolona
    print(f"Visina matrice: {len(matrix)}")


    max_triangles =0
    for i in range(side_length,2*side_length-2):
         max_triangles+=2*side_length-1
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
                    symbols[current_player]["count"]=draw_triangle(matrix, symbols[current_player]["symbol"],symbols[current_player]["count"],max_triangles)  # Dodavanje simbola
                    print_board(matrix,yp)
                    current_player = switch_player(current_player)
            except ValueError:
                print("Unesite potez u ispravnom formatu!")
        else:
            # Logika za kompjuter
            try:
                start, direction = move.split()
                valid = play_move(matrix, nodes, start, direction)
                if valid:
                    symbols[current_player]["count"]= draw_triangle(matrix, symbols[current_player]["symbol"],symbols[current_player]["count"],max_triangles)  # Dodavanje simbola
                    print_board(matrix,yp)
                    current_player = switch_player(current_player)
            except ValueError:
                print("Unesite potez u ispravnom formatu!")


else:
    print("Tabla nije odgovarajuce velicine!")

