"""Compone y sintetiza la musica (bucle perfecto) y los efectos del juego.

Uso:  python generar_audio.py <carpeta_del_proyecto>
Crea: assets/audio/musica/reino_encantado.wav, assets/audio/efectos/salto.wav, golpe.wav
"""
import os
import sys
import wave

import numpy as np

SR = 22050
PROYECTO = sys.argv[1] if len(sys.argv) > 1 else "."
BPM = 100
BEAT = 60 / BPM


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def laud(f, dur, vol=0.5):
    """Cuerda pulsada: suma de armonicos que se apagan (los agudos antes)."""
    n = int(SR * (dur + 1.2))
    t = np.arange(n) / SR
    s = np.zeros(n)
    for k, a in enumerate([1, 0.5, 0.33, 0.22, 0.12, 0.08], start=1):
        s += a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (2.2 + k * 1.6))
    ataque = np.minimum(1, t / 0.004)
    return vol * s * ataque


def flauta(f, dur, vol=0.32):
    n = int(SR * (dur + 0.15))
    t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.25)
    fase = 2 * np.pi * f * np.cumsum(vib) / SR
    s = np.sin(fase) + 0.18 * np.sin(2 * fase) + 0.06 * np.sin(3 * fase)
    env = np.minimum(1, t / 0.05) * np.clip((dur + 0.15 - t) / 0.15, 0, 1)
    ruido = np.random.default_rng(1).normal(0, 0.02, n) * env
    return vol * (s * env + ruido)


def pad(fs, dur, vol=0.07):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.003 * t) for f in fs)
    env = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    return vol * s * env


def tambor(fuerte=True):
    n = int(SR * 0.35)
    t = np.arange(n) / SR
    f = 90 * np.exp(-t * 8) + 50
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)
    s += np.random.default_rng(2).normal(0, 1, n) * np.exp(-t * 40) * 0.25
    return s * (0.55 if fuerte else 0.22)


def cascabel():
    n = int(SR * 0.12)
    t = np.arange(n) / SR
    s = np.random.default_rng(3).normal(0, 1, n)
    s = np.diff(s, prepend=0)  # agudo
    return s * np.exp(-t * 45) * 0.06


# ------------------------------------------------------------- partitura (Re dorico)
A4, C5, Cs5, D5, E5, F5, G5, A5, Bb5, C6, D6 = 69, 72, 73, 74, 76, 77, 79, 81, 82, 84, 86
SECCION_A = [
    [(A4, 1), (D5, 1), (F5, 1.5), (E5, .5)],
    [(E5, 1), (C5, 1), (E5, 1), (G5, 1)],
    [(F5, 1.5), (E5, .5), (D5, 1), (F5, 1)],
    [(E5, 2), (Cs5, 1), (A4, 1)],
]
SECCION_B = [
    [(D5, .5), (E5, .5), (F5, 1), (A5, 1), (G5, .5), (F5, .5)],
    [(E5, 1), (G5, 1), (C6, 1), (G5, 1)],
    [(D6, 1.5), (C6, .5), (Bb5, 1), (F5, 1)],
    [(A5, 2), (G5, .5), (F5, .5), (E5, 1)],
]
SECCION_B2 = SECCION_B[:3] + [[(A5, 1), (E5, 1), (Cs5, 1), (A4, 1)]]
ACORDES = [  # (bajo arpegiado, notas del pad)
    ([50, 57, 62, 57], [62, 65, 69]),   # Rem
    ([48, 55, 60, 55], [60, 64, 67]),   # Do
    ([46, 53, 58, 53], [58, 62, 65]),   # Sib
    ([45, 52, 57, 61], [57, 61, 64]),   # La
]

compases = SECCION_A + SECCION_B + SECCION_A + SECCION_B2
COMPAS = 4 * BEAT
total = int(SR * COMPAS * len(compases))
mezcla = np.zeros(total + SR * 3)


def poner(senal, t0):
    i = int(t0 * SR)
    mezcla[i:i + len(senal)] += senal


for c, notas in enumerate(compases):
    t_compas = c * COMPAS
    bajo, acorde = ACORDES[c % 4]
    instrumento = laud if (c // 4) % 2 == 0 else flauta
    t = t_compas
    for midi, beats in notas:
        poner(instrumento(hz(midi), beats * BEAT), t)
        if instrumento is flauta:
            poner(laud(hz(midi - 12), beats * BEAT, 0.12), t)
        t += beats * BEAT
    for k in range(8):  # arpegio de arpa en corcheas
        poner(laud(hz(bajo[k % 4]), BEAT / 2, 0.22 if k % 2 == 0 else 0.15), t_compas + k * BEAT / 2)
    poner(pad([hz(m) for m in acorde], COMPAS + 0.4), t_compas)
    for b in range(4):
        poner(tambor(b % 2 == 0), t_compas + b * BEAT)
        poner(cascabel(), t_compas + b * BEAT + BEAT / 2)

# bucle perfecto: lo que sobra despues del final se suma al inicio
cola = mezcla[total:]
mezcla = mezcla[:total]
mezcla[:len(cola)] += cola
# reverberacion sencilla (ecos) aplicada de forma circular
eco = np.zeros_like(mezcla)
for retardo, g in [(0.11, 0.25), (0.23, 0.15), (0.37, 0.08)]:
    eco += np.roll(mezcla, int(retardo * SR)) * g
mezcla = mezcla + eco
mezcla = np.tanh(mezcla / np.max(np.abs(mezcla)) * 1.2) * 0.85


def guardar(ruta, datos):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    pcm = (np.clip(datos, -1, 1) * 32767).astype(np.int16)
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("ok", ruta, f"{len(datos) / SR:.1f}s")


base = os.path.join(PROYECTO, "assets", "audio")
guardar(os.path.join(base, "musica", "reino_encantado.wav"), mezcla)

# ------------------------------------------------------------- victoria y derrota
def componer(compases, acordes, bpm, melodia_fn, vol_bajo=0.2, percusion=True, eco_g=0.25):
    """Sintetiza una pieza que enlaza el final con el inicio (bucle perfecto)."""
    beat = 60 / bpm
    compas = 4 * beat
    n = int(SR * compas * len(compases))
    buf = np.zeros(n + SR * 3)

    def put(s, t0):
        i = int(t0 * SR)
        buf[i:i + len(s)] += s

    for c, notas in enumerate(compases):
        t0 = c * compas
        bajo, acorde = acordes[c % len(acordes)]
        t = t0
        for midi, beats in notas:
            put(melodia_fn(hz(midi), beats * beat), t)
            t += beats * beat
        for k in range(8):
            put(laud(hz(bajo[k % 4]), beat / 2, vol_bajo if k % 2 == 0 else vol_bajo * 0.7), t0 + k * beat / 2)
        put(pad([hz(m) for m in acorde], compas + 0.4), t0)
        if percusion:
            for b in range(4):
                put(tambor(b % 2 == 0), t0 + b * beat)
    cola_ = buf[n:]
    buf = buf[:n]
    buf[:len(cola_)] += cola_
    eco_ = np.zeros_like(buf)
    for retardo, g in [(0.13, eco_g), (0.29, eco_g * 0.6), (0.47, eco_g * 0.3)]:
        eco_ += np.roll(buf, int(retardo * SR)) * g
    buf = buf + eco_
    return np.tanh(buf / np.max(np.abs(buf)) * 1.2) * 0.85


def trompeta(f, dur, vol=0.3):
    """Metal brillante: armónicos con ataque suave y vibrato."""
    n = int(SR * (dur + 0.12))
    t = np.arange(n) / SR
    vib = 1 + 0.005 * np.sin(2 * np.pi * 6 * t) * np.minimum(1, t / 0.2)
    fase = 2 * np.pi * f * np.cumsum(vib) / SR
    s = sum((0.8 ** k) * np.sin(k * fase) for k in range(1, 8))
    env = np.minimum(1, t / 0.03) * np.clip((dur + 0.12 - t) / 0.12, 0, 1)
    return vol * 0.35 * s * env


Fs5, B5, A4b, Bb4, D4 = 78, 83, 69, 70, 62
# Fanfarria triunfal en Re mayor (100 bpm, 4 compases)
VICTORIA = [
    [(D5, .5), (D5, .5), (D5, .5), (Fs5, .5), (A5, 2)],
    [(Fs5, .5), (G5, .5), (A5, .5), (B5, .5), (A5, 2)],
    [(D6, 1.5), (B5, .5), (A5, 1), (Fs5, 1)],
    [(G5, 1), (E5, 1), (D5, 2)],
]
ACORDES_VICTORIA = [
    ([50, 57, 62, 66], [62, 66, 69]),   # Re
    ([55, 62, 67, 62], [62, 67, 71]),   # Sol
    ([50, 57, 62, 66], [62, 66, 69]),   # Re
    ([45, 52, 57, 61], [61, 64, 69]),   # La
]
guardar(os.path.join(base, "musica", "victoria.wav"),
        componer(VICTORIA * 2, ACORDES_VICTORIA, 112, trompeta, vol_bajo=0.22))

# Lamento lento en Re menor (66 bpm, 4 compases) para el Game Over
DERROTA = [
    [(A5, 1.5), (G5, .5), (F5, 1), (E5, 1)],
    [(D5, 3), (Cs5, 1)],
    [(F5, 1.5), (E5, .5), (D5, 1), (Bb4, 1)],
    [(A4b, 4)],
]
ACORDES_DERROTA = [
    ([50, 57, 62, 57], [62, 65, 69]),   # Rem
    ([45, 52, 57, 61], [57, 61, 64]),   # La
    ([46, 53, 58, 53], [58, 62, 65]),   # Sib
    ([45, 52, 57, 52], [57, 61, 64]),   # La
]
guardar(os.path.join(base, "musica", "derrota.wav"),
        componer(DERROTA, ACORDES_DERROTA, 66, flauta, vol_bajo=0.16, percusion=False, eco_g=0.35))

# ------------------------------------------------------------- efectos
t = np.arange(int(SR * 0.28)) / SR
f = 500 + 1400 * t / t[-1]
salto = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
salto += 0.3 * np.sin(2 * np.pi * np.cumsum(f * 2) / SR) * np.exp(-t * 14)
guardar(os.path.join(base, "efectos", "salto.wav"), salto * 0.45)

t = np.arange(int(SR * 0.45)) / SR
f = 160 * np.exp(-t * 6) + 40
golpe = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
golpe += np.random.default_rng(5).normal(0, 1, len(t)) * np.exp(-t * 25) * 0.5
guardar(os.path.join(base, "efectos", "golpe.wav"), np.tanh(golpe * 1.5) * 0.7)

# cristal que se rompe: tintineos agudos con ruido
t = np.arange(int(SR * 0.6)) / SR
cristal = np.random.default_rng(8).normal(0, 1, len(t)) * np.exp(-t * 30) * 0.4
for i, f in enumerate([2093, 2637, 3136, 3951, 2349]):
    t0 = int(i * 0.045 * SR)
    seg = np.sin(2 * np.pi * f * t[: len(t) - t0]) * np.exp(-t[: len(t) - t0] * 12) * 0.3
    cristal[t0:] += seg
guardar(os.path.join(base, "efectos", "cristal.wav"), np.tanh(cristal) * 0.6)

# rebote del hongo: "boing" que sube
t = np.arange(int(SR * 0.5)) / SR
f = 180 + 520 * (1 - np.exp(-t * 9))
vib = 1 + 0.08 * np.sin(2 * np.pi * 22 * t) * np.exp(-t * 4)
rebote = np.sin(2 * np.pi * np.cumsum(f * vib) / SR) * np.exp(-t * 5)
guardar(os.path.join(base, "efectos", "rebote.wav"), rebote * 0.6)

# brillo al recoger una gema: arpegio rápido ascendente
partes = []
for f in [1319, 1568, 1976, 2637]:
    t = np.arange(int(SR * 0.07)) / SR
    partes.append(np.sin(2 * np.pi * f * t) * np.exp(-t * 18))
t = np.arange(int(SR * 0.35)) / SR
partes.append(np.sin(2 * np.pi * 3136 * t) * np.exp(-t * 9))
guardar(os.path.join(base, "efectos", "brillo.wav"), np.concatenate(partes) * 0.4)

# rugido del troll: sierra grave con trémolo y ruido
t = np.arange(int(SR * 1.3)) / SR
f = 70 + 30 * np.sin(np.pi * t / 1.3)
fase = 2 * np.pi * np.cumsum(f) / SR
sierra = sum(np.sin(k * fase) / k for k in range(1, 12))
ruido = np.random.default_rng(9).normal(0, 1, len(t))
ruido = np.convolve(ruido, np.ones(30) / 30, mode="same")
env = np.minimum(1, t / 0.15) * np.clip((1.3 - t) / 0.4, 0, 1) * (0.8 + 0.2 * np.sin(2 * np.pi * 18 * t))
guardar(os.path.join(base, "efectos", "rugido.wav"), np.tanh((sierra * 0.6 + ruido * 2.5) * env * 1.5) * 0.7)
