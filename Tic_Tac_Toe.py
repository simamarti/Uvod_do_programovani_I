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

def set_size():

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
        number = input("Kolik políček by měla mít hrací plocha na šířku: ")

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

def is_Digit(number):

    if number.isdigit():

            if int(number) < 1 or int(number) > row:

                return True
        
    print("Špatný formát vstupu, zkuste to znovu.")
    return False 

def shift(player):   # dotaz (cyklus), posun

    while(True):

        coord_x = 0
        coord_y = 0
        check = 0

        string = input("Hraje hráč č. " + str(player + 1) + ": ")
        splitted = string.split(",")
        print("<<" + str(splitted[0]) + "," + str(splitted[1]) + ">>")
        if is_Digit(splitted[0]):
            
            coord_x = int(splitted[0]) - 1
            check += 1
            continue

        if is_Digit(splitted[1]):
                
            coord_x = int(splitted[1]) - 1
            check += 1
            continue

        if check == 2:

            break

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

            shift(player)
            sign(player)

            player = 1
            move += 1

        else:

            shift(player)
            sign(player)

            player = 0
            move += 1

row, column = set_size()
cell_centers = None

if row is not None:
    
    draw(row, column)
    cell_centers = centers(row, column)

    fill = [[0]*row for i in range(column)]
    
    game(cell_centers, fill, row, column)


exitonclick()
