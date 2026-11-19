"""Genera todo el arte original del juego "Unicornio: El Reino Encantado".

Uso:  python generar_arte.py <carpeta_del_proyecto>
Crea las imagenes en <proyecto>/assets/fantasia/.
Todo se dibuja con figuras simples (Pillow) a 4x y se reduce para suavizar bordes.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

S = 4  # super-muestreo
OUT = (52, 34, 72, 255)          # color de contorno
W_OUT = 3                        # grosor de contorno (px finales)

PROYECTO = sys.argv[1] if len(sys.argv) > 1 else "."
DEST = os.path.join(PROYECTO, "assets", "fantasia")
os.makedirs(DEST, exist_ok=True)


# ---------------------------------------------------------------- utilidades
class Lienzo:
    """Lienzo con coordenadas en px finales; dibuja internamente a S x."""

    def __init__(self, w, h, fondo=(0, 0, 0, 0)):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (w * S, h * S), fondo)
        self.d = ImageDraw.Draw(self.im)

    @staticmethod
    def _p(pts):
        return [(x * S, y * S) for x, y in pts]

    def elipse(self, x0, y0, x1, y1, color, borde=OUT, grosor=W_OUT):
        self.d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=color,
                       outline=borde, width=int(grosor * S) if borde else 0)

    def circulo(self, cx, cy, r, color, borde=OUT, grosor=W_OUT):
        self.elipse(cx - r, cy - r, cx + r, cy + r, color, borde, grosor)

    def poligono(self, pts, color, borde=OUT, grosor=W_OUT):
        self.d.polygon(self._p(pts), fill=color)
        if borde:
            p = self._p(pts)
            self.d.line(p + [p[0]], fill=borde, width=int(grosor * S), joint="curve")

    def rect(self, x0, y0, x1, y1, color, borde=OUT, grosor=W_OUT, radio=0):
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=radio * S,
                                 fill=color, outline=borde,
                                 width=int(grosor * S) if borde else 0)

    def linea(self, pts, color, ancho, redondo=True):
        p = self._p(pts)
        self.d.line(p, fill=color, width=int(ancho * S), joint="curve")
        if redondo:
            for x, y in p:
                r = ancho * S / 2
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)

    def pierna(self, a, b, color, ancho, casco=None):
        """Pierna = trazo grueso con contorno y casco opcional al final."""
        self.linea([a, b], OUT, ancho + W_OUT * 2)
        self.linea([a, b], color, ancho)
        if casco:
            bx, by = b
            self.rect(bx - ancho / 2 - 1, by - 3, bx + ancho / 2 + 1, by + 5, casco, radio=2)

    def guardar(self, nombre):
        im = self.im.resize((self.w, self.h), Image.LANCZOS)
        im.save(os.path.join(DEST, nombre))
        print("ok", nombre, im.size)
        return im


def mezcla(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(len(c1)))


# ---------------------------------------------------------------- UNICORNIO
BLANCO = (252, 248, 255, 255)
SOMBRA = (222, 212, 246, 255)
CASCO = (240, 196, 92, 255)
CUERNO = (255, 214, 92, 255)
CUERNO_RAYA = (226, 160, 40, 255)
ARCOIRIS = [(255, 112, 170, 255), (255, 170, 90, 255), (255, 228, 110, 255),
            (120, 226, 170, 255), (110, 176, 255, 255), (180, 120, 255, 255)]


def unicornio(nombre, patas):
    """patas: dict con desplazamientos de pies {'ad','at','pd','pt'} (adelante/atras, delantera/trasera)."""
    c = Lienzo(180, 176)
    oy = 20
    # cola arcoiris
    for i, col in enumerate(ARCOIRIS):
        ang = math.radians(200 + i * 14)
        for k in range(5):
            r = 9 - k * 0.6
            cx = 44 + math.cos(ang) * (8 + k * 7) - k * 2
            cy = 70 + oy + math.sin(ang) * -(4 + k * 5) + k * 6
            c.circulo(cx, cy, r, col, borde=None)
    # patas lejanas (sombreadas)
    hips = {"td": (58, 96 + oy), "dd": (112, 96 + oy)}
    c.pierna(hips["td"], (58 + patas["pt"][0], 140 + oy + patas["pt"][1]), SOMBRA, 13, CASCO)
    c.pierna(hips["dd"], (112 + patas["pd"][0], 140 + oy + patas["pd"][1]), SOMBRA, 13, CASCO)
    # cuerpo
    c.elipse(36, 52 + oy, 132, 108 + oy, BLANCO)
    c.elipse(50, 84 + oy, 120, 104 + oy, SOMBRA, borde=None)
    # patas cercanas
    c.pierna((48, 98 + oy), (48 + patas["at"][0], 140 + oy + patas["at"][1]), BLANCO, 14, CASCO)
    c.pierna((122, 98 + oy), (122 + patas["ad"][0], 140 + oy + patas["ad"][1]), BLANCO, 14, CASCO)
    # cuello
    c.poligono([(104, 66 + oy), (128, 84 + oy), (148, 40 + oy), (126, 24 + oy)], BLANCO)
    # cabeza y hocico
    c.elipse(118, 8 + oy, 158, 46 + oy, BLANCO)
    c.elipse(136, 22 + oy, 172, 52 + oy, (255, 232, 240, 255))
    c.circulo(162, 38 + oy, 2.2, OUT, borde=None)  # fosa nasal
    # oreja
    c.poligono([(124, 16 + oy), (126, -2 + oy), (138, 12 + oy)], BLANCO)
    c.poligono([(127, 12 + oy), (128, 4 + oy), (133, 11 + oy)], (255, 190, 210, 255), borde=None)
    # cuerno
    base = [(138, 12 + oy), (150, 14 + oy)]
    punta = (160, -14 + oy)
    c.poligono([base[0], punta, base[1]], CUERNO)
    for t in (0.3, 0.55, 0.78):
        a = mezcla(base[0], punta, t)
        b = mezcla(base[1], punta, t)
        c.linea([(a[0], a[1] + 2), (b[0], b[1] - 2)], CUERNO_RAYA, 1.6, redondo=False)
    # crin arcoiris por la nuca
    crin = [(124, 8), (118, 18), (112, 30), (106, 42), (100, 54), (94, 64)]
    for i, (x, y) in enumerate(crin):
        col = ARCOIRIS[i % len(ARCOIRIS)]
        c.circulo(x, y + oy, 10, col)
    c.circulo(130, 8 + oy, 8, ARCOIRIS[-1])  # mechón en la frente
    # ojo
    c.elipse(140, 20 + oy, 152, 34 + oy, OUT, borde=None)
    c.circulo(144, 24 + oy, 2.6, (255, 255, 255, 255), borde=None)
    c.circulo(149, 30 + oy, 1.2, (255, 255, 255, 255), borde=None)
    c.elipse(146, 36 + oy, 158, 42 + oy, (255, 160, 190, 200), borde=None)  # rubor
    # estrellita en el anca (marca de magia)
    est = []
    for k in range(10):
        r = 9 if k % 2 == 0 else 4
        a = math.radians(-90 + k * 36)
        est.append((70 + math.cos(a) * r, 74 + oy + math.sin(a) * r))
    c.poligono(est, (255, 200, 230, 255), borde=None)
    return c.guardar(nombre)


# ---------------------------------------------------------------- TROLL
PIEL = (128, 156, 116, 255)
PIEL_OSC = (98, 124, 90, 255)
TAPARRABO = (136, 92, 56, 255)


def troll():
    c = Lienzo(120, 130)
    # pies
    c.elipse(22, 112, 52, 128, PIEL_OSC)
    c.elipse(68, 112, 98, 128, PIEL_OSC)
    # cuerpo
    c.elipse(10, 30, 110, 120, PIEL)
    c.elipse(30, 60, 90, 112, (150, 176, 136, 255), borde=None)  # panza
    # taparrabo
    c.poligono([(22, 96), (98, 96), (90, 118), (74, 110), (60, 120), (46, 110), (30, 118)], TAPARRABO)
    c.linea([(22, 98), (98, 98)], (96, 62, 36, 255), 3)
    # cabeza (pequeña, hundida en los hombros)
    c.elipse(32, 4, 88, 56, PIEL)
    # orejas puntiagudas
    c.poligono([(34, 26), (14, 14), (36, 38)], PIEL)
    c.poligono([(86, 26), (106, 14), (84, 38)], PIEL)
    # cejas enojadas y ojos
    c.linea([(44, 22), (58, 28)], OUT, 4)
    c.linea([(76, 22), (62, 28)], OUT, 4)
    c.circulo(52, 32, 5, (255, 236, 120, 255))
    c.circulo(68, 32, 5, (255, 236, 120, 255))
    c.circulo(53, 33, 2.2, OUT, borde=None)
    c.circulo(67, 33, 2.2, OUT, borde=None)
    # nariz de papa
    c.elipse(54, 34, 66, 44, PIEL_OSC)
    # boca con colmillos
    c.elipse(46, 44, 74, 54, (90, 40, 50, 255))
    c.poligono([(50, 48), (53, 38), (56, 48)], (250, 246, 230, 255), grosor=1.5)
    c.poligono([(64, 48), (67, 38), (70, 48)], (250, 246, 230, 255), grosor=1.5)
    # verrugas / manchas
    for x, y in [(30, 70), (88, 64), (80, 86)]:
        c.circulo(x, y, 3, PIEL_OSC, borde=None)
    c.guardar("troll.png")

    m = Lienzo(48, 48)
    m.circulo(24, 26, 16, PIEL)
    for i, x in enumerate((14, 22, 30)):
        m.circulo(x, 12 + (i % 2) * 2, 6, PIEL)
    m.circulo(38, 30, 6, PIEL)
    m.guardar("troll_mano.png")


# ---------------------------------------------------------------- ROCAS
def roca(nombre, grietas_color, base=(150, 136, 128, 255), brillo=False):
    c = Lienzo(64, 64)
    rnd = random.Random(7)
    pts = []
    for k in range(11):
        a = math.radians(k * 360 / 11)
        r = 19 + rnd.uniform(-2.2, 2.2)
        pts.append((32 + math.cos(a) * r, 32 + math.sin(a) * r))
    c.poligono(pts, base)
    c.elipse(18, 16, 34, 28, mezcla(base, (255, 255, 255, 255), 0.25), borde=None)
    c.linea([(26, 34), (34, 30), (38, 40), (44, 38)], grietas_color, 2.4)
    c.linea([(20, 42), (26, 46)], grietas_color, 2.0)
    c.linea([(36, 20), (40, 26)], grietas_color, 2.0)
    if brillo:
        glow = Image.new("RGBA", c.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse([8 * S, 8 * S, 56 * S, 56 * S], fill=(255, 120, 40, 90))
        glow = glow.filter(ImageFilter.GaussianBlur(6 * S))
        c.im = Image.alpha_composite(glow, c.im)
        c.d = ImageDraw.Draw(c.im)
    else:
        c.elipse(36, 38, 46, 46, (110, 150, 80, 255), borde=None)  # musgo
    c.guardar(nombre)


# ---------------------------------------------------------------- BOLA DE FUEGO
def bola_fuego():
    c = Lienzo(56, 84)
    capas = [((255, 90, 40, 255), 1.0), ((255, 160, 50, 255), 0.72), ((255, 236, 140, 255), 0.42)]
    for col, f in capas:
        r = 18 * f
        cx, cy = 28, 62
        cola = [(cx - r, cy), (cx - r * 0.6, cy - 34 * f - 6), (cx - r * 0.1, cy - 22 * f),
                (cx + r * 0.2, cy - 52 * f - 4), (cx + r * 0.5, cy - 24 * f), (cx + r * 0.9, cy - 38 * f),
                (cx + r, cy)]
        c.poligono(cola, col, borde=None)
        c.circulo(cx, cy, r, col, borde=None)
    c.circulo(28, 62, 18, (0, 0, 0, 0), borde=(150, 40, 20, 255), grosor=2)
    # ojitos traviesos
    c.circulo(23, 63, 2.4, OUT, borde=None)
    c.circulo(33, 63, 2.4, OUT, borde=None)
    c.guardar("bola_fuego.png")

    # chispa (particula)
    p = Lienzo(16, 16)
    p.circulo(8, 8, 6, (255, 200, 80, 255), borde=None)
    p.circulo(8, 8, 3, (255, 250, 210, 255), borde=None)
    p.guardar("chispa.png")


# ---------------------------------------------------------------- LOBO SOMBRIO
LOBO = (92, 84, 128, 255)
LOBO_OSC = (66, 58, 98, 255)


def lobo(nombre, fase):
    c = Lienzo(120, 76)
    d = 10 if fase == 0 else -10
    # cola
    c.poligono([(18, 34), (2, 18), (6, 30), (0, 40), (20, 44)], LOBO_OSC)
    # patas lejanas
    c.pierna((36, 50), (36 - d, 70), LOBO_OSC, 9)
    c.pierna((84, 50), (84 + d, 70), LOBO_OSC, 9)
    # cuerpo
    c.elipse(14, 24, 100, 60, LOBO)
    c.poligono([(30, 28), (40, 18), (48, 28), (58, 20), (66, 28), (76, 20), (82, 30)], LOBO_OSC, borde=None)
    # patas cercanas
    c.pierna((30, 52), (30 + d, 70), LOBO, 10)
    c.pierna((90, 50), (90 - d, 70), LOBO, 10)
    # cabeza
    c.elipse(80, 10, 112, 42, LOBO)
    c.poligono([(100, 24), (120, 32), (102, 40)], LOBO)  # hocico
    c.circulo(118, 31, 2.5, OUT, borde=None)
    c.poligono([(84, 16), (86, 0), (96, 12)], LOBO)  # oreja
    c.circulo(100, 22, 4, (255, 236, 90, 255), borde=None)  # ojo brillante
    c.circulo(101, 22, 1.6, OUT, borde=None)
    c.poligono([(104, 38), (106, 44), (109, 38)], (255, 255, 255, 255), grosor=1)  # colmillo
    c.guardar(nombre)


# ---------------------------------------------------------------- PLATAFORMAS
PIEDRA = [(170, 160, 196, 255), (156, 146, 184, 255), (184, 174, 208, 255)]
PIEDRA_OSC = (110, 100, 140, 255)
PASTO = (124, 206, 132, 255)
PASTO_OSC = (78, 160, 98, 255)


def franja_pasto(c, w, y, alto=7, flores=True, semilla=1):
    rnd = random.Random(semilla)
    c.rect(-2, y, w + 2, y + alto, PASTO, borde=OUT, grosor=2, radio=3)
    x = 2
    while x < w - 4:
        h = rnd.uniform(3, 7)
        c.poligono([(x, y + alto - 1), (x + 2.5, y + alto + h), (x + 5, y + alto - 1)], PASTO_OSC, borde=None)
        x += rnd.uniform(6, 14)
    if flores:
        for _ in range(w // 70):
            fx = rnd.uniform(8, w - 8)
            col = rnd.choice([(255, 150, 200, 255), (255, 240, 140, 255), (170, 210, 255, 255)])
            c.circulo(fx, y + 1, 2.4, col, borde=None)


def ladrillos(c, w, y0, y1, alto_fila, semilla=2):
    rnd = random.Random(semilla)
    fila = 0
    y = y0
    while y < y1:
        x = -rnd.uniform(0, 20) - (fila % 2) * 18
        while x < w:
            lw = rnd.uniform(30, 46)
            c.rect(x, y, x + lw, min(y + alto_fila, y1), rnd.choice(PIEDRA), borde=PIEDRA_OSC, grosor=1.6, radio=2)
            x += lw
        y += alto_fila
        fila += 1


def plataforma(nombre, w, h, alto_fila, semilla):
    c = Lienzo(w, h)
    ladrillos(c, w, 6, h - 2, alto_fila, semilla)
    c.d.line([(0, (h - 2) * S), (w * S, (h - 2) * S)], fill=OUT, width=2 * S)
    franja_pasto(c, w, 0, alto=6, semilla=semilla)
    c.guardar(nombre)


def muralla():
    w, h = 1444, 180
    c = Lienzo(w, h)
    ladrillos(c, w, 6, h, 22, semilla=9)
    # arcos oscuros como en un acueducto/castillo
    x = 30
    while x < w - 60:
        c.d.rounded_rectangle([x * S, 70 * S, (x + 44) * S, (h + 10) * S], radius=22 * S,
                              fill=(60, 48, 90, 255), outline=OUT, width=3 * S)
        c.circulo(x + 22, 98, 4, (255, 220, 120, 255), borde=None)  # farolito
        x += 96
    franja_pasto(c, w, 0, alto=8, semilla=9)
    c.guardar("muralla.png")


# ---------------------------------------------------------------- DECORACION
def arbol_magico(nombre, hojas, semilla):
    c = Lienzo(110, 170)
    rnd = random.Random(semilla)
    c.poligono([(48, 170), (52, 90), (40, 70), (50, 72), (55, 60), (62, 74), (72, 66), (64, 92), (66, 170)],
               (120, 86, 120, 255))
    for _ in range(9):
        x, y, r = rnd.uniform(22, 88), rnd.uniform(22, 80), rnd.uniform(16, 24)
        c.circulo(x, y, r, hojas)
    for _ in range(10):
        x, y = rnd.uniform(18, 92), rnd.uniform(14, 90)
        c.circulo(x, y, 2.2, (255, 255, 220, 255), borde=None)
    c.guardar(nombre)


def cristal():
    c = Lienzo(90, 130)
    glow = Image.new("RGBA", c.im.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([5 * S, 5 * S, 85 * S, 105 * S], fill=(140, 240, 255, 110))
    c.im = Image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9 * S)), c.im)
    c.d = ImageDraw.Draw(c.im)
    # pedestal
    c.rect(22, 104, 68, 118, PIEDRA[0], radio=3)
    c.rect(14, 116, 76, 128, PIEDRA[1], radio=3)
    # cristal principal + laterales
    c.poligono([(45, 6), (62, 40), (54, 104), (36, 104), (28, 40)], (150, 236, 255, 255))
    c.poligono([(45, 6), (50, 40), (45, 104), (36, 104), (28, 40)], (205, 250, 255, 255), borde=None)
    c.poligono([(24, 60), (34, 74), (34, 104), (22, 104), (16, 78)], (190, 160, 255, 255))
    c.poligono([(66, 58), (74, 78), (68, 104), (56, 104), (56, 74)], (255, 170, 230, 255))
    for x, y in [(12, 20), (78, 30), (70, 8), (18, 46)]:
        c.circulo(x, y, 2.5, (255, 255, 255, 255), borde=None)
    c.guardar("cristal.png")


def fondo():
    W = H = 2048
    im = Image.new("RGBA", (W, H))
    px = im.load()
    arriba, medio, abajo = (34, 24, 74), (104, 64, 140), (250, 160, 170)
    for y in range(H):
        t = y / H
        col = mezcla(arriba, medio, t / 0.55) if t < 0.55 else mezcla(medio, abajo, (t - 0.55) / 0.2) if t < 0.75 else abajo
        for x in range(W):
            px[x, y] = col + (255,)
    d = ImageDraw.Draw(im)
    rnd = random.Random(3)
    for _ in range(260):  # estrellas
        x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.55)
        r = rnd.choice([1, 1, 1.5, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 220, rnd.randint(150, 255)))
    # luna con halo
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([640, 560, 940, 860], fill=(255, 240, 200, 90))
    im = Image.alpha_composite(im, halo.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(im)
    d.ellipse([700, 620, 880, 800], fill=(255, 246, 214))
    for x, y, r in [(760, 680, 18), (820, 740, 12), (790, 760, 8)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(236, 224, 190))

    def montes(y_base, alto, color, semilla, paso):
        rnd2 = random.Random(semilla)
        pts = [(0, H)]
        x = -100
        while x < W + 200:
            pts.append((x, y_base - rnd2.uniform(alto * 0.4, alto)))
            x += rnd2.uniform(paso * 0.6, paso)
            pts.append((x, y_base - rnd2.uniform(0, alto * 0.25)))
            x += rnd2.uniform(paso * 0.4, paso * 0.8)
        pts.append((W, H))
        d.polygon(pts, fill=color)

    montes(1360, 380, (120, 84, 160), 11, 260)
    # nieve en cumbres lejanas
    montes(1440, 300, (92, 64, 132), 12, 200)
    # castillo en la colina
    cx0, base = 1320, 1330
    d.ellipse([1150, base - 40, 1700, base + 300], fill=(70, 48, 104))
    torres = [(cx0, 230, 70), (cx0 + 90, 330, 80), (cx0 + 190, 270, 70), (cx0 + 280, 200, 60)]
    d.rectangle([cx0 - 10, base - 160, cx0 + 330, base], fill=(56, 38, 88))
    for tx, alto, ancho in torres:
        d.rectangle([tx, base - alto, tx + ancho, base], fill=(56, 38, 88))
        d.polygon([(tx - 12, base - alto), (tx + ancho / 2, base - alto - 90), (tx + ancho + 12, base - alto)],
                  fill=(150, 70, 130))
        d.line([(tx + ancho / 2, base - alto - 90), (tx + ancho / 2, base - alto - 130)], fill=(56, 38, 88), width=4)
        d.polygon([(tx + ancho / 2, base - alto - 130), (tx + ancho / 2 + 34, base - alto - 120),
                   (tx + ancho / 2, base - alto - 108)], fill=(255, 140, 190))
        for wy in range(base - alto + 30, base - 30, 60):
            d.rounded_rectangle([tx + ancho / 2 - 9, wy, tx + ancho / 2 + 9, wy + 26], radius=8, fill=(255, 214, 120))
    montes(1560, 160, (64, 44, 96), 13, 160)
    # bruma
    bruma = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bruma)
    for y in (1380, 1520, 1650):
        bd.rectangle([0, y, W, y + 60], fill=(255, 200, 230, 60))
    im = Image.alpha_composite(im, bruma.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(im)
    montes(1760, 120, (44, 32, 70), 14, 120)
    im.convert("RGB").save(os.path.join(DEST, "fondo_reino.png"))
    print("ok fondo_reino.png")


# ---------------------------------------------------------------- UI
def pergamino():
    c = Lienzo(165, 64)
    c.rect(10, 6, 155, 58, (246, 228, 186, 255), radio=6)
    c.elipse(2, 4, 22, 60, (226, 200, 150, 255))
    c.elipse(143, 4, 163, 60, (226, 200, 150, 255))
    c.guardar("pergamino.png")


def cabeza_icono(tam, nombre, fondo_col=None):
    """Icono: cabeza de unicornio (para app y barra de vida)."""
    c = Lienzo(tam, tam)
    k = tam / 100
    if fondo_col:
        c.rect(0, 0, tam, tam, fondo_col, borde=None, radio=18 * k)
    def P(x, y):
        return (x * k, y * k)
    for i, (x, y) in enumerate([(30, 30), (24, 46), (22, 62), (26, 78)]):
        c.circulo(*P(x, y), 13 * k, ARCOIRIS[i], grosor=W_OUT * k / 2.4)
    c.poligono([P(30, 92), P(40, 40), P(66, 46), P(66, 92)], BLANCO, grosor=W_OUT * k / 2.4)
    c.elipse(*P(34, 22), *P(72, 62), BLANCO, grosor=W_OUT * k / 2.4)
    c.elipse(*P(52, 38), *P(86, 68), (255, 232, 240, 255), grosor=W_OUT * k / 2.4)
    c.poligono([P(48, 22), P(64, 0), P(60, 24)], CUERNO, grosor=W_OUT * k / 2.4)
    c.circulo(*P(36, 22), 9 * k, ARCOIRIS[5], grosor=W_OUT * k / 2.4)
    c.circulo(*P(58, 40), 5 * k, OUT, borde=None)
    c.circulo(*P(56, 38), 1.8 * k, (255, 255, 255, 255), borde=None)
    c.circulo(*P(78, 58), 1.8 * k, OUT, borde=None)
    c.guardar(nombre)


if __name__ == "__main__":
    unicornio("unicornio_quieto.png", {"ad": (0, 0), "at": (0, 0), "pd": (0, 0), "pt": (0, 0)})
    unicornio("unicornio_paso1.png", {"ad": (14, -2), "at": (-12, 0), "pd": (-10, 0), "pt": (12, -2)})
    unicornio("unicornio_paso2.png", {"ad": (-10, 0), "at": (12, -2), "pd": (14, -2), "pt": (-12, 0)})
    unicornio("unicornio_salto.png", {"ad": (22, -16), "at": (-22, -10), "pd": (18, -18), "pt": (-18, -12)})
    troll()
    roca("roca.png", (96, 84, 80, 255))
    roca("roca_ardiente.png", (255, 120, 40, 255), base=(120, 92, 88, 255), brillo=True)
    bola_fuego()
    lobo("lobo1.png", 0)
    lobo("lobo2.png", 1)
    plataforma("plataforma.png", 933, 49, 14, 4)
    plataforma("cornisa.png", 422, 24, 10, 5)
    muralla()
    arbol_magico("arbol_turquesa.png", (110, 220, 210, 255), 1)
    arbol_magico("arbol_rosa.png", (255, 160, 210, 255), 2)
    cristal()
    fondo()
    pergamino()
    cabeza_icono(40, "icono_vida.png")
    cabeza_icono(256, "icono_app.png", fondo_col=(70, 48, 120, 255))
    cabeza_icono(432, "icono_adaptativo.png")
