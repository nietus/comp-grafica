def dda(x1, y1, x2, y2):
    pontos = []
    dx = x2 - x1
    dy = y2 - y1

    passos = abs(dx) if abs(dx) >= abs(dy) else abs(dy)
    if passos == 0:
        return [(round(x1), round(y1))]

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


def bresenham_reta(x1, y1, x2, y2):
    pontos = []

    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))

    dx = x2 - x1
    dy = y2 - y1

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
        p = 2 * dy - dx
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


def bresenham_circulo(xc, yc, raio):
    pontos = set()

    xc = int(round(xc))
    yc = int(round(yc))
    r = int(round(raio))

    x = 0
    y = r
    p = 3 - (2 * r)

    for pt in _simetria_octantes(xc, yc, x, y):
        pontos.add(pt)

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
