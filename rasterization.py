# Algoritmos de rasterizacao de retas e circunferencias


# Rasterizacao de reta pelo algoritmo DDA
def dda(x1, y1, x2, y2):
    pontos = []
    dx = x2 - x1
    dy = y2 - y1

    # Usa o maior delta como numero de passos
    passos = abs(dx) if abs(dx) >= abs(dy) else abs(dy)
    if passos == 0:
        return [(round(x1), round(y1))]

    # Incremento por passo em cada eixo
    x_incr = dx / passos
    y_incr = dy / passos
    x = x1
    y = y1
    pontos.append((round(x), round(y)))

    for _ in range(int(passos)):
        x += x_incr
        y += y_incr
        pontos.append((round(x), round(y)))

    return pontos


# Rasterizacao de reta pelo algoritmo de Bresenham (usa apenas inteiros)
def bresenham_reta(x1, y1, x2, y2):
    pontos = []

    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))

    dx = x2 - x1
    dy = y2 - y1

    # Determina a direcao do incremento em cada eixo
    if dx >= 0:
        incrx = 1
    else:
        incrx = -1
        dx = -dx

    if dy >= 0:
        incry = 1
    else:
        incry = -1
        dy = -dy

    x = x1
    y = y1
    pontos.append((x, y))

    if dy < dx:
        # Caso onde X eh o eixo de maior variacao
        p = 2 * dy - dx  # variavel de decisao
        const1 = 2 * dy
        const2 = 2 * (dy - dx)
        for _ in range(dx):
            x += incrx
            if p < 0:
                p += const1
            else:
                y += incry
                p += const2
            pontos.append((x, y))
    else:
        # Caso onde Y eh o eixo de maior variacao
        p = 2 * dx - dy
        const1 = 2 * dx
        const2 = 2 * (dx - dy)
        for _ in range(dy):
            y += incry
            if p < 0:
                p += const1
            else:
                x += incrx
                p += const2
            pontos.append((x, y))

    return pontos


# Espelha um ponto nos 8 octantes da circunferencia
def _simetria_octantes(xc, yc, x, y):
    return [
        (xc + x, yc + y),
        (xc - x, yc + y),
        (xc + x, yc - y),
        (xc - x, yc - y),
        (xc + y, yc + x),
        (xc - y, yc + x),
        (xc + y, yc - x),
        (xc - y, yc - x),
    ]


# Rasterizacao de circunferencia pelo algoritmo de Bresenham
def bresenham_circulo(xc, yc, raio):
    pontos = set()  # set evita pontos duplicados da simetria

    xc = int(round(xc))
    yc = int(round(yc))
    r = int(round(raio))

    x = 0
    y = r
    p = 3 - (2 * r)  # variavel de decisao inicial

    for pt in _simetria_octantes(xc, yc, x, y):
        pontos.add(pt)

    # Calcula apenas 1/8 da circunferencia e espelha o restante
    while x < y:
        if p < 0:
            p = p + (4 * x) + 6
        else:
            p = p + (4 * (x - y)) + 10
            y -= 1
        x += 1
        for pt in _simetria_octantes(xc, yc, x, y):
            pontos.add(pt)

    return list(pontos)
