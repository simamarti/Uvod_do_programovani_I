import tkinter

class Point:
    def __init__(self, x : float, y : float) -> None:
        self.__x = x
        self.__y = y
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    def __eq__(self, o: object) -> bool:
        if o.x == self.x and o.y == self.y:
            return True
        return False

class Edge:
    def __init__(self, point_1 : Point, point_2 : Point):
        pass

class Rect:
    def __init__(self, point : Point, height : float, width : float) -> None:
        self.__vertices = [ point, 
                            Point(point.x, point.y + height),
                            Point(point.x + width, point.y + height),
                            Point(point.x + width, point.y),]
        self.__edges = [Edge(self.__vertices[0], self.__vertices[1]),
                        Edge(self.__vertices[1], self.__vertices[2]),
                        Edge(self.__vertices[2], self.__vertices[3]),
                        Edge(self.__vertices[3], self.__vertices[0])]
    def collision(self, other : object) -> bool:
        pass
p_1 = Point(0, 0)
p_2 = Point(1, 1)
w = 10
h = 5
rect_1 = Rect(p_1, h, w)  
rect_2 = Rect(p_2, h, w)        
print(rect_1.collision(rect_2))

