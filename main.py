from collections import OrderedDict
def draw_hexagon(side_length):
    # Ukupna visina matrice (gornji deo + donji deo - 1, jer sredina se ponavlja)

    height = 3 * side_length + 2
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
    x, y = nodes[start]
    dx, dy = directions[direction]

    # Iteracija kroz 4 poteza
    positions = [(x + dx * i, y + dy * i) for i in range(4)]

    # Provera da li su sve pozicije validne
    if all(is_valid_move(matrix, px, py) for px, py in positions):
        # Ako su sve pozicije validne, postavi kvadratiće
        for px, py in positions:
            matrix[px][py] = "■"

        return True
    else:
        print("Potez izlazi izvan granica ili prelazi nepostojeći čvor!")
        return False


def print_board(matrix):
    for row in matrix:
        print(" ".join(row))


def is_valid_position(matrix, x, y):
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])


def draw_triangle(matrix, nodes):
    for node_label, (i, j) in nodes.items():
        if(is_valid_position(matrix, i, j) and matrix[i][j]=="■"):
            # Proveri gornji trougao
            if (is_valid_position(matrix, i - 2, j - 1) and
                    is_valid_position(matrix, i - 2, j + 1) and
                    matrix[i - 2][j - 1] == "■" and
                    matrix[i - 2][j + 1] == "■" and
                    is_valid_position(matrix, i - 1, j)):
                matrix[i - 1][j] = "▲"

            # Proveri donji trougao
            if (is_valid_position(matrix, i + 2, j - 1) and
                    is_valid_position(matrix, i + 2, j + 1) and
                    matrix[i + 2][j - 1] == "■" and
                    matrix[i + 2][j + 1] == "■" and
                    is_valid_position(matrix, i + 1, j)):
                matrix[i + 1][j] = "▲"

            # Proveri levi trougao
            if (is_valid_position(matrix, i - 2, j - 1) and
                    is_valid_position(matrix, i + 2, j - 1) and
                    matrix[i - 2][j - 1] == "■" and
                    matrix[i + 2][j - 1] == "■" and
                    is_valid_position(matrix, i, j - 1)):
                matrix[i][j - 1] = "▲"

            # Proveri desni trougao
            if (is_valid_position(matrix, i - 2, j + 1) and
                    is_valid_position(matrix, i + 2, j + 1) and
                    matrix[i - 2][j + 1] == "■" and
                    matrix[i + 2][j + 1] == "■" and
                    is_valid_position(matrix, i, j + 1)):
                matrix[i][j + 1] = "▲"
                # LEVO GORE
            if (is_valid_position(matrix, i - 2, j - 1) and
                    is_valid_position(matrix, i , j -2) and
                    matrix[i - 2][j - 1] == "■" and
                    matrix[i][j - 2] == "■" and
                    is_valid_position(matrix, i, j - 1)):
                matrix[i-1][j - 1] = "▲"
            #levo dole
            if (is_valid_position(matrix, i+2, j - 2) and
                    is_valid_position(matrix, i, j - 2) and
                    matrix[i - 2][j - 1] == "■" and
                    matrix[i][j - 2] == "■" and
                    is_valid_position(matrix, i-1, j - 1)):
                matrix[i-1][j - 1] = "▲"
            #desno gore
            if (is_valid_position(matrix, i - 2, j + 1) and
                    is_valid_position(matrix, i, j + 2) and
                    matrix[i - 2][j + 1] == "■" and
                    matrix[i][j + 2] == "■" and
                    is_valid_position(matrix, i-1, j + 1)):
                matrix[i-1][j + 1] = "▲"
            #desno dole
            if (is_valid_position(matrix, i + 2, j + 1) and
                    is_valid_position(matrix, i, j + 2) and
                    matrix[i + 2][j + 1] == "■" and
                    matrix[i][j + 2] == "■" and
                    is_valid_position(matrix, i+1, j + 1)):
                matrix[i+1][j + 1] = "▲"

def switch_player(current_player):
    return "računar" if current_player == "čovek" else "čovek"

# Main

side_length = int(input("Unesite dužinu stranice heksagona: "))
if 3 < side_length < 9:
    matrix, nodes = draw_hexagon(side_length)
    print_board(matrix)
    print(f"Širina matrice: {len(matrix[0])}")  # Broj kolona
    print(f"Visina matrice: {len(matrix)}")

    player_choice = input("Ko igra prvi (čovek/računar)? ").strip().lower()
    while player_choice not in ["čovek", "računar"]:
        player_choice = input("Unesite 'čovek' ili 'računar': ").strip().lower()

    first_symbol = input("Koji simbol igra prvi (X/O)? ").strip().upper()
    while first_symbol not in ["X", "O"]:
        first_symbol = input("Unesite 'X' ili 'O': ").strip().upper()

    second_symbol = "O" if first_symbol == "X" else "X"
    current_player = player_choice
    symbols = {"čovek": first_symbol, "računar": second_symbol}

    while True:
        #print("\nČvorovi: ", ", ".join(nodes.keys()))
        print(f"Na potezu: {current_player} ({symbols[current_player]})")
        move = input("Unesite potez (format: čvor direkcija, npr. A1 D): ").strip().upper()
        if move == "EXIT":
            break
        if(current_player == "čovek"):
            try:
                start, direction = move.split()
                valid = play_move(matrix, nodes, start, direction)
                draw_triangle(matrix, nodes)
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
                draw_triangle(matrix, nodes)
                print_board(matrix)

                if (valid):
                    current_player = switch_player(current_player)

            except ValueError:
                print("Unesite potez u ispravnom formatu!")

else:
    print("Tabla nije odgovarajuce velicine!")