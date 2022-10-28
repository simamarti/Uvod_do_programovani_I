from sys import maxsize
from turtle import begin_fill, circle, color, down, fillcolor, forward, hideturtle, pos, right, left, exitonclick, goto, speed, title, up, width, window_height, window_width, write

def draw_Square():

    '''
        Funkce vykreslí čtverec o hraně 50 px
        Vykreslování začína vlevo nahoře
        Vstupní parametry: žádné
        Návratová hodnota: žádná
    '''
    forward(50)
    right(90)
    forward(50)
    right(90)
    forward(50)
    right(90)
    forward(50)
    right(90)

def draw(row, column):

    '''
        Funkce vykreslí čtvercovou síť o zadaných rozměrech
        Vykreslování začína vlevo nahoře
        Vstupní parametry:
            row (počet řádků v síti)
            column (počet sloupců v síti)
        Návratová hodnota: žádná
    '''

    speed(10)

    up()
    goto(-window_width()/2, window_height()/2)
    down()

    for i in range(row):

        for j in range(column):

            draw_Square()
            forward(50)
        
        up()
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

        right(180)
        forward(50*column)
        left(90)
        forward(50)
        left(90)
    
    up()
    right(90)
    forward(25)
    left(90)
    forward(25)

    for i in range(column):

        write(str(i +1))
        forward(50)
    down()

    hideturtle()

def input_check(number):
 
    '''
        Funkce kontroluje, zda je zadaný řetězec číslo
        Vstupní parametry:
            nummber (řetězec)
        Návratová hodnota: bool
            True - řetězec je číslo
            False - řetězec není číslo
    '''

    if number == "":

        print("Nebylo nic zadano")
        return False

    if is_Digit(number, maxsize):
            
        return True
    
    return False

def query(string):

    '''
        Funkce žádá uživatele aby zadal velikost hrací plochy
        Vstupní parametry:
            string (řetězec)
        Návratová hodnota:
            number (Integer)

    '''
    while(True):

        expression = input("Kolik políček by měla mít hrací plocha na " + string + ": ")

        if input_check(expression):

            number = int(expression)
            return number

def set_size():

    '''
        Funkce vrátí velikost hrací plochy
        Vstupní parametry: žádné
        Návratová hodnota:
            tuple - výška a šířka hracího pole
    '''

    return query("výšku"), query("šířku")

def centers(row, column):

    '''
        Funkce vypočítá středy spodní hrany jednotlivých políček
        Vstupní parametry:
            row (počet políček sítě na výšku)
            column (počet políček na šířku)
        Návratová hodnota:
            2D pole se soiřadnicemi bodů (tuple)
    '''

    centers = [[None]*row for i in range(column)]

    coord_x = -window_width()/2 + 25
    coord_y = window_height()/2 - 50

    for i in range(row):

        for j in range(column):

            centers[i][j] = (coord_x, coord_y)
            coord_x += 50
            
        coord_y -= 50
        coord_x = -window_width()/2 + 25

    return centers

def is_Digit(number, limit):

    '''
        Funkce kontroluje je řetězec kladné přirozené číslo v příslučném intervalu
        Vstupní parametry:
            number (řetězec)
            limit (maximální hodnota, které může číslo mabývat - rozměry sítě/interní maximální velikost proměnné)
        Návratová hodnota: bool
            True - řetězec je číslo
            False - řetězec není číslo
    '''

    if number.isdecimal():
        
        if int(number) <= limit:

            return True
        
    print("Špatný formát vstupu, vstup musí být kladné přirozené číslo v intervalu <0, " + str(limit) + ">. Zkuste to znovu.")
    return False 
 
def shift(player, centers, fill, row, column):

    '''
        Funkce se ptá uživatele na souřadnice a přesouvá želvu na příslušnou souřadnici
        Vstupní parametry:
            player: hodnota 1, 2
                1 - červený kroužek (začíná)
                2 - modrý křážek
            centers (2D pole se souřadnicemi středů spodních hran buněk)
            fill (2D pole se informacemi o obsazenosti buněk)
                0 - volno
                1 - hráč č. 1
                2 - hráč č. 2
            row (počet řádků sítě)
            column (počet sloupců sítě)
        Návratová hodnota:
            fill - aktualizované 2D pole obsazenosti
    '''

    while(True):

        coord_x = 0
        coord_y = 0

        string = input("Hraje hráč č. " + str(player) + ": ")
        splitted = string.split(",")

        if len(splitted) != 2:

            print("Špatný formát vstupu, zadejte souřadnice ve formátu \"x, y\".")
            continue

        if is_Digit(splitted[0], row) and is_Digit(splitted[1], column):
            
            coord_x = int(splitted[0]) - 1
            coord_y = int(splitted[1]) - 1
        
        else:

            continue
        
        if fill[coord_x][coord_y] == 0:

            fill[coord_x][coord_y] = player
            break
            
        else:

            print("Políčko je již obsazeno.")
            continue

    up()
    goto(centers[coord_x][coord_y])
    down()
    last = (coord_x, coord_y)

    return fill, last

def sign(player):

    '''
        Funkce vykreslí značku příslušného hráče (0 - červené kolečko, 1 - modrý křížek)
        Vstupní parametry:
            player: hodnota 1, 2
                1 - červený kroužek (začíná)
                2 - modrý křážek
        Návratová hodnota: žádná
    '''

    if player == 1:

        color("red")
        begin_fill()
        circle(25)
    
    else:

        color("blue")
        begin_fill()
        up()
        goto(pos()[0], pos()[1] + 25)
        down()
        goto(pos()[0] + 25, pos()[1] + 25)
        goto(pos()[0] - 50, pos()[1] - 50)
        goto(pos()[0] + 25, pos()[1] + 25)
        goto(pos()[0] - 25, pos()[1] + 25)
        goto(pos()[0] + 50, pos()[1] - 50)

def win_row_check(player, direction, fill, centers, last, row, column):

    '''
        Funkce hledá spojnici znaků a vykreslí ji
        Vstupní parametry:
            player: hodnota 1, 2
                1 - červený kroužek (začíná)
                2 - modrý křážek
            direction
                1 - vodorovně
                2 - svisle
                3 - z pravo nahoře vlevo douu
                4 - z leva nahoře pravo dolu
            fill (2D pole se informacemi o obsazenosti buněk)
                0 - volno
                1 - obsazeno
            centers (2D pole se souřadnicemi středů spodních hran buněk)
            last - souřadnice naposled zadaného znaku
            row (počet řádků sítě)
            column (počet sloupců sítě)
        Návratová hodnota: bool
            0 - hráč vyhrál
            1 - hráč nevyhrál
    '''

    lenght = min(row, column)

    if lenght > 5:

        length = 5
    
    match direction:

        case 1:
            move = (1, 0)
        case 2:       
            move = (0, 1)
        case 3:
            move = (1, 1)
        case 4:
            move = (-1, 1)
    
    most_left = last
    most_right = last

    for i in range(lenght):
        
        coord_x = last[0]
        coord_y = last[1]
        counter = 1

        while coord_x + move[0] < row and coord_y + move[1] < column and fill[coord_x + move[0]][coord_y + move[1]] == player:

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

        while coord_x + move[0] < row and coord_y + move[1] < column and fill[coord_x + move[0]][coord_y + move[1]] == player:

            counter += 1
            coord_x += move[0]
            coord_y += move[1]
            most_left = (coord_x, coord_y)

            if counter == lenght:

                draw_line(centers, most_left, most_right)
                return True

        return False

def win_check(player, fill, centers, last, row, column):
    
    '''
        Funkce kontroluje zda hráč, který je na řadě vyhrál, pokud ano vykreslí spojici daných bodů
        Vstupní parametry:
            player: hodnota 1, 2
                1 - červený kroužek (začíná)
                2 - modrý křážek
            fill (2D pole se informacemi o obsazenosti buněk)
                0 - volno
                1 - hráč č. 1
                2 - hráč č. 2
            centers (2D pole se souřadnicemi středů spodních hran buněk)
            last - souřadnice naposled zadaného znaku
            row (počet řádků sítě)
            column (počet sloupců sítě)
        Návratová hodnota: bool
            0 - hráč vyhrál
            1 - hráč nevyhrál
    '''

    if win_row_check(player, 1, fill, centers, last, row, column):
        
        return True

    if win_row_check(player, 2, fill, centers, last, row, column):
        
        return True
    
    if win_row_check(player, 3, fill, centers,  last, row, column):
        
        return True

    if win_row_check(player, 4, fill, centers, last, row, column):
        
        return True
    
    return False

def draw_line(centers, most_left, most_right):

    '''
        Funkce vykresluje čáru spojující vítězné znaky
        Vstupní parametry:
            centers (2D pole se souřadnicemi středů spodních hran buněk)
            most_left (souřadnice body nejvíce nahoře)
            most_right (souřadnice bodu nejvíce dole)
        Návratová hodnota: žádná
    '''

    width(6)
    color("black")
    fillcolor()

    up()
    goto(centers[most_left[0]][most_left[1]][0], centers[most_left[0]][most_left[1]][1] + 25)
    down()
    goto(centers[most_right[0]][most_right[1]][0], centers[most_right[0]][most_right[1]][1] + 25)

def message(text):

    up()
    goto(0, 0)
    write(text, font = ("Arial", 20, "normal"))
    down()

def game(centers, fill, row, column):

    '''
        Funkce se nastřídačku ptát jednotlivých hráčů na souřadnice a zakresluje je do sítě
        Vstupní parametry:
            centers (2D pole se souřadnicemi středů spodních hran buněk)
            fill (2D pole se informacemi o obsazenosti buněk)
                0 - volno
                1 - hráč č. 1
                2 - hráč č. 2
            row (počet řádků sítě)
            column (počet sloupců sítě)
        Návratová hodnota: žádná
    '''

    up()
    goto(0, 0)
    down()

    width(4)

    player = 1
    move = 1
    print("Zadávejte souřadnice ve formátu číslo řádku, číslo sloupce. Např. \"2,1\" (řádek číslo 2 a sloupec číslo 1).")

    while move <= row*column:
  
        if player == 1:

            fill, last = shift(player, centers, fill, row, column)
            sign(player)

            if win_check(player, fill, centers, last, row, column):

                message("Hráč 1 vyhrál")

                print("Hráč 1 vyhrál.")
                break

            player = 2
            move += 1

        else:

            fill, last = shift(player, centers, fill, row, column)
            sign(player)
            
            if win_check(player, fill, centers, last, row, column):
                
                message("Hráč 2 vyhrál")

                print("Hráč 2 vyhrál.")
                break

            player = 1
            move += 1
    
    if move > row*column:

        message("Remíza")
        
        print("Remíza")

    print("Hra skončila.")

row, column = set_size()

lenght = min(row, column)

if lenght > 5:

    length = 5

print("Vyhraje hráč, který dříve vytvoří nepřerušenou řadu svých značek dlouhou " + str(lenght) + " znaků.\n")
cell_centers = None
title("Piškvorky")

draw(row, column)
cell_centers = centers(row, column)

fill = [[0]*row for i in range(column)]
    
game(cell_centers, fill, row, column)

exitonclick()
