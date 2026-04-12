import math


def translacao_raw(x, y, dx, dy):
    return x + dx, y + dy


def rotacao_raw(x, y, angulo_graus, cx=0.0, cy=0.0):
    rad = math.radians(angulo_graus)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    tx = x - cx
    ty = y - cy

    nx = cx + (tx * cos_a) - (ty * sin_a)
    ny = cy + (tx * sin_a) + (ty * cos_a)
    return nx, ny


def escala_raw(x, y, sx, sy, cx=0.0, cy=0.0):
    nx = cx + (x - cx) * sx
    ny = cy + (y - cy) * sy
    return nx, ny


def reflexao_raw(x, y, tipo, cx=0.0, cy=0.0):
    if tipo == "X":
        return x, cy - (y - cy)
    if tipo == "Y":
        return cx - (x - cx), y
    if tipo == "XY":
        return cx - (x - cx), cy - (y - cy)
    return x, y
