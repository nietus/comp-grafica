# Interface grafica do trabalho de Computacao Grafica
# Permite desenhar primitivas, aplicar transformacoes e recorte

import tkinter as tk
from tkinter import messagebox

import clipping as c
import rasterization as r
import transformations as t
from models import Circunferencia, Poligono, Ponto, Reta


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trabalho CG Antonio Neto")
        self.geometry("1100x700")

        self.canvas_width = 1100
        self.canvas_height = 520

        self.objetos = []              # todos os objetos desenhados
        self.objetos_selecionados = []  # objetos dentro da area de selecao
        self.pontos_temp = []           # pontos temporarios durante criacao

        self.modo_atual = "RETA_BRESENHAM"
        self.start_selection = None     # canto inicial da selecao
        self.end_selection = None       # canto final da selecao

        self._criar_interface()

    def _criar_interface(self):
        frame_formas = tk.Frame(self)
        frame_formas.pack(fill=tk.X, side=tk.TOP, padx=4, pady=4)

        frame_ops = tk.Frame(self)
        frame_ops.pack(fill=tk.X, side=tk.TOP, padx=4, pady=4)

        frame_transform = tk.Frame(self)
        frame_transform.pack(fill=tk.X, side=tk.TOP, padx=4, pady=4)

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.img = tk.PhotoImage(width=self.canvas_width, height=self.canvas_height)
        self.canvas.create_image((0, 0), image=self.img, anchor="nw", tags="img")

        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        tk.Button(frame_formas, text="Ponto", command=lambda: self.set_modo("PONTO")).pack(side=tk.LEFT)
        tk.Button(frame_formas, text="Reta DDA", command=lambda: self.set_modo("RETA_DDA")).pack(side=tk.LEFT)
        tk.Button(frame_formas, text="Reta Bresenham", command=lambda: self.set_modo("RETA_BRESENHAM")).pack(side=tk.LEFT)
        tk.Button(frame_formas, text="Circunferencia", command=lambda: self.set_modo("CIRCULO")).pack(side=tk.LEFT)
        tk.Button(frame_formas, text="Poligono", command=lambda: self.set_modo("POLIGONO")).pack(side=tk.LEFT)
        tk.Button(frame_formas, text="Finalizar Poligono", command=self.finaliza_poligono).pack(side=tk.LEFT)
        tk.Button(frame_formas, text="Selecionar Area", command=lambda: self.set_modo("SELECIONAR")).pack(side=tk.LEFT)
        tk.Button(frame_formas, text="Limpar Tudo", command=self.limpar).pack(side=tk.RIGHT)

        tk.Button(frame_ops, text="Clipping Cohen-Sutherland", command=lambda: self.recortar_selecao("COHEN")).pack(side=tk.LEFT)
        tk.Button(frame_ops, text="Clipping Liang-Barsky", command=lambda: self.recortar_selecao("LIANG")).pack(side=tk.LEFT)
        tk.Button(frame_ops, text="Apagar Selecionados", command=self.apagar_selecao).pack(side=tk.RIGHT)

        self.dx_var = tk.DoubleVar(value=40.0)
        self.dy_var = tk.DoubleVar(value=40.0)
        self.ang_var = tk.DoubleVar(value=30.0)
        self.sx_var = tk.DoubleVar(value=1.2)
        self.sy_var = tk.DoubleVar(value=1.2)
        self.reflexao_var = tk.StringVar(value="X")

        self._criar_slider(frame_transform, "dx", self.dx_var, -300, 300, 1.0)
        self._criar_slider(frame_transform, "dy", self.dy_var, -300, 300, 1.0)
        self._criar_slider(frame_transform, "angulo", self.ang_var, -180, 180, 1.0)
        self._criar_slider(frame_transform, "sx", self.sx_var, -4.0, 4.0, 0.1)
        self._criar_slider(frame_transform, "sy", self.sy_var, -4.0, 4.0, 0.1)

        tk.Button(frame_transform, text="Aplicar Translacao", command=self.aplicar_translacao).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_transform, text="Aplicar Rotacao", command=self.aplicar_rotacao).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_transform, text="Aplicar Escala", command=self.aplicar_escala).pack(side=tk.LEFT, padx=4)

        tk.OptionMenu(frame_transform, self.reflexao_var, "X", "Y", "XY").pack(side=tk.LEFT, padx=4)
        tk.Button(frame_transform, text="Aplicar Reflexao", command=self.aplicar_reflexao).pack(side=tk.LEFT, padx=4)

        self.status_var = tk.StringVar(
            value="Modo atual: RETA_BRESENHAM | Selecione area para transformar/recortar."
        )
        tk.Label(self, textvariable=self.status_var, anchor="w").pack(fill=tk.X, side=tk.BOTTOM, padx=4, pady=2)

    def _criar_slider(self, parent, label, variable, from_, to_, resolution):
        frame = tk.Frame(parent)
        frame.pack(side=tk.LEFT, padx=2)
        tk.Label(frame, text=label).pack(anchor="w")
        tk.Scale(
            frame,
            from_=from_,
            to=to_,
            orient=tk.HORIZONTAL,
            resolution=resolution,
            variable=variable,
            length=130,
        ).pack(anchor="w")

    def set_modo(self, modo):
        self.modo_atual = modo
        self.pontos_temp = []
        self.status_var.set(f"Modo atual: {modo}")

    def limpar(self):
        self.objetos.clear()
        self.objetos_selecionados.clear()
        self.pontos_temp.clear()
        self.start_selection = None
        self.end_selection = None
        self.redesenhar()

    def apagar_selecao(self):
        if not self.objetos_selecionados:
            messagebox.showinfo("Aviso", "Nenhum objeto selecionado.")
            return
        for obj in self.objetos_selecionados:
            if obj in self.objetos:
                self.objetos.remove(obj)
        self.objetos_selecionados.clear()
        self.redesenhar()

    def on_resize(self, event):
        if event.width > self.canvas_width or event.height > self.canvas_height:
            self.canvas_width = max(self.canvas_width, event.width)
            self.canvas_height = max(self.canvas_height, event.height)
            self.img = tk.PhotoImage(width=self.canvas_width, height=self.canvas_height)
            self.canvas.delete("img")
            self.canvas.create_image((0, 0), image=self.img, anchor="nw", tags="img")
            self.redesenhar()

    # Trata cliques no canvas conforme o modo atual
    def on_click(self, event):
        x, y = event.x, event.y

        if self.modo_atual == "SELECIONAR":
            self.start_selection = (x, y)
            self.end_selection = None
            self.canvas.delete("sel")
            return

        if self.modo_atual == "PONTO":
            self.objetos.append(Ponto(x, y))
            self.redesenhar()
            return

        if self.modo_atual in ("RETA_DDA", "RETA_BRESENHAM"):
            self.pontos_temp.append((x, y))
            if len(self.pontos_temp) == 2:
                p1 = Ponto(self.pontos_temp[0][0], self.pontos_temp[0][1])
                p2 = Ponto(self.pontos_temp[1][0], self.pontos_temp[1][1])
                algoritmo = "DDA" if self.modo_atual == "RETA_DDA" else "BRESENHAM"
                self.objetos.append(Reta(p1, p2, algoritmo=algoritmo))
                self.pontos_temp.clear()
                self.redesenhar()
            return

        if self.modo_atual == "CIRCULO":
            self.pontos_temp.append((x, y))
            if len(self.pontos_temp) == 2:
                xc, yc = self.pontos_temp[0]
                rx, ry = self.pontos_temp[1]
                raio = ((rx - xc) ** 2 + (ry - yc) ** 2) ** 0.5
                self.objetos.append(Circunferencia(Ponto(xc, yc), raio))
                self.pontos_temp.clear()
                self.redesenhar()
            return

        if self.modo_atual == "POLIGONO":
            self.pontos_temp.append((x, y))
            self.redesenhar()

    def on_drag(self, event):
        if self.modo_atual == "SELECIONAR" and self.start_selection:
            self.canvas.delete("sel")
            self.canvas.create_rectangle(
                self.start_selection[0],
                self.start_selection[1],
                event.x,
                event.y,
                outline="red",
                dash=(4, 2),
                tags="sel",
            )

    def on_release(self, event):
        if self.modo_atual != "SELECIONAR" or not self.start_selection:
            return

        self.end_selection = (event.x, event.y)
        self.objetos_selecionados = self._objetos_na_janela()
        self.redesenhar()
        messagebox.showinfo("Selecao", f"{len(self.objetos_selecionados)} objeto(s) selecionado(s).")

    # Fecha o poligono com os pontos coletados ate agora
    def finaliza_poligono(self):
        if len(self.pontos_temp) < 3:
            messagebox.showerror("Erro", "Poligono precisa de pelo menos 3 pontos.")
            return

        pontos = [Ponto(x, y) for x, y in self.pontos_temp]
        self.objetos.append(Poligono(pontos))
        self.pontos_temp.clear()
        self.redesenhar()

    def _obter_centro_transformacao(self):
        if self.start_selection and self.end_selection:
            x1, y1 = self.start_selection
            x2, y2 = self.end_selection
            return (x1 + x2) / 2.0, (y1 + y2) / 2.0
        return self.canvas_width / 2.0, self.canvas_height / 2.0

    def _aplicar_em_objetos_selecionados(self, func):
        if not self.objetos_selecionados:
            messagebox.showinfo("Aviso", "Nenhum objeto selecionado.")
            return

        for obj in self.objetos_selecionados:
            func(obj)
        self.redesenhar()

    def aplicar_translacao(self):
        dx = self.dx_var.get()
        dy = self.dy_var.get()

        def op(obj):
            if isinstance(obj, Ponto):
                obj.x, obj.y = t.translacao_raw(obj.x, obj.y, dx, dy)
            elif isinstance(obj, Reta):
                obj.p1.x, obj.p1.y = t.translacao_raw(obj.p1.x, obj.p1.y, dx, dy)
                obj.p2.x, obj.p2.y = t.translacao_raw(obj.p2.x, obj.p2.y, dx, dy)
            elif isinstance(obj, Poligono):
                for p in obj.pontos:
                    p.x, p.y = t.translacao_raw(p.x, p.y, dx, dy)
            elif isinstance(obj, Circunferencia):
                obj.centro.x, obj.centro.y = t.translacao_raw(obj.centro.x, obj.centro.y, dx, dy)

        self._aplicar_em_objetos_selecionados(op)

    def aplicar_rotacao(self):
        angulo = self.ang_var.get()
        cx, cy = self._obter_centro_transformacao()

        def op(obj):
            if isinstance(obj, Ponto):
                obj.x, obj.y = t.rotacao_raw(obj.x, obj.y, angulo, cx, cy)
            elif isinstance(obj, Reta):
                obj.p1.x, obj.p1.y = t.rotacao_raw(obj.p1.x, obj.p1.y, angulo, cx, cy)
                obj.p2.x, obj.p2.y = t.rotacao_raw(obj.p2.x, obj.p2.y, angulo, cx, cy)
            elif isinstance(obj, Poligono):
                for p in obj.pontos:
                    p.x, p.y = t.rotacao_raw(p.x, p.y, angulo, cx, cy)
            elif isinstance(obj, Circunferencia):
                obj.centro.x, obj.centro.y = t.rotacao_raw(obj.centro.x, obj.centro.y, angulo, cx, cy)

        self._aplicar_em_objetos_selecionados(op)

    def aplicar_escala(self):
        sx = self.sx_var.get()
        sy = self.sy_var.get()
        cx, cy = self._obter_centro_transformacao()

        def op(obj):
            if isinstance(obj, Ponto):
                obj.x, obj.y = t.escala_raw(obj.x, obj.y, sx, sy, cx, cy)
            elif isinstance(obj, Reta):
                obj.p1.x, obj.p1.y = t.escala_raw(obj.p1.x, obj.p1.y, sx, sy, cx, cy)
                obj.p2.x, obj.p2.y = t.escala_raw(obj.p2.x, obj.p2.y, sx, sy, cx, cy)
            elif isinstance(obj, Poligono):
                for p in obj.pontos:
                    p.x, p.y = t.escala_raw(p.x, p.y, sx, sy, cx, cy)
            elif isinstance(obj, Circunferencia):
                obj.centro.x, obj.centro.y = t.escala_raw(obj.centro.x, obj.centro.y, sx, sy, cx, cy)
                fator = max(abs(sx), abs(sy))
                obj.raio = abs(obj.raio * fator)

        self._aplicar_em_objetos_selecionados(op)

    def aplicar_reflexao(self):
        tipo = self.reflexao_var.get()
        cx, cy = self._obter_centro_transformacao()

        def op(obj):
            if isinstance(obj, Ponto):
                obj.x, obj.y = t.reflexao_raw(obj.x, obj.y, tipo, cx, cy)
            elif isinstance(obj, Reta):
                obj.p1.x, obj.p1.y = t.reflexao_raw(obj.p1.x, obj.p1.y, tipo, cx, cy)
                obj.p2.x, obj.p2.y = t.reflexao_raw(obj.p2.x, obj.p2.y, tipo, cx, cy)
            elif isinstance(obj, Poligono):
                for p in obj.pontos:
                    p.x, p.y = t.reflexao_raw(p.x, p.y, tipo, cx, cy)
            elif isinstance(obj, Circunferencia):
                obj.centro.x, obj.centro.y = t.reflexao_raw(obj.centro.x, obj.centro.y, tipo, cx, cy)

        self._aplicar_em_objetos_selecionados(op)

    # Aplica recorte (clipping) nas retas dentro da area selecionada
    def recortar_selecao(self, tipo):
        if not self.start_selection or not self.end_selection:
            messagebox.showinfo("Aviso", "Selecione uma area retangular antes do recorte.")
            return

        x1, y1 = self.start_selection
        x2, y2 = self.end_selection
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)

        novos_objetos = []
        for obj in self.objetos:
            if isinstance(obj, Reta):
                if tipo == "COHEN":
                    recorte = c.cohen_sutherland(obj.p1.x, obj.p1.y, obj.p2.x, obj.p2.y, xmin, ymin, xmax, ymax)
                else:
                    recorte = c.liang_barsky(obj.p1.x, obj.p1.y, obj.p2.x, obj.p2.y, xmin, ymin, xmax, ymax)

                if recorte:
                    novos_objetos.append(
                        Reta(
                            Ponto(recorte[0], recorte[1]),
                            Ponto(recorte[2], recorte[3]),
                            algoritmo=obj.algoritmo,
                        )
                    )
            else:
                novos_objetos.append(obj)

        self.objetos = novos_objetos
        self.objetos_selecionados = self._objetos_na_janela()
        self.redesenhar()

    # Retorna os objetos cuja bounding box intersecta a area de selecao
    def _objetos_na_janela(self):
        if not self.start_selection or not self.end_selection:
            return []

        x1, y1 = self.start_selection
        x2, y2 = self.end_selection
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        selecao = (xmin, ymin, xmax, ymax)

        selecionados = []
        for obj in self.objetos:
            bb = self._bounding_box_objeto(obj)
            if bb and self._intersecta(bb, selecao):
                selecionados.append(obj)
        return selecionados

    def _bounding_box_objeto(self, obj):
        if isinstance(obj, Ponto):
            return obj.x, obj.y, obj.x, obj.y

        if isinstance(obj, Reta):
            return (
                min(obj.p1.x, obj.p2.x),
                min(obj.p1.y, obj.p2.y),
                max(obj.p1.x, obj.p2.x),
                max(obj.p1.y, obj.p2.y),
            )

        if isinstance(obj, Poligono) and obj.pontos:
            xs = [p.x for p in obj.pontos]
            ys = [p.y for p in obj.pontos]
            return min(xs), min(ys), max(xs), max(ys)

        if isinstance(obj, Circunferencia):
            return (
                obj.centro.x - obj.raio,
                obj.centro.y - obj.raio,
                obj.centro.x + obj.raio,
                obj.centro.y + obj.raio,
            )
        return None

    @staticmethod
    def _intersecta(bb1, bb2):
        ax1, ay1, ax2, ay2 = bb1
        bx1, by1, bx2, by2 = bb2
        return ax1 <= bx2 and ax2 >= bx1 and ay1 <= by2 and ay2 >= by1

    # Redesenha todos os objetos no canvas (objetos selecionados ficam em vermelho)
    def redesenhar(self):
        self.img.blank()

        selecionados_ids = set(id(o) for o in self.objetos_selecionados)

        for obj in self.objetos:
            cor = "#d00000" if id(obj) in selecionados_ids else "#000000"
            self._desenhar_objeto(obj, cor)

        if self.modo_atual == "POLIGONO" and self.pontos_temp:
            for i in range(1, len(self.pontos_temp)):
                x1, y1 = self.pontos_temp[i - 1]
                x2, y2 = self.pontos_temp[i]
                for x, y in r.bresenham_reta(x1, y1, x2, y2):
                    self.set_pixel(x, y, "#0066cc")

        self.canvas.delete("sel")
        if self.start_selection and self.end_selection:
            self.canvas.create_rectangle(
                self.start_selection[0],
                self.start_selection[1],
                self.end_selection[0],
                self.end_selection[1],
                outline="red",
                dash=(4, 2),
                tags="sel",
            )

    # Rasteriza e desenha um objeto pixel a pixel
    def _desenhar_objeto(self, obj, cor):
        if isinstance(obj, Ponto):
            self.set_pixel(obj.x, obj.y, cor)
            return

        if isinstance(obj, Reta):
            if obj.algoritmo == "DDA":
                pontos = r.dda(obj.p1.x, obj.p1.y, obj.p2.x, obj.p2.y)
            else:
                pontos = r.bresenham_reta(obj.p1.x, obj.p1.y, obj.p2.x, obj.p2.y)
            for x, y in pontos:
                self.set_pixel(x, y, cor)
            return

        if isinstance(obj, Circunferencia):
            for x, y in r.bresenham_circulo(obj.centro.x, obj.centro.y, obj.raio):
                self.set_pixel(x, y, cor)
            return

        if isinstance(obj, Poligono):
            n = len(obj.pontos)
            if n < 2:
                return
            for i in range(n):
                p1 = obj.pontos[i]
                p2 = obj.pontos[(i + 1) % n]
                for x, y in r.bresenham_reta(p1.x, p1.y, p2.x, p2.y):
                    self.set_pixel(x, y, cor)

    # Pinta um pixel na imagem (ignora se estiver fora dos limites)
    def set_pixel(self, x, y, color):
        xi = int(round(x))
        yi = int(round(y))
        if 0 <= xi < self.canvas_width and 0 <= yi < self.canvas_height:
            self.img.put(color, (xi, yi))


if __name__ == "__main__":
    app = App()
    app.mainloop()
