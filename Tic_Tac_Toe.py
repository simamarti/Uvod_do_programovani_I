from curses import window
from turtle import forward, right, left, exitonclick, setpos, setposition, speed, window_height, window_width

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

    if (row <= 0 OR column <= 0)

        print("Číslo musí být kladné.")

    return (row, column)

draw(row, row)

exitonclick()
