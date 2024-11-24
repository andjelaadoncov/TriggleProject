from collections import OrderedDict
def draw_hexagon(side_length):
    # Ukupna visina matrice (gornji deo + donji deo - 1, jer sredina se ponavlja)
    height = 2 * side_length - 1
    width = 3 * side_length + 2  # Širina matrice

    # Kreiraj matricu dimenzija height x width ispunjenu praznim karakterima
    matrix = [[" " for _ in range(width)] for _ in range(height)]

    # Lista za čuvanje čvorova (sa slovima za redove)
    nodes = {}


    for i in range(int(height / 2) + 1):
        dots=side_length+i
        start=side_length-i-1
        end=width-dots+2*i+1
        k=1
        for j in range(start,end,2):
            matrix[i][j] = "●"
            matrix[height-i-1][j] = "●"

            row_label = chr(65 + i)
            node_label=f"{row_label}{k}"
            nodes[node_label]=(i,j)

            row_label = chr(65 + (height-i-1))
            node_label = f"{row_label}{k}"
            nodes[node_label] = ((height-i-1),j)
            k+=1

    for j in range(0,width, 2):
         matrix[int(height/2)][j] = "●"
         row_label = chr(65 + int(height/2))
         node_label = f"{row_label}{j}"
         nodes[node_label] = (int(height/2),j)

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
        "DD": (1, 1),     # Dole desno
        "DL": (1, -1)      # Dole levo
    }

    if start not in nodes or direction not in directions:
        print("Nevalidan potez!")
        return

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
    else:
        print("Potez izlazi izvan granica ili prelazi nepostojeći čvor!")


def print_board(matrix):
    for row in matrix:
        print(" ".join(row))


# Main

side_length = int(input("Unesite dužinu stranice heksagona: "))
matrix, nodes = draw_hexagon(side_length)
print_board(matrix)
print(f"Širina matrice: {len(matrix[0])}")  # Broj kolona
print(f"Visina matrice: {len(matrix)}")
while True:
    print("\nČvorovi: ", ", ".join(nodes.keys()))
    move = input("Unesite potez (format: čvor direkcija, npr. A1 D): ").strip().upper()
    if move == "EXIT":
        break
    try:
        start, direction = move.split()
        play_move(matrix, nodes, start, direction)
        print_board(matrix)
    except ValueError:
        print("Unesite potez u ispravnom formatu!")