# Modelos das primitivas graficas

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Representacao em coordenadas homogeneas
    def to_matrix(self):
        return [self.x, self.y, 1]

    def from_matrix(self, matrix):
        self.x = matrix[0]
        self.y = matrix[1]

class Reta:
    def __init__(self, p1, p2, algoritmo="BRESENHAM"):
        self.p1 = p1  # ponto inicial
        self.p2 = p2  # ponto final
        self.algoritmo = algoritmo  # DDA ou BRESENHAM

class Poligono:
    def __init__(self, pontos):
        self.pontos = pontos  # lista de vertices

class Circunferencia:
    def __init__(self, centro, raio):
        self.centro = centro
        self.raio = raio
