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
    
    up()
    goto(0, 0)
    down()

def Input():

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

    return centers

def Game(centers, fill, r, c):

    for i in range(r*c):

        while(True):

            try:
                while(True):

                    string = input("Hraje hráč č. 1: ")
                    splitted = string.split(",")
                    print("<" + splitted[0] + ", " + splitted[1] + ">")
                    if int(splitted[0]) < 1 or int(splitted[0]) > r:

                        print(">> Číslo je příliš veliké, mříýka má " + str(r) + " řádků.")
                        continue   
                    print("<" + splitted[0] + ", " + splitted[1] + ">")
                    if int(splitted[1]) < 1 or int(splitted[1]) > c:

                        print(">> Číslo je příliš veliké, mříýka má " + str(c) + " řádků.")
                        continue  
                    print("<" + str(fill[int(splitted[0]) - 1][int(splitted[1]) - 1]) + ">")
                    if fill[int(splitted[0]) - 1][int(splitted[1]) - 1] == 0:

                        fill[int(splitted[0]) - 1][int(splitted[1]) - 1] = 1
                        
                        up()
                        goto(centers[int(splitted[0]) - 1][int(splitted[1]) - 1])
                        print("<" + str(centers[int(splitted[0]) - 1][int(splitted[1]) - 1]) + ">")
                        down()
                        print(">> Tah proveden")
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

                    string = input("Hraje hráč č. 1: ")
                    splitted = string.split(",")
                    print("<" + splitted[0] + ", " + splitted[1] + ">")
                    if int(splitted[0]) < 1 or int(splitted[0]) > r:

                        print(">> Číslo je příliš veliké, mříýka má " + str(r) + " řádků.")
                        continue   
                    print("<" + splitted[0] + ", " + splitted[1] + ">")
                    if int(splitted[1]) < 1 or int(splitted[1]) > c:

                        print(">> Číslo je příliš veliké, mříýka má " + str(c) + " řádků.")
                        continue  
                    print("<" + str(fill[int(splitted[0]) - 1][int(splitted[1]) - 1]) + ">")
                    if fill[int(splitted[0]) - 1][int(splitted[1]) - 1] == 0:

                        fill[int(splitted[0]) - 1][int(splitted[1]) - 1] = 1
                        
                        up()
                        goto(centers[int(splitted[0]) - 1][int(splitted[1]) - 1])
                        print("<" + str(centers[int(splitted[0]) - 1][int(splitted[1]) - 1]) + ">")
                        down()
                        print(">> Tah proveden")
                        circle(25)
                        break

                    else:
                        print(">> Pole je již obsazeno.")
                    
                break

            except:
                print("Špatný vstup")
        
        
row, column = Input()
centers = None

if row is not None:
    
    draw(row, column)
    centers = Centers(row, column)

    fill = [[0]*row]*column

    Game(centers, fill, row, column)


exitonclick()
