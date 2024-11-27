from collections import OrderedDict
def draw_hexagon(side_length):
    # Ukupna visina matrice (gornji deo + donji deo - 1, jer sredina se ponavlja)

    height = 2*(2*side_length-1)-1
    width = 3 * side_length + 2  # Širina matrice

    # Kreiraj matricu dimenzija height x width ispunjenu praznim karakterima
    matrix = [[" " for _ in range(width)] for _ in range(height)]

    # Lista za čuvanje čvorova (sa slovima za redove)
    nodes = {}
    ii=0
    for i in range(0,int(height / 2) ,2):

        dots=side_length+ii
        start=side_length-ii-1
        end=width-dots+2*ii+1
        k=1
        for j in range(start,end,2):
            matrix[i][j] = "●"
            matrix[height-i-1][j] = "●"

            row_label = chr(65 + ii)
            node_label=f"{row_label}{k}"
            nodes[node_label]=(i,j)

            row_label = chr(65 + (int(height/2)-ii))
            node_label = f"{row_label}{k}"
            nodes[node_label] = (int(height/2)-ii,j)
            k+=1
        ii+=1
    ii=1
    row_label = chr(65 + int((height/2)/2))
    for j in range(0,width, 2):
        matrix[int(height/2)][j] = "●"
        node_label = f"{row_label}{ii}"
        nodes[node_label] = (int(height/2),j)
        ii+=1

    nodes = OrderedDict(sorted(nodes.items()))
    print("Pozicije tačaka u matrici:")
    for node_label, (i, j) in nodes.items():
        print(f"{node_label}: red = {i}, kolona = {j}")
    return matrix, nodes

def is_valid_move(matrix, x, y):
    """Provera da li je koordinata (x, y) unutar granica matrice i da li postoji čvor"""
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and (matrix[x][y] == "●" or matrix[x][y] == "■")

def play_move(matrix, nodes, start, direction):
    # Direkcije definisane kao pomeraji u matrici
    directions = {
        "D": (0, 2),      # Desno (isti red)
        "DD": (2, 1),     # Dole desno
        "DL": (2, -1)      # Dole levo
    }

    if start not in nodes or direction not in directions:
        print("Nevalidan potez!")
        return False

    # Dobij početne koordinate
    dx, dy = directions[direction]
    x, y = nodes[start]

    # Iteracija kroz 4 poteza
    positions = [(x + dx * i, y + dy * i) for i in range(4)]
    if direction == "D":
        line="-"
        y+=1
    else:
        if direction == "DD":
            line="\\"
            y+=1
        else:
            line="/"
            y-=1
        x+=1


    # Provera da li su sve pozicije validne
    if all(is_valid_move(matrix, px, py) for px, py in positions):
        for i in range(3):
            if direction == "DL" and "/" not in matrix[x][y] :
                if matrix[x][y] == " ":
                    matrix[x][y] = line
                else :
                    matrix[x][y] = matrix[x][y] + line
            else:
                if direction == "DD" and "\\" not in matrix[x][y] :
                    if matrix[x][y] == " ":
                        matrix[x][y] = line
                    else:
                        matrix[x][y] = line + matrix[x][y]
                else:
                    matrix[x][y] = line
            x += dx
            y += dy
        return True
    else:
        print("Potez izlazi izvan granica ili prelazi nepostojeći čvor!")
        return False

def draw_triangle(matrix):
    for i in range(1, len(matrix), 2):
        for j in range(len(matrix[0])):
            if is_valid_position(matrix,i,j):
               if (is_valid_position(matrix, i + 1, j)
                    and is_valid_position(matrix,j,i-1)
                    and is_valid_position(matrix,i, j+1)):
                   if ("/" in matrix[i][j - 1] and "\\" in matrix[i][j + 1] and "-" in matrix[i + 1][j]):
                       matrix[i][j] = "▲"
                   if is_valid_position(matrix, i - 1, j):
                       if ("\\" in matrix[i][j] and "/" in matrix[i][j] and "-" in matrix[i - 1][j]):
                           matrix[i][j] = "\\▼/"


def print_board(matrix):
    for row in matrix:
        print(" ".join(row))


def is_valid_position(matrix, x, y):
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])


def switch_player(current_player):
    return "racunar" if current_player == "covek" else "covek"

# Main

side_length = int(input("Unesite dužinu stranice heksagona: "))
if 3 < side_length < 9:
    matrix, nodes = draw_hexagon(side_length)
    print_board(matrix)
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
    symbols = {"covek": first_symbol, "racunar": second_symbol}

    while True:
        #print("\nČvorovi: ", ", ".join(nodes.keys()))
        print(f"Na potezu: {current_player} ({symbols[current_player]})")
        move = input("Unesite potez (format: čvor direkcija, npr. A1 D): ").strip().upper()
        if move == "EXIT":
            break
        if(current_player == "covek"):
            try:
                start, direction = move.split()
                valid = play_move(matrix, nodes, start, direction)
                draw_triangle(matrix)
                print_board(matrix)

                if valid:
                    current_player = switch_player(current_player)

            except ValueError:
                print("Unesite potez u ispravnom formatu!")
        else:
            #logika za kompjuter
            try:
                start, direction = move.split()
                valid = play_move(matrix, nodes, start, direction)
                draw_triangle(matrix)
                print_board(matrix)

                if (valid):
                    current_player = switch_player(current_player)

            except ValueError:
                print("Unesite potez u ispravnom formatu!")

else:
    print("Tabla nije odgovarajuce velicine!")