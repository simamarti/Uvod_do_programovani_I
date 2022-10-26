from turtle import circle, down, forward, right, left, exitonclick, goto, speed, up, window_height, window_width

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

    goto(0, 0)

def Input():

    row = None
    column = None

    try:
        
        row = int(input("KOlik políček by měla mít hrací plocha na výšku: "))

        if row <= 0:

            print("Číslo musí být kladné.")
            return (None, None)

        column = int(input("KOlik políček by měla mít hrací plocha na šířku: "))

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

def Centers(row, column):

    centers = [[None]*row]*column

    coord_x = -window_width()/2 + 25
    coord_y = window_height()/2 - 25

    for i in range(row):

        for j in range(column):

            centers[i][j] = (coord_x, coord_y)
            coord_x += 50
            
        coord_y -= 50
        coord_x = -window_width()/2 + 25

row, column = Input()

if row is not None:
    
    draw(row, column)
    centers = Centers(row, column)




exitonclick()
