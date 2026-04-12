# Algoritmos de recorte (clipping) de retas

# Codigos de regiao para Cohen-Sutherland (bits representam cada lado)
INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8


# Calcula o codigo de regiao de um ponto em relacao a janela de recorte
def compute_code(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT

    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP

    return code


# Recorte de reta pelo algoritmo de Cohen-Sutherland
def cohen_sutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    accept = False

    while True:
        c1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
        c2 = compute_code(x2, y2, xmin, ymin, xmax, ymax)

        # Ambos os pontos dentro da janela — aceita
        if c1 == 0 and c2 == 0:
            accept = True
            break

        # Ambos os pontos do mesmo lado de fora — rejeita
        if (c1 & c2) != 0:
            break

        # Calcula intersecao com a borda da janela
        code_out = c1 if c1 != 0 else c2
        x_int = 0.0
        y_int = 0.0

        if code_out & LEFT:
            if x2 == x1:
                return None
            x_int = xmin
            y_int = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
        elif code_out & RIGHT:
            if x2 == x1:
                return None
            x_int = xmax
            y_int = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
        elif code_out & BOTTOM:
            if y2 == y1:
                return None
            y_int = ymin
            x_int = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
        else:
            if y2 == y1:
                return None
            y_int = ymax
            x_int = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)

        # Substitui o ponto de fora pela intersecao
        if code_out == c1:
            x1, y1 = x_int, y_int
        else:
            x2, y2 = x_int, y_int

    if not accept:
        return None

    return x1, y1, x2, y2


# Cliptest para Liang-Barsky
def _cliptest(p, q, u1, u2):
    if p < 0:
        r = q / p
        if r > u2:
            return False, u1, u2
        if r > u1:
            u1 = r
    elif p > 0:
        r = q / p
        if r < u1:
            return False, u1, u2
        if r < u2:
            u2 = r
    else:
        if q < 0:
            return False, u1, u2
    return True, u1, u2


# Recorte de reta pelo algoritmo de Liang-Barsky (parametrico)
def liang_barsky(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    dx = x2 - x1
    dy = y2 - y1
    u1 = 0.0  # parametro de entrada
    u2 = 1.0  # parametro de saida

    # Testa as 4 bordas: esquerda, direita, inferior, superior
    ok, u1, u2 = _cliptest(-dx, x1 - xmin, u1, u2)
    if not ok:
        return None
    ok, u1, u2 = _cliptest(dx, xmax - x1, u1, u2)
    if not ok:
        return None
    ok, u1, u2 = _cliptest(-dy, y1 - ymin, u1, u2)
    if not ok:
        return None
    ok, u1, u2 = _cliptest(dy, ymax - y1, u1, u2)
    if not ok:
        return None

    # Calcula os novos pontos recortados
    nx1 = x1 + u1 * dx
    ny1 = y1 + u1 * dy
    nx2 = x1 + u2 * dx
    ny2 = y1 + u2 * dy
    return nx1, ny1, nx2, ny2
