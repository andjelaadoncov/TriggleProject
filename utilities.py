#OVDE SE NALAZE POMOCNE FUNKCIJE
def max_connections(side_length):
    conn = 0
    for i in range(side_length, 2*side_length - 1):
        conn+=2*(i-1)+4*i
    conn+=2*(side_length-1)
    print(str(conn) + " Maksimalni broj konekcija je.")
    return conn