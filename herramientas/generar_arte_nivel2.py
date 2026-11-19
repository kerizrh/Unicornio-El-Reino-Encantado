"""Arte del nivel extra "La Torre de las Nubes".

Uso:  python generar_arte_nivel2.py <carpeta_del_proyecto>
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

import generar_arte as ga
from generar_arte import Lienzo, OUT, mezcla


def nube_plataforma():
    c = Lienzo(200, 48)
    blanco, sombra = (250, 246, 255, 255), (214, 204, 240, 255)
    for x, y, r in [(30, 26, 18), (62, 18, 20), (100, 14, 22), (140, 18, 20), (172, 26, 18)]:
        c.circulo(x, y, r, blanco)
    c.rect(14, 18, 186, 42, blanco, radio=12)
    c.rect(18, 30, 182, 40, sombra, borde=None, radio=8)
    c.guardar("nube_plataforma.png")


def cristal_fragil():
    c = Lienzo(160, 34)
    pts = [(4, 6), (156, 6), (150, 30), (120, 24), (96, 32), (70, 24), (44, 32), (20, 24), (8, 30)]
    c.poligono(pts, (160, 220, 255, 255))
    c.poligono([(10, 8), (150, 8), (146, 14), (14, 14)], (220, 248, 255, 255), borde=None)
    for a, b in [((40, 8), (52, 22)), ((52, 22), (46, 28)), ((100, 8), (92, 20)), ((92, 20), (106, 26)),
                 ((128, 8), (134, 18))]:
        c.linea([a, b], (90, 130, 200, 255), 1.6)
    c.guardar("cristal_fragil.png")


def plataforma_magica():
    c = Lienzo(180, 34)
    c.rect(2, 4, 178, 30, (196, 150, 84, 255), radio=8)
    c.rect(6, 6, 174, 14, (226, 186, 112, 255), borde=None, radio=5)
    for x in range(22, 170, 34):  # runas brillantes
        c.circulo(x, 20, 5, (140, 240, 255, 255), borde=(60, 120, 170, 255), grosor=1.5)
    c.guardar("plataforma_magica.png")


def hongo_trampolin():
    c = Lienzo(96, 76)
    c.rect(38, 36, 58, 74, (250, 240, 220, 255), radio=6)
    pts = []
    for k in range(25):
        a = math.radians(180 + k * 7.5)
        pts.append((48 + math.cos(a) * 46, 44 + math.sin(a) * 40))
    c.poligono(pts, ga.ARCOIRIS[0])
    for i, col in enumerate(ga.ARCOIRIS[1:5]):
        r = 36 - i * 8
        bandas = []
        for k in range(25):
            a = math.radians(180 + k * 7.5)
            bandas.append((48 + math.cos(a) * r, 44 + math.sin(a) * r * 0.86))
        c.poligono(bandas, col, borde=None)
    for x, y in [(26, 30), (60, 18), (72, 34)]:
        c.circulo(x, y, 4, (255, 255, 255, 255), borde=None)
    c.guardar("hongo_trampolin.png")


def murcielago(nombre, alas_arriba):
    c = Lienzo(90, 56)
    col, osc = (110, 70, 150, 255), (80, 48, 112, 255)
    dy = -14 if alas_arriba else 12
    c.poligono([(40, 26), (6, 26 + dy), (14, 34 + dy * 0.3), (22, 30), (30, 38)], osc)
    c.poligono([(50, 26), (84, 26 + dy), (76, 34 + dy * 0.3), (68, 30), (60, 38)], osc)
    c.elipse(32, 16, 58, 44, col)
    c.poligono([(36, 20), (34, 6), (42, 16)], col)
    c.poligono([(54, 20), (56, 6), (48, 16)], col)
    c.circulo(40, 27, 3.5, (255, 236, 90, 255), borde=None)
    c.circulo(50, 27, 3.5, (255, 236, 90, 255), borde=None)
    c.poligono([(42, 36), (44, 41), (46, 36)], (255, 255, 255, 255), grosor=1)
    c.poligono([(46, 36), (48, 41), (50, 36)], (255, 255, 255, 255), grosor=1)
    c.guardar(nombre)


def fondo_cielo():
    W, H = 1600, 2800
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    arriba, medio, abajo = (16, 12, 48), (70, 50, 130), (240, 150, 190)
    for y in range(H):
        t = y / H
        col = mezcla(arriba, medio, t / 0.6) if t < 0.6 else mezcla(medio, abajo, (t - 0.6) / 0.4)
        d.line([(0, y), (W, y)], fill=col)
    im = im.convert("RGBA")
    d = ImageDraw.Draw(im)
    rnd = random.Random(21)
    for _ in range(420):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.7)
        r = rnd.choice([1, 1, 1.5, 2, 2.5])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 220, rnd.randint(140, 255)))
    # aurora mágica
    aur = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(aur)
    for i, col in enumerate([(120, 255, 200, 70), (150, 170, 255, 60), (255, 140, 220, 50)]):
        pts = [(x, 420 + i * 70 + math.sin(x / 180 + i) * 90) for x in range(0, W + 40, 40)]
        ad.line(pts, fill=col, width=60)
    im = Image.alpha_composite(im, aur.filter(ImageFilter.GaussianBlur(30)))
    # capas de nubes lejanas
    nub = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(nub)
    for capa, (y0, col) in enumerate([(1300, (200, 170, 240, 90)), (1900, (240, 190, 230, 120)),
                                      (2450, (255, 220, 240, 170))]):
        for _ in range(26):
            x = rnd.uniform(-100, W + 100)
            y = y0 + rnd.uniform(-60, 60)
            r = rnd.uniform(60, 140)
            nd.ellipse([x - r * 1.6, y - r * 0.6, x + r * 1.6, y + r * 0.6], fill=col)
    im = Image.alpha_composite(im, nub.filter(ImageFilter.GaussianBlur(8)))
    im.convert("RGB").save(os.path.join(ga.DEST, "fondo_cielo.png"))
    print("ok fondo_cielo.png")


if __name__ == "__main__":
    nube_plataforma()
    cristal_fragil()
    plataforma_magica()
    hongo_trampolin()
    murcielago("murcielago1.png", True)
    murcielago("murcielago2.png", False)
    fondo_cielo()
