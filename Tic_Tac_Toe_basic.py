from sys import maxsize
from turtle import begin_fill, circle, color, down, fillcolor, forward, hideturtle, pos, right, left, exitonclick, goto, speed, title, up, width, window_height, window_width, write

def draw_Square():

    forward(50)
    right(90)
    forward(50)
    right(90)
    forward(50)
    right(90)
    forward(50)
    right(90)

def draw(row, column):

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
 

    if number == "":

        print(">> Nebylo nic zadano")
        return False

    if is_Digit(number, maxsize):
            
        return True
    
    return False

def query(string):

    while(True):

        expression = input(">> Kolik políček by měla mít hrací plocha na " + string + ": ")

        if input_check(expression):

            number = int(expression)
            return number

def set_size():

    return query("výšku"), query("šířku")

def centers(row, column):

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

    if number.isdecimal():
        
        if int(number) > 0 and int(number) <= limit:

            return True
        
    print(">> Špatný formát vstupu, souřadnice musí být kladné přirozené číslo v intervalu <0, " + str(limit) + ">. Zkuste to znovu.")
    return False 
 
def shift(player, centers, fill, row, column):

    while(True):

        coord_x = 0
        coord_y = 0

        string = input("Hraje hráč č. " + str(player) + ": ")
        splitted = string.split(",")

        if len(splitted) != 2:

            print(">> Špatný formát vstupu, zadejte souřadnice ve formátu \"x, y\".")
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

            print(">> Políčko je již obsazeno.")
            continue

    up()
    goto(centers[coord_x][coord_y])
    down()
    last = (coord_x, coord_y)

    return fill, last

def sign(player):

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

def lenght_row(row, column):

    tmp = min(row, column)
    
    if tmp > 5:
        
        return 5

    return tmp

def message(text):

    up()
    goto(0, 0)
    write(text, font = ("Arial", 20, "normal"))
    down()

def game(centers, fill, row, column):

    up()
    goto(0, 0)
    down()

    width(4)

    player = 1
    move = 1
    print(">> Zadávejte souřadnice ve formátu číslo řádku, číslo sloupce. Např. \"2,1\" (řádek číslo 2 a sloupec číslo 1).")

    while move <= row*column:
  
        if player == 1:

            fill, last = shift(player, centers, fill, row, column)
            sign(player)

            player = 2
            move += 1

        else:

            fill, last = shift(player, centers, fill, row, column)
            sign(player)

            player = 1
            move += 1
    
    print(">> Hra skončila.")

row, column = set_size()

lenght = lenght_row(row, column)

print(">> Vyhraje hráč, který dříve vytvoří nepřerušenou řadu svých značek dlouhou " + str(lenght) + " znaků.\n")
cell_centers = None
title("Piškvorky")

draw(row, column)
cell_centers = centers(row, column)

fill = [[0]*row for i in range(column)]
    
game(cell_centers, fill, row, column)

exitonclick()
