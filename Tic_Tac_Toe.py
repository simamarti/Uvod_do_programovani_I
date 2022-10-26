from turtle import down, forward, right, left, exitonclick, goto, speed, up, window_height, window_width

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

def Input():

    row = 0
    column = 0

    try:
        
        row = int(input("KOlik políček by měla mít hrací plocha na výšku: "))
        column = int(input("KOlik políček by měla mít hrací plocha na šířku: "))

    except ValueError:

        print("Měl jste vložit číslo.")

    except OverflowError:

        print("Číslo je příliš velké.")

    if row <= 0 or column <= 0:

        print("Číslo musí být kladné.")
        row = 0
        column = 0

    return (row, column)

def Centers(row, column):

    pass
row, column = Input()

draw(row, row)

exitonclick()
