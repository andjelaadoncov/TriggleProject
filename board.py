#OVDE SE NALAZE SVE FUNKCIJE ZA RAD SA TABLOM
from collections import OrderedDict

def parse_matrix(matrix_str):
    rows = matrix_str.split("\n")
    matrix = [list(row) for row in rows]
    side_length = matrix_str[0].count("●")
    height = 3 * (2 * side_length - 2) + 1
    width = 6 * (2 * side_length - 2) + 1
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
    # ukupna visina matrice (gornji deo + donji deo - 1, jer sredina se ponavlja)

    height = 3*(2*side_length-2)+1
    width = 6*(2*side_length-2)+1


    matrix = [[" " for _ in range(width)] for _ in range(height)]


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

def print_board(matrix,y):
    first_row = [" "] * (y + 1)
    col_num = 1
    for i in range(y + 2, y+2+len(matrix[0])):
        if (i - (y + 2)) % 6 == 0:
            first_row.append(str(col_num))
            col_num += 1
        else:
            first_row.append(" ")

    print("  " + "".join(first_row))

    for index, row in enumerate(matrix):
        row = [str(cell) for cell in row]

        if index % 3 == 0:
            print(chr(65 + index // 3) + " " + "".join(row))
        else:
            print("  " + "".join(row))
    last_row = [" "] * (y + 1)
    col_num = 1
    for i in range(y + 2, y + 2 + len(matrix[0])):
        if (i - (y + 2)) % 6 == 0:
            last_row.append(str(col_num))
            col_num += 1
        else:
            last_row.append(" ")

    print("  " + "".join(last_row))