# Curvas parametricas (TP2)
#
# Este modulo reune codigo pronto (de dominio publico / referencias classicas)
# para gerar dois tipos de curvas parametricas a partir de pontos de controle:
#
#   1) Curva de Bezier  -> algoritmo de De Casteljau
#   2) Curva B-Spline    -> B-spline cubica uniforme (forma matricial)
#
# As funcoes recebem uma lista de pontos de controle no formato [(x, y), ...]
# e devolvem uma lista de pontos da curva [(x, y), ...] ja amostrados, prontos
# para serem ligados por pequenos segmentos de reta na rasterizacao.
#
# Fontes do codigo adaptado (ver DOCUMENTACAO_TP2.md para detalhes):
#   - De Casteljau: implementacao classica descrita na Wikipedia
#     (https://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm)
#   - B-spline cubica uniforme: forma matricial apresentada em Hearn & Baker,
#     "Computer Graphics with OpenGL", e em diversos materiais on-line.


# ---------------------------------------------------------------------------
# 1) CURVA DE BEZIER - ALGORITMO DE DE CASTELJAU
# ---------------------------------------------------------------------------

# Avalia um unico ponto da curva de Bezier para um parametro t em [0, 1].
# O algoritmo de De Casteljau faz interpolacoes lineares sucessivas entre os
# pontos de controle ate sobrar um unico ponto, que pertence a curva.
def _de_casteljau(pontos, t):
    # Copia mutavel dos pontos de controle (cada ponto vira [x, y])
    temp = [[p[0], p[1]] for p in pontos]
    n = len(temp)

    # A cada nivel r, interpola cada par de pontos vizinhos
    for r in range(1, n):
        for i in range(n - r):
            temp[i][0] = (1.0 - t) * temp[i][0] + t * temp[i + 1][0]
            temp[i][1] = (1.0 - t) * temp[i][1] + t * temp[i + 1][1]

    # O primeiro elemento concentra o resultado final da interpolacao
    return (temp[0][0], temp[0][1])


# Gera a curva de Bezier amostrando 'num_amostras' valores de t entre 0 e 1.
# Funciona para qualquer quantidade de pontos de controle (>= 2).
def bezier_de_casteljau(pontos, num_amostras=200):
    curva = []
    if len(pontos) < 2:
        return curva

    for i in range(num_amostras + 1):
        t = i / float(num_amostras)
        curva.append(_de_casteljau(pontos, t))

    return curva


# ---------------------------------------------------------------------------
# 2) CURVA B-SPLINE CUBICA UNIFORME (FORMA MATRICIAL)
# ---------------------------------------------------------------------------

# Avalia um ponto de um segmento de B-spline cubica uniforme definido por
# 4 pontos de controle consecutivos (p0, p1, p2, p3) e parametro t em [0, 1].
# Os coeficientes vem da matriz base da B-spline cubica uniforme (fator 1/6).
def _segmento_bspline(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    # Funcoes de mistura (blending) da B-spline cubica uniforme
    b0 = (-t3 + 3.0 * t2 - 3.0 * t + 1.0) / 6.0
    b1 = (3.0 * t3 - 6.0 * t2 + 4.0) / 6.0
    b2 = (-3.0 * t3 + 3.0 * t2 + 3.0 * t + 1.0) / 6.0
    b3 = t3 / 6.0

    x = b0 * p0[0] + b1 * p1[0] + b2 * p2[0] + b3 * p3[0]
    y = b0 * p0[1] + b1 * p1[1] + b2 * p2[1] + b3 * p3[1]
    return (x, y)


# Gera a curva B-spline cubica uniforme. Para cada grupo de 4 pontos de
# controle consecutivos calcula um segmento; a juncao dos segmentos forma a
# curva completa. Exige pelo menos 4 pontos de controle.
def bspline_uniforme_cubica(pontos, num_amostras=30):
    curva = []
    n = len(pontos)
    if n < 4:
        return curva

    # Desliza uma "janela" de 4 pontos ao longo da lista de controle
    for i in range(n - 3):
        p0 = pontos[i]
        p1 = pontos[i + 1]
        p2 = pontos[i + 2]
        p3 = pontos[i + 3]

        for j in range(num_amostras + 1):
            t = j / float(num_amostras)
            curva.append(_segmento_bspline(p0, p1, p2, p3, t))

    return curva


# ---------------------------------------------------------------------------
# Funcao auxiliar usada pela interface: devolve os pontos amostrados da curva
# de acordo com o tipo escolhido.
# ---------------------------------------------------------------------------
def gerar_curva(pontos_controle, tipo):
    if tipo == "BEZIER":
        return bezier_de_casteljau(pontos_controle)
    if tipo == "BSPLINE":
        return bspline_uniforme_cubica(pontos_controle)
    return []
