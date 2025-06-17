#OVDE SE NALAZE POMOCNE FUNKCIJE
def max_connections(side_length):
    conn = 0
    for i in range(side_length, 2*side_length - 1):
        conn+=2*(i-1)+4*i
    conn+=2*(side_length-1)
#    print(str(conn) + " Maksimalni broj konekcija")
    return conn

def get_depth_based_on_board_size(side_length):
    if side_length in [4, 5]:
        return 3
    elif side_length in [6, 7, 8]:
        return 2
    else:
        return 1
