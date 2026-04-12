# Transformacoes geometricas 2D

import math


# Translacao: desloca o ponto por (dx, dy)
def translacao_raw(x, y, dx, dy):
    return x + dx, y + dy


# Rotacao em torno do ponto (cx, cy)
def rotacao_raw(x, y, angulo_graus, cx=0.0, cy=0.0):
    rad = math.radians(angulo_graus)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # Translada para a origem antes de rotacionar
    tx = x - cx
    ty = y - cy

    # Aplica a rotacao e translada de volta
    nx = cx + (tx * cos_a) - (ty * sin_a)
    ny = cy + (tx * sin_a) + (ty * cos_a)
    return nx, ny


# Escala em relacao ao ponto (cx, cy)
def escala_raw(x, y, sx, sy, cx=0.0, cy=0.0):
    nx = cx + (x - cx) * sx
    ny = cy + (y - cy) * sy
    return nx, ny


# Reflexao em relacao a um eixo centrado em (cx, cy)
def reflexao_raw(x, y, tipo, cx=0.0, cy=0.0):
    if tipo == "X":       # reflete no eixo X (inverte Y)
        return x, cy - (y - cy)
    if tipo == "Y":       # reflete no eixo Y (inverte X)
        return cx - (x - cx), y
    if tipo == "XY":      # reflete em ambos os eixos
        return cx - (x - cx), cy - (y - cy)
    return x, y
