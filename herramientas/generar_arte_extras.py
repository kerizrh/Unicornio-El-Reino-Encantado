"""Arte de coleccionables: gema arcoíris (+tiempo) y corazón (+vida).

Uso:  python generar_arte_extras.py <carpeta_del_proyecto>
"""
import math

import generar_arte as ga
from generar_arte import Lienzo


def gema():
    c = Lienzo(40, 44)
    pts = [(20, 2), (36, 14), (20, 42), (4, 14)]
    c.poligono(pts, (150, 230, 255, 255))
    c.poligono([(20, 2), (28, 14), (20, 42), (12, 14)], (255, 170, 230, 255), borde=None)
    c.poligono([(20, 2), (36, 14), (28, 14)], (255, 240, 150, 255), borde=None)
    c.poligono([(4, 14), (12, 14), (20, 42)], (170, 140, 255, 255), borde=None)
    p = pts + [pts[0]]
    c.linea(p, ga.OUT, 2.4)
    c.linea([(4, 14), (36, 14)], ga.OUT, 2)
    c.circulo(14, 9, 2.2, (255, 255, 255, 255), borde=None)
    c.guardar("gema.png")


def corazon():
    c = Lienzo(40, 38)
    pts = []
    for k in range(60):
        t = k / 60 * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((20 + x * 1.1, 18 - y * 1.1))
    c.poligono(pts, (255, 92, 140, 255))
    c.circulo(13, 12, 3.5, (255, 200, 220, 255), borde=None)
    c.guardar("corazon.png")


def aviso():
    c = Lienzo(40, 40)
    c.circulo(20, 20, 17, (255, 120, 50, 255))
    c.rect(17, 8, 23, 24, (255, 250, 220, 255), borde=None, radio=3)
    c.circulo(20, 30, 3.2, (255, 250, 220, 255), borde=None)
    c.guardar("aviso_fuego.png")


if __name__ == "__main__":
    gema()
    corazon()
    aviso()
