class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_matrix(self):
        return [self.x, self.y, 1]

    def from_matrix(self, matrix):
        self.x = matrix[0]
        self.y = matrix[1]

class Reta:
    def __init__(self, p1, p2, algoritmo="BRESENHAM"):
        self.p1 = p1
        self.p2 = p2
        self.algoritmo = algoritmo

class Poligono:
    def __init__(self, pontos):
        self.pontos = pontos

class Circunferencia:
    def __init__(self, centro, raio):
        self.centro = centro
        self.raio = raio
