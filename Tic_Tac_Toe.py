from turtle import begin_fill, circle, color, down, fillcolor, forward, hideturtle, pos, right, left, exitonclick, goto, speed, up, width, window_height, window_width

def draw_Square():      # Začíná nahoře vlevo
    
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
        
        right(180)
        forward(50*column)
        left(90)
        forward(50)
        left(90)
    
    hideturtle()

def input():

    row = None
    column = None

    try:
        
        number = input("Kolik políček by měla mít hrací plocha na výšku: ")

        if number == "":

            print("Nebylo nic zadano")
            return (None, None)

        row = int(number)

        if row <= 0:

            print("Číslo musí být kladné.")
            return (None, None)

        number = ""
        number = input("KOlik políček by měla mít hrací plocha na šířku: ")

        if number == "":

            print("Nebylo nic zadano")
            return (None, None)

        column = int(number)

        if column <= 0:

            print("Číslo musí být kladné.")
            return (None, None)

    except ValueError:

        print("Měl jste vložit číslo.")
        return (None, None)

    except OverflowError:

        print("Číslo je příliš velké.")
        return (None, None)

    return (row, column)

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

def move(player):   # dotaz (cyklus), posun

    while(True):

        coord_x = 0
        coord_y = 0
        check = 0

        string = input("Hraje hráč č. " + str(player) + ": ")
        splitted = string.split(",")

        if splitted[0].isdigit():

            if int(splitted[0]) < 1 or int(splitted[0]) > row:
                
                coord_x = int(splitted[0]) - 1
                check += 1

        if splitted[1].isdigit():

            if int(splitted[1]) < 1 or int(splitted[1]) > column:
                
                coord_x = int(splitted[1]) - 1
                check += 1

        if check == 2:

            return 

    
    up()
    goto(centers[coord_x][coord_y])
    down()

def sign(player):

    if player == 1:

        color("red", "red")
        begin_fill()
        circle(25)
    
    else:

        color("blue", "blue")
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

    up()
    goto(0, 0)
    down()

    width(4)

    player = 0
    move = 1

    while move <= row*column:

        if player == 0:

            move(player)
            sign(player)

            player = 1
            move += 1

        else:

            move(player)
            sign(player)

            player = 0
            move += 1


 '''   for i in range(r*c):

        while(True):

            try:
                while(True):

                    string = input("Hraje hráč č. 1: ")
                    splitted = string.split(",")

                    if int(splitted[0]) < 1 or int(splitted[0]) > r:

                        continue   

                    if int(splitted[1]) < 1 or int(splitted[1]) > c:

                        continue  

                    
                    if fill[int(splitted[0]) - 1][int(splitted[1]) - 1] == 0:

                        fill[int(splitted[0]) - 1][int(splitted[1]) - 1] = 1
                        
                        up()
                        goto(centers[int(splitted[0]) - 1][int(splitted[1]) - 1])
                        down()

                        color("red", "red")
                        begin_fill()
                        circle(25)

                        break

                    else:
                        print(">> Pole je již obsazeno.")
                    
                break

            except:
                print("Špatný vstup")
 
        while(True):

            try:
                while(True):

                    string = input("Hraje hráč č. 2: ")
                    splitted = string.split(",")

                    if int(splitted[0]) < 1 or int(splitted[0]) > r:

                        continue   

                    if int(splitted[1]) < 1 or int(splitted[1]) > c:

                        continue  

                    
                    if fill[int(splitted[0]) - 1][int(splitted[1]) - 1] == 0:

                        fill[int(splitted[0]) - 1][int(splitted[1]) - 1] = 1
                        
                        up()
                        goto(centers[int(splitted[0]) - 1][int(splitted[1]) - 1])
                        down()

                        color("blue", "blue")
                        begin_fill()
                        up()
                        goto(pos()[0], pos()[1] + 25)
                        down()
                        goto(pos()[0] + 25, pos()[1] + 25)
                        goto(pos()[0] - 50, pos()[1] - 50)
                        goto(pos()[0] + 25, pos()[1] + 25)
                        goto(pos()[0] - 25, pos()[1] + 25)
                        goto(pos()[0] + 50, pos()[1] - 50)

                        break

                    else:
                        print(">> Pole je již obsazeno.")
                    
                break

            except:
                print("Špatný vstup")
'''
row, column = input()
centers = None

if row is not None:
    
    draw(row, column)
    centers = Centers(row, column)

    fill = [[0]*row for i in range(column)]
    
    game(centers, fill, row, column)


exitonclick()
