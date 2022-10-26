from turtle import forward, right, left, exitonclick

def draw_Square(edge = 50):      # Začíná nahoře vlevo
    
    forward(edge)
    right(90)
    forward(edge)
    right(90)
    forward(edge)
    right(90)
    forward(edge)
    right(90)

def draw(row, column):

   for i in range(row):

        for j in range(column):

            draw_Square()
            forward()




draw(3, 3)

exitonclick()