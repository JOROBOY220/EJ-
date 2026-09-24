"""Синтез звуков интерфейса «Ты Еж» (оригинальные, сгенерированы кодом).

hover.ogg  — мягкий «блип» при наведении на кнопку
click.ogg  — «поп» + колокольчик при нажатии (заменяет ванильный клик)
snuff1/2   — «фыр-фыр» ёжика (пасхалка: клик по ёжику в главном меню)

Запуск: python3 tools/gen_sounds.py (нужны numpy и ffmpeg с libvorbis).
"""
import os
import subprocess
import tempfile
import wave

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "src/main/resources/assets/tyezh/sounds/ui/")
os.makedirs(OUT, exist_ok=True)
SR = 44100
rng = np.random.default_rng(7)


def t_axis(sec):
    return np.arange(int(SR * sec)) / SR


def env(n, attack=0.004, decay=0.05):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / decay)


def sweep(f0, f1, sec):
    t = t_axis(sec)
    f = np.linspace(f0, f1, len(t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def bell(freq, sec, decay):
    t = t_axis(sec)
    s = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2.01 * t)
         + 0.12 * np.sin(2 * np.pi * freq * 3.03 * t))
    return s * env(len(t), 0.002, decay)


def bandpass_noise(sec, lo, hi):
    n = int(SR * sec)
    x = rng.standard_normal(n)
    spec = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(n, 1 / SR)
    spec[(freqs < lo) | (freqs > hi)] = 0
    return np.fft.irfft(spec, n)


def place(buf, sig, at):
    i = int(at * SR)
    end = min(len(buf), i + len(sig))
    buf[i:end] += sig[:end - i]


def export(sig, name, peak_db=-3.0):
    sig = sig / (np.max(np.abs(sig)) + 1e-9) * (10 ** (peak_db / 20))
    fade = min(len(sig), int(0.004 * SR))
    sig[-fade:] *= np.linspace(1, 0, fade)
    pcm = (sig * 32767).astype(np.int16)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        path = tmp.name
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-c:a", "libvorbis",
                    "-q:a", "5", "-ac", "1", OUT + name + ".ogg"], check=True)
    os.remove(path)


def make_hover():
    s = sweep(1150, 1650, 0.075)
    s += 0.25 * sweep(2300, 3300, 0.075)
    export(s * env(len(s), 0.003, 0.025), "hover", -6)


def make_click():
    buf = np.zeros(int(SR * 0.32))
    pop = sweep(380, 950, 0.03)
    place(buf, pop * env(len(pop), 0.001, 0.012) * 0.9, 0)
    place(buf, bell(1318.5, 0.25, 0.07) * 0.55, 0.018)   # E6
    place(buf, bell(1975.5, 0.25, 0.09) * 0.45, 0.055)  # B6
    export(buf, "click", -3)


def make_snuff(variant):
    buf = np.zeros(int(SR * 0.42))
    starts = [0.0, 0.085, 0.165] if variant == 1 else [0.0, 0.07, 0.13, 0.2]
    for i, st in enumerate(starts):
        n = bandpass_noise(0.055, 1300 + 250 * i, 4200)
        e = env(len(n), 0.006, 0.02)
        place(buf, n * e * (1.0 - 0.12 * i), st)
    squeak = sweep(1900, 2500 if variant == 1 else 2200, 0.06)
    place(buf, squeak * env(len(squeak), 0.004, 0.025) * 0.18, starts[-1] + 0.07)
    export(buf, "snuff%d" % variant, -4)


if __name__ == "__main__":
    make_hover()
    make_click()
    make_snuff(1)
    make_snuff(2)
    print("ok")
