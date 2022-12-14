from sys import maxsize
from turtle import Screen, begin_fill, circle, color, down, fillcolor, forward, hideturtle, pos, right, left, exitonclick, goto, speed, title, up, width, window_height, window_width, write

EDGE = 50

def draw_Square():          # Funkce vykreslí čtverec o hraně 50 px, začíná nahoře vlevo
    forward(EDGE)
    right(90)
    forward(EDGE)
    right(90)
    forward(EDGE)
    right(90)
    forward(EDGE)
    right(90)

def draw(row, column):      # Funkce vykreslí čtvercovou síť o zadaných rozměrech
    speed(10)
    up()
    goto(-window_width()/2, window_height()/2)
    down()
    for i in range(row):
        for j in range(column):
            draw_Square()
            forward(EDGE)

        up()                    # Vykreslení číslování řádků
        forward(25)
        right(90)
        forward(25)
        write(str(i + 1))
        left(180)
        forward(25)
        left(90)
        forward(25)
        left(180)
        down()

        right(180)              # Z pozice vykreslování čísla otočení o 180° a přesun na spodní levý roh první buňky v řádku
        forward(EDGE*column)
        left(90)
        forward(EDGE)
        left(90)
    
    up()
    right(90)                   # Posun z levého spodního okraje první buňky na pozici vykreslení první  
    forward(25)
    left(90)
    forward(25)
    for i in range(column):     # Vykreslení číslování sloupců
        write(str(i +1))
        forward(EDGE)
    down()
    hideturtle()

def input_check(number):    # Funkce kontroluje, zda je zadaný řetězec číslo
    if number == "":
        print(">> Nebylo nic zadano")
        return False
    if is_Digit(number, 3, maxsize):
        return True
    return False

def query(string):          # Funkce žádá uživatele, aby zadal velikost hrací plochy
    while(True):
        expression = input(">> Kolik políček by měla mít hrací plocha na " + string + ", minimum jsou 3: ")
        if input_check(expression):
            number = int(expression)
            return number

def set_size():             # Funkce vrátí velikost hrací plochy
    return query("výšku"), query("šířku")

def centers(row, column):   # Funkce vypočítá středy spodní hrany jednotlivých buněk sítě
    centers = [[None]*column for i in range(row)]
    coord_x = -window_width()/2 + EDGE/2
    coord_y = window_height()/2 - EDGE
    for i in range(row):
        for j in range(column):
            centers[i][j] = (coord_x, coord_y)
            coord_x += EDGE
        coord_y -= EDGE
        coord_x = -window_width()/2 + EDGE/2
    return centers

def is_Digit(number, min, max, coord = None):   # Funkce kontroluje, zda je řetězec kladné přirozené číslo v příslušném intervalu
    if number.isdecimal():
        if int(number) >= min and int(number) <= max:
            return True
    if coord == None:           # Při vkládání velikosti pole 
        print(">> Špatný formát vstupu, šířka i výška hracího pole musí být kladné přirozené číslo v intervalu <" + str(min) + ", " + str(max) + ">. Zkuste to znovu.")
    else:                       # Při vkládání souřadnic bodu
        print(">> Špatný formát vstupu, číslo " + coord + " musí být kladné přirozené číslo v intervalu <" + str(min) + ", " + str(max) + ">. Zkuste to znovu.")
    return False 

def shift(player, centers, fill, row, column):  # Funkce se ptá uživatele na souřadnice a přesouvá želvu na příslušnou souřadnici
    while(True):
        coord_x = 0
        coord_y = 0
        string = input("Hraje hráč č. " + str(player) + ": ")
        splitted = string.split(",")
        if len(splitted) != 2:
            print(">> Špatný formát vstupu, zadejte souřadnice ve formátu \"x, y\".")
            continue
        if is_Digit(splitted[0], 0, row, coord = "řádku") and is_Digit(splitted[1], 0, column, coord = "sloupce"):
            coord_x = int(splitted[0]) - 1
            coord_y = int(splitted[1]) - 1
        else:
            continue
        if fill[coord_x][coord_y] == 0:
            fill[coord_x][coord_y] = player
            break
        print(">> Políčko je již obsazeno.")
    up()
    goto(centers[coord_x][coord_y])
    down()
    last = (coord_x, coord_y)
    return fill, last

def sign(player):   # Funkce vykreslí značku příslušného hráče (0 - červené kolečko, 1 - modrý křížek)
    if player == 1:
        color("red")
        begin_fill()
        circle(EDGE/2)
    else:
        color("blue")
        begin_fill()
        up()
        goto(pos()[0], pos()[1] + EDGE/2)
        down()
        goto(pos()[0] + EDGE/2, pos()[1] + EDGE/2)
        goto(pos()[0] - EDGE, pos()[1] - EDGE)
        goto(pos()[0] + EDGE/2, pos()[1] + EDGE/2)
        goto(pos()[0] - EDGE/2, pos()[1] + EDGE/2)
        goto(pos()[0] + EDGE, pos()[1] - EDGE)

def lenght_row(row, column):    # Funkce spočítá délku vítězné linie
    tmp = min(row, column)
    if tmp > 5:
        return 5
    return tmp

def win_row_check(player, direction, fill, centers, last, row, column):     # Funkce hledá spojnici znaků a vykreslí ji
    lenght = lenght_row(row, column)
    if direction == 1:            # Posun v 2D poli pro kontrolu vítězství, např. direction == 4: [2][1] -> [1][2]
        move = (1, 0)
    elif direction == 2:
        move = (0, 1)
    elif direction == 3:
        move = (1, 1)
    else:
        move = (-1, 1)
    most_left = last
    most_right = last
    coord_x = last[0]
    coord_y = last[1]
    counter = 1
    while (coord_x + move[0]) < row and (coord_x + move[0]) >= 0 and (coord_y + move[1]) < column and (coord_y + move[1]) >= 0 and fill[coord_x + move[0]][coord_y + move[1]] == player:
        counter += 1
        coord_x += move[0]
        coord_y += move[1]
        most_right = (coord_x, coord_y)
        if counter == lenght:
            draw_line(centers, most_left, most_right)
            return True
    coord_x = last[0]
    coord_y = last[1]
    move = tuple((-1)* elem for elem in move)
    while (coord_x + move[0]) < row and (coord_x + move[0]) >= 0 and (coord_y + move[1]) < column and (coord_y + move[1]) >= 0 and fill[coord_x + move[0]][coord_y + move[1]] == player:
        counter += 1
        coord_x += move[0]
        coord_y += move[1]
        most_left = (coord_x, coord_y)
        if counter == lenght:
            draw_line(centers, most_left, most_right)
            return True
    return False

def win_check(player, fill, centers, last, row, column):    # Funkce kontroluje zda hráč, který je na řadě vyhrál, pokud ano vykreslí spojnici daných bodů
    if win_row_check(player, 1, fill, centers, last, row, column):
        return True
    if win_row_check(player, 2, fill, centers, last, row, column):
        return True
    if win_row_check(player, 3, fill, centers,  last, row, column):
        return True
    if win_row_check(player, 4, fill, centers, last, row, column):
        return True
    return False

def draw_line(centers, most_left, most_right):      # Funkce vykresluje čáru spojující vítězné znaky
    width(6)
    color("black")
    fillcolor()
    up()
    goto(centers[most_left[0]][most_left[1]][0], centers[most_left[0]][most_left[1]][1] + EDGE/2)
    down()
    goto(centers[most_right[0]][most_right[1]][0], centers[most_right[0]][most_right[1]][1] + EDGE/2)

def message(text):  # Funkce na konci hry zobrazí text, kdo vyhrál
    up()
    goto(0, 0)
    fillcolor("red")
    down()
    begin_fill()
    write(text, font = ("Arial", 20, "normal"))   

def game(centers, fill, row, column):   # Funkce se na střídačku ptát jednotlivých hráčů na souřadnice a zakresluje je do sítě
    up()
    goto(0, 0)
    down()
    width(4)
    player = 1
    move = 1
    print(">> Zadávejte souřadnice ve formátu \"<číslo řádku>,<číslo sloupce>\". Např. \"2,1\" (řádek číslo 2 a sloupec číslo 1).")
    while move <= row*column:
        if player == 1:
            fill, last = shift(player, centers, fill, row, column)
            sign(player)
            if win_check(player, fill, centers, last, row, column):
                message("Hráč 1 vyhrál")
                print(">> Hráč 1 vyhrál.")
                break
            player = 2
            move += 1
        else:
            fill, last = shift(player, centers, fill, row, column)
            sign(player)
            if win_check(player, fill, centers, last, row, column):
                message("Hráč 2 vyhrál")
                print(">> Hráč 2 vyhrál.")
                break
            player = 1
            move += 1
    if move > row*column:
        message("Remíza")
        print(">> Remíza")
    print("Hra skončila.")

row, column = set_size()
lenght = lenght_row(row, column)
print(">> Vyhraje hráč, který dříve vytvoří nepřerušenou řadu svých značek dlouhou " + str(lenght) + " znaky.\n")
cell_ceenters = None
title("Piškvorky")
Screen()
cell_centers = centers(row, column)
draw(row, column)
fill = [[0]*row for i in range(column)]  
game(cell_centers, fill, row, column)
exitonclick()
