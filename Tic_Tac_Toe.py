from sys import maxsize
from turtle import begin_fill, circle, color, down, fillcolor, forward, hideturtle, pos, right, left, exitonclick, goto, speed, title, up, width, window_height, window_width

def draw_Square():

    '''
        Funkce vykreslí čtverec o hraně 50 px
        Vykreslování začína vlevo nahoře
        Vstupní parametry: žádně
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
        
        right(180)
        forward(50*column)
        left(90)
        forward(50)
        left(90)
    
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
        Vstupní parametry: žádně
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
            player: hodnota 0, 1
                0 - červený kroužek (začíná)
                1 - modrý křážek
            centers (2D pole se souřadnicemi středů spodních hran buněk)
            fill (2D pole se informacemi o obsazenosti buněk)
                0 - volno
                1 - obsazeno
            row (počet řádků sítě)
            column (počet sloupců sítě)
        Návratová hodnota:
            fill - aktualizované 2D pole obsazenosti
    '''

    while(True):

        coord_x = 0
        coord_y = 0

        string = input("Hraje hráč č. " + str(player + 1) + ": ")
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

            fill[coord_x][coord_y] = 1
            break
            
        else:

            print("Políčko je již obsazeno.")
            continue

    up()
    goto(centers[coord_x][coord_y])
    down()

    return fill

def sign(player):

    '''
        Funkce vykreslí značku příslušného hráče (0 - červené kolečko, 1 - modrý křížek)
        Vstupní parametry:
            player: hodnota 0, 1
                0 - červený kroužek (začíná)
                1 - modrý křážek
        Návratová hodnota: žádná
    '''

    if player == 0:

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

def game(centers, fill, row, column):

    '''
        Funkce se nastřídačku ptát jednotlivých hráčů na souřadnice a zakresluje je do sítě
        Vstupní parametry:
            centers (2D pole se souřadnicemi středů spodních hran buněk)
            fill (2D pole se informacemi o obsazenosti buněk)
                0 - volno
                1 - obsazeno
            row (počet řádků sítě)
            column (počet sloupců sítě)
        Návratová hodnota: žádná
    '''

    up()
    goto(0, 0)
    down()

    width(4)

    player = 0
    move = 1
    print("Zadávejte souřadnice ve formátu číslo řádku, číslo sloupce. Např. \"2,1\" (řádek číslo 2 a sloupec číslo 1).\n")
    while move <= row*column:
  
        if player == 0:

            fill = shift(player, centers, fill, row, column)
            sign(player)

            player = 1
            move += 1

        else:

            fill = shift(player, centers, fill, row, column)
            sign(player)

            player = 0
            move += 1

    print("Hra skončila.")

row, column = set_size()
cell_centers = None
title("Piškvorky")

draw(row, column)
cell_centers = centers(row, column)

fill = [[0]*row for i in range(column)]
    
game(cell_centers, fill, row, column)

exitonclick()
