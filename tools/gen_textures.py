"""Генератор пиксель-арт текстур для мода «Ты Еж» (оригинальная графика)."""
import math, random
from PIL import Image, ImageDraw

import os
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(_ROOT, "src/main/resources/assets/tyezh/textures/gui/")
ICON_OUT = os.path.join(_ROOT, "src/main/resources/assets/tyezh/icon.png")

def hx(s, a=255):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)

def lerp(c1, c2, t):
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * t)) for i in range(4))

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

def rect(img, x0, y0, x1, y1, c):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=c)

def put(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), c)

def outline(img, col, diag=False):
    """Обводка по краю непрозрачных пикселей."""
    src = img.copy()
    w, h = img.size
    sp = src.load()
    dp = img.load()
    nb = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diag:
        nb += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for y in range(h):
        for x in range(w):
            if sp[x, y][3] == 0:
                for dx, dy in nb:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and sp[nx, ny][3] > 0:
                        dp[x, y] = col
                        break

def paste(dst, src, x, y):
    dst.alpha_composite(src, (x, y))

def ellipse(img, cx, cy, rx, ry, c):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                put(img, x, y, c)

def heart_mask(w, h):
    m = []
    for y in range(h):
        row = []
        for x in range(w):
            u = (x + 0.5) / w * 2.6 - 1.3
            v = 1.25 - (y + 0.5) / h * 2.5
            row.append((u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0)
        m.append(row)
    return m

def heart(w, h, base, light, dark, edge):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    m = heart_mask(w, h)
    for y in range(h):
        for x in range(w):
            if m[y][x]:
                c = base
                if y > h * 0.62:
                    c = dark
                img.putpixel((x, y), c)
    # блик
    ellipse(img, w * 0.3, h * 0.3, max(1.5, w * 0.1), max(1.2, h * 0.09), light)
    if w > 20:
        put(img, int(w * 0.22), int(h * 0.42), light)
    outline(img, edge)
    return img

def sparkle(img, x, y, r, c, core=(255, 255, 255, 255)):
    for i in range(-r, r + 1):
        put(img, x + i, y, c)
        put(img, x, y + i, c)
    put(img, x, y, core)

# ---------------------------------------------------------------- палитра
WIN_BORDER = hx("5B4BC4")
WIN_BODY = hx("FFF3FB")
WIN_SHADOW = hx("7A5BC8", 110)
TITLE_A = hx("9C8CF0")
TITLE_B = hx("D9CEFF")
PINK = hx("FF9ED8")
PINK_L = hx("FFD0EE")
PINK_D = hx("F06CB8")
HOT = hx("E0489A")
CYAN = hx("8FE8FF")
CYAN_D = hx("4FB6E0")
DARK = hx("3A2553")
LINE = hx("4A2E6B")

def window(img, x, y, w, h, body=WIN_BODY):
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rect(shadow, x + 3, y + 3, x + w + 3, y + h + 3, WIN_SHADOW)
    img.alpha_composite(shadow)
    rect(img, x, y, x + w, y + h, WIN_BORDER)
    rect(img, x + 1, y + 1, x + w - 1, y + h - 1, body)
    # заголовок
    for i in range(x + 1, x + w - 1):
        t = (i - x) / max(1, w)
        c = lerp(TITLE_A, TITLE_B, t)
        for j in range(y + 1, y + 11):
            img.putpixel((i, j), c)
    for i in range(x + 1, x + w - 1):
        img.putpixel((i, y + 11), WIN_BORDER)
        img.putpixel((i, y + 2), lerp(TITLE_B, (255, 255, 255, 255), 0.6))
    # кнопки окна
    bx = x + w - 1 - 3 * 8
    for k in range(3):
        cx = bx + k * 8
        rect(img, cx, y + 3, cx + 7, y + 10, WIN_BORDER)
        rect(img, cx + 1, y + 4, cx + 6, y + 9, hx("FFFFFF"))
        g = hx("5B4BC4")
        if k == 0:
            rect(img, cx + 2, y + 7, cx + 5, y + 8, g)
        elif k == 1:
            rect(img, cx + 2, y + 5, cx + 5, y + 6, g)
            put(img, cx + 2, y + 7, g); put(img, cx + 4, y + 7, g)
        else:
            for q in range(4):
                put(img, cx + 2 + q, y + 5 + q, g)
                put(img, cx + 5 - q, y + 5 + q, g)
    return (x + 1, y + 12, x + w - 1, y + h - 1)  # область содержимого

# ---------------------------------------------------------------- небо
def make_sky():
    W, H = 480, 270
    img = Image.new("RGBA", (W, H))
    stops = [(0.0, hx("A996F2")), (0.45, hx("E6B0EC")), (0.8, hx("FFCBE9")), (1.0, hx("FFE1F2"))]
    steps = 14
    for y in range(H):
        t = y / (H - 1)
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                lt = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
                a, b = stops[i][1], stops[i + 1][1]
                break
        q = lt * steps
        base = int(q)
        frac = q - base
        for x in range(W):
            k = base + (1 if frac * 16 > BAYER[y % 4][x % 4] else 0)
            img.putpixel((x, y), lerp(a, b, min(1, k / steps)))
    rnd = random.Random(7)
    for _ in range(90):
        x, y = rnd.randrange(W), rnd.randrange(int(H * 0.7))
        c = rnd.choice([hx("FFFFFF", 200), hx("FFF4C9", 200), hx("D9F6FF", 200)])
        if rnd.random() < 0.25:
            sparkle(img, x, y, 1, c, c)
        else:
            put(img, x, y, c)
    # облака внизу
    cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i in range(22):
        cx = i * 24 + rnd.randrange(-6, 6)
        cy = H - 18 + rnd.randrange(-10, 6)
        r = rnd.randrange(14, 26)
        ellipse(cl, cx, cy, r, r * 0.75, hx("FFF0FA"))
    for i in range(14):
        cx = i * 36 + rnd.randrange(-8, 8)
        cy = H - 4
        ellipse(cl, cx, cy, 22, 14, hx("FFFFFF"))
    # тень облаков
    px = cl.load()
    for y in range(1, H):
        for x in range(W):
            if px[x, y][3] and not px[x, y - 1][3]:
                pass
    img.alpha_composite(cl)
    img.save(OUT + "sky.png")

def cloud(w, h, rnd):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    n = max(3, w // 12)
    for i in range(n):
        cx = w * (0.15 + 0.7 * i / (n - 1))
        r = h * rnd.uniform(0.3, 0.48)
        ellipse(img, cx, h - r - 1, r * 1.1, r, hx("FFFFFF"))
    ellipse(img, w / 2, h * 0.72, w * 0.46, h * 0.28, hx("FFFFFF"))
    # тень снизу
    px = img.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and (y + 3 >= h or px[x, min(h - 1, y + 3)][3] == 0):
                px[x, y] = hx("F7D3F0")
    outline(img, hx("E7B6E6"))
    return img

def make_clouds():
    W, H = 480, 270
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rnd = random.Random(3)
    spots = [(10, 30, 70, 22), (140, 70, 54, 18), (250, 20, 90, 26), (380, 95, 60, 20),
             (60, 150, 80, 24), (300, 175, 70, 22), (420, 210, 50, 16), (180, 225, 64, 20)]
    for x, y, w, h in spots:
        paste(img, cloud(w, h, rnd), x, y)
    img.save(OUT + "clouds.png")

# ---------------------------------------------------------------- ёж (фронтальный)
def star_poly(cx, cy, n, ro_x, ro_y, ri_x, ri_y, rot, a0=-math.pi, a1=math.pi):
    pts = []
    for i in range(n * 2):
        a = rot + i * math.pi / n
        if a0 <= ((a + math.pi) % (2 * math.pi)) - math.pi <= a1 or True:
            if i % 2 == 0:
                pts.append((cx + math.cos(a) * ro_x, cy + math.sin(a) * ro_y))
            else:
                pts.append((cx + math.cos(a) * ri_x, cy + math.sin(a) * ri_y))
    return pts

def hedgehog_big(closed=False):
    W, H = 84, 74
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 42, 38
    # иголки: тёмный слой, основной, светлый
    d.polygon(star_poly(cx, cy + 1, 17, 38, 33, 28, 25, -math.pi / 2), fill=hx("B06BC0"))
    d.polygon(star_poly(cx, cy - 1, 17, 35, 30, 26, 23, -math.pi / 2), fill=hx("EFA6DD"))
    d.polygon(star_poly(cx - 3, cy - 5, 13, 24, 20, 17, 14, -math.pi / 2 + 0.2), fill=hx("F9CDEF"))
    # штрихи на иголках
    for i in range(17):
        a = -math.pi / 2 + i * 2 * math.pi / 17
        for r in range(22, 30):
            x = int(cx + math.cos(a) * r)
            y = int(cy - 1 + math.sin(a) * r * 0.86)
            if img.getpixel((x, y))[3]:
                put(img, x, y, hx("D98BD2"))
    # ушки
    ellipse(img, 25, 26, 6, 6, hx("FFE8D6"))
    ellipse(img, 59, 26, 6, 6, hx("FFE8D6"))
    ellipse(img, 25, 27, 3.2, 3.2, hx("FFB3C9"))
    ellipse(img, 59, 27, 3.2, 3.2, hx("FFB3C9"))
    # мордочка
    ellipse(img, cx, 46, 24, 19, hx("F4CDB8"))
    ellipse(img, cx, 45, 23, 18, hx("FFE8D6"))
    ellipse(img, cx - 6, 39, 9, 6, hx("FFF4EA"))
    # глазки
    for ex in (31, 53):
        if closed:
            for q in range(-3, 4):
                put(img, ex + q, 45 + (1 if abs(q) == 3 else 0), DARK)
        else:
            ellipse(img, ex, 45, 3.6, 5.2, DARK)
            for yy in range(46, 50):
                for xx in range(ex - 3, ex + 4):
                    if img.getpixel((xx, yy)) == DARK:
                        put(img, xx, yy, hx("6A3FA8") if yy < 48 else hx("9A6BE0"))
            rect(img, ex - 2, 41, ex, 43, hx("FFFFFF"))
            put(img, ex + 1, 48, hx("FFFFFF"))
            put(img, ex + 2, 47, hx("E9DBFF"))
    # румянец
    for bx in (23, 57):
        rect(img, bx - 3, 51, bx + 3, 53, hx("FF9CC2"))
        put(img, bx - 2, 51, hx("FFC3DA")); put(img, bx, 51, hx("FFC3DA")); put(img, bx + 2, 51, hx("FFC3DA"))
    # носик
    rect(img, cx - 2, 50, cx + 2, 52, DARK)
    put(img, cx - 1, 50, hx("8C6BB0"))
    # ротик «ω»
    for p in [(-3, 54), (-2, 55), (-1, 55), (0, 54), (1, 55), (2, 55), (3, 54)]:
        put(img, cx + p[0], p[1], hx("B0506E"))
    # лапки на столе
    ellipse(img, 30, 68, 7, 5, hx("F4CDB8"))
    ellipse(img, 54, 68, 7, 5, hx("F4CDB8"))
    for fx in (27, 30, 33, 51, 54, 57):
        put(img, fx, 71, hx("D9A690"))
    # бантик
    bow_c = (63, 11)
    d.polygon([(bow_c[0], bow_c[1]), (bow_c[0] - 8, bow_c[1] - 5), (bow_c[0] - 8, bow_c[1] + 5)], fill=CYAN)
    d.polygon([(bow_c[0], bow_c[1]), (bow_c[0] + 8, bow_c[1] - 5), (bow_c[0] + 8, bow_c[1] + 5)], fill=CYAN)
    put(img, bow_c[0] - 6, bow_c[1] - 2, hx("E4FBFF")); put(img, bow_c[0] + 5, bow_c[1] - 2, hx("E4FBFF"))
    rect(img, bow_c[0] - 1, bow_c[1] - 2, bow_c[0] + 2, bow_c[1] + 2, CYAN_D)
    outline(img, LINE)
    img = img.crop(img.getbbox())
    return img

def hedgehog_head(closed=True, w=30, h=24):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2 + 1
    d.polygon(star_poly(cx, cy, 11, w * 0.48, h * 0.48, w * 0.36, h * 0.36, -math.pi / 2), fill=hx("B06BC0"))
    d.polygon(star_poly(cx, cy - 1, 11, w * 0.44, h * 0.44, w * 0.33, h * 0.33, -math.pi / 2), fill=hx("EFA6DD"))
    ellipse(img, cx, cy + 3, w * 0.3, h * 0.28, hx("FFE8D6"))
    ey = int(cy + 2)
    for ex in (int(cx - 4), int(cx + 3)):
        if closed:
            put(img, ex - 1, ey, DARK); put(img, ex, ey + 1, DARK); put(img, ex + 1, ey, DARK)
        else:
            rect(img, ex - 1, ey - 1, ex + 1, ey + 2, DARK)
            put(img, ex - 1, ey - 1, hx("FFFFFF"))
    put(img, int(cx), ey + 3, DARK); put(img, int(cx) - 1, ey + 3, DARK)
    rect(img, int(cx - 7), ey + 3, int(cx - 5), ey + 4, hx("FF9CC2"))
    rect(img, int(cx + 5), ey + 3, int(cx + 7), ey + 4, hx("FF9CC2"))
    outline(img, LINE)
    return img

def hedgehog_side():
    """Маленький ёжик сбоку (гуляет)."""
    img = Image.new("RGBA", (24, 15), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(2, 11)]
    for i in range(9):
        pts.append((3 + i * 2, 2 + (i % 2) * 2 + (2 if i in (0, 8) else 0)))
    pts += [(20, 9), (18, 11)]
    d.polygon(pts, fill=hx("C98A6A"))
    ellipse(img, 11, 8, 8, 4, hx("A9694E"))
    d.polygon([(15, 7), (22, 10), (15, 12)], fill=hx("F6D8BE"))
    put(img, 22, 10, DARK)
    put(img, 18, 8, DARK)
    rect(img, 5, 12, 7, 14, hx("8C5540")); rect(img, 14, 12, 16, 14, hx("8C5540"))
    outline(img, hx("4B2B25"))
    return img

# ---------------------------------------------------------------- иконки
def icon_apple():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    ellipse(img, 5.5, 9.5, 4.8, 5, hx("FF5C7A"))
    ellipse(img, 10.5, 9.5, 4.8, 5, hx("FF5C7A"))
    ellipse(img, 5, 8, 1.6, 2, hx("FFB0C0"))
    rect(img, 7, 2, 9, 5, hx("7A4A30"))
    ImageDraw.Draw(img).polygon([(9, 3), (14, 1), (12, 5)], fill=hx("7EDC8A"))
    outline(img, LINE)
    return img

def icon_mushroom():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    ellipse(img, 8, 7, 7, 5.5, hx("FF6FB5"))
    rect(img, 1, 7, 15, 9, hx("FF6FB5"))
    for p in [(5, 4), (10, 5), (7, 7), (12, 7), (3, 7)]:
        rect(img, p[0], p[1], p[0] + 2, p[1] + 2, hx("FFFFFF"))
    rect(img, 5, 9, 11, 15, hx("FFF1E0"))
    rect(img, 6, 13, 10, 15, hx("F3D4BF"))
    outline(img, LINE)
    return img

def icon_play():
    img = Image.new("RGBA", (16, 12), (0, 0, 0, 0))
    rect(img, 1, 1, 15, 11, hx("FF5FA8"))
    put(img, 1, 1, (0, 0, 0, 0)); put(img, 14, 1, (0, 0, 0, 0)); put(img, 1, 10, (0, 0, 0, 0)); put(img, 14, 10, (0, 0, 0, 0))
    ImageDraw.Draw(img).polygon([(6, 3), (6, 8), (10, 5.5)], fill=hx("FFFFFF"))
    outline(img, LINE)
    return img

def icon_note():
    img = Image.new("RGBA", (14, 16), (0, 0, 0, 0))
    rect(img, 1, 2, 13, 16, hx("FFFFFF"))
    for y in (6, 9, 12):
        rect(img, 3, y, 11, y + 1, hx("B6A8F5"))
    for x in (3, 6, 9):
        rect(img, x, 0, x + 2, 4, hx("6E5BD6"))
    outline(img, LINE)
    return img

def icon_pad():
    img = Image.new("RGBA", (18, 12), (0, 0, 0, 0))
    ellipse(img, 5, 7, 4.5, 4.2, hx("CFF3FF"))
    ellipse(img, 13, 7, 4.5, 4.2, hx("CFF3FF"))
    rect(img, 5, 3, 13, 11, hx("CFF3FF"))
    rect(img, 4, 6, 7, 7, hx("6E5BD6")); rect(img, 5, 5, 6, 8, hx("6E5BD6"))
    put(img, 12, 6, hx("FF5FA8")); put(img, 14, 7, hx("7EDC8A"))
    outline(img, LINE)
    return img

# ---------------------------------------------------------------- логотип «ТЫ ЕЖ»
GLYPHS = {
    "Т": ["######", "######", "..##..", "..##..", "..##..", "..##..", "..##..", "..##..", "..##.."],
    "Ы": ["##.....##", "##.....##", "##.....##", "#####..##", "######.##", "##..##.##", "##..##.##", "######.##", "#####..##"],
    "Е": ["######", "######", "##....", "##....", "#####.", "#####.", "##....", "######", "######"],
    "Ж": ["##..##..##", "##..##..##", ".##.##.##.", "..######..", "..######..", ".##.##.##.", "##..##..##", "##..##..##", "##..##..##"],
    " ": ["....", "....", "....", "....", "....", "....", "....", "....", "...."],
}

def logo(text="ТЫ ЕЖ", scale=3):
    cols = []
    for i, ch in enumerate(text):
        g = GLYPHS[ch]
        for c in range(len(g[0])):
            cols.append([g[r][c] == "#" for r in range(9)])
        if ch != " " and i + 1 < len(text) and text[i + 1] != " ":
            cols.append([False] * 9)
    w1 = len(cols)
    fillc = [hx("FFFFFF"), hx("FFFFFF"), hx("FFFFFF"), hx("FFF0FA"), hx("CFF6FF"), hx("FFE0F3"),
             hx("FFCDEB"), hx("FFBCE4"), hx("FFABDD")]
    pad = 4
    W, H = w1 * scale + pad * 2, 9 * scale + pad * 2
    letters = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for x in range(w1):
        for y in range(9):
            if cols[x][y]:
                c = fillc[y]
                for dx in range(scale):
                    for dy in range(scale):
                        put(letters, pad + x * scale + dx, pad + y * scale + dy, c)
    # блик на верхней кромке букв
    lp = letters.load()
    for x in range(W):
        for y in range(1, H):
            if lp[x, y][3] and lp[x, y - 1][3] == 0:
                pass
    outline(letters, hx("FF5FA8"))
    outline(letters, hx("FF5FA8"))
    outline(letters, hx("FFFFFF"))
    outline(letters, hx("7A4FC8"), diag=True)
    res = Image.new("RGBA", (W + 3, H + 3), (0, 0, 0, 0))
    shadow = Image.new("RGBA", letters.size, (0, 0, 0, 0))
    sp = shadow.load()
    for y in range(H):
        for x in range(W):
            if lp[x, y][3]:
                sp[x, y] = hx("6A4FC0", 170)
    res.alpha_composite(shadow, (3, 3))
    res.alpha_composite(letters, (0, 0))
    return res.crop(res.getbbox())

# ---------------------------------------------------------------- милкшейк
def milkshake():
    img = Image.new("RGBA", (30, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # соломинка
    for i in range(22):
        x, y = 19 + i // 4, 18 - i * 0.8
        c = hx("FF6FB5") if (i // 3) % 2 == 0 else hx("FFFFFF")
        rect(img, int(x), int(y), int(x) + 2, int(y) + 2, c)
    # бокал
    d.polygon([(3, 16), (26, 16), (21, 40), (8, 40)], fill=hx("D9F6FF", 235))
    d.polygon([(5, 22), (24, 22), (20, 39), (9, 39)], fill=hx("FF8FC8"))
    d.polygon([(6, 30), (22, 30), (20, 39), (9, 39)], fill=hx("FF6FB5"))
    rect(img, 13, 40, 17, 49, hx("D9F6FF", 235))
    rect(img, 7, 49, 23, 52, hx("D9F6FF", 235))
    rect(img, 6, 17, 8, 36, hx("FFFFFF", 200))
    # сливки
    ellipse(img, 14.5, 15, 11, 5, hx("FFFFFF"))
    ellipse(img, 14.5, 10, 7, 4, hx("FFFFFF"))
    ellipse(img, 14.5, 7, 4, 3, hx("FFF7FB"))
    for p in [(8, 13), (12, 9), (18, 12), (21, 15)]:
        put(img, p[0], p[1], hx("FFD6EC"))
    # вишенка
    ellipse(img, 15, 3.5, 3, 3, hx("FF3F6E"))
    put(img, 14, 2, hx("FFC1CF"))
    put(img, 17, 0, hx("5C8A3A"))
    # посыпка
    for p, c in [((9, 11), CYAN), ((20, 14), hx("FFE36E")), ((13, 13), hx("B38CFF")), ((17, 9), CYAN)]:
        put(img, p[0], p[1], c)
    outline(img, LINE)
    return img

# ---------------------------------------------------------------- панель
def make_panel():
    W, H = 400, 225
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # ---------- главное окно
    cx0, cy0, cx1, cy1 = window(img, 126, 18, 232, 194)
    # стена
    for y in range(cy0, cy1):
        t = (y - cy0) / (cy1 - cy0)
        a = hx("B9A6FF"); b = hx("FFC9EE")
        for x in range(cx0, cx1):
            k = int(t * 10 + (1 if (t * 10 % 1) * 16 > BAYER[y % 4][x % 4] else 0))
            img.putpixel((x, y), lerp(a, b, min(1, k / 10)))
    # узор: мелкие ромбики
    for y in range(cy0 + 4, cy1 - 30, 12):
        for x in range(cx0 + 4 + (6 if (y // 12) % 2 else 0), cx1 - 2, 12):
            put(img, x, y, hx("FFFFFF", 90)); put(img, x + 1, y + 1, hx("FFFFFF", 60))
            put(img, x - 1, y + 1, hx("FFFFFF", 60)); put(img, x, y + 2, hx("FFFFFF", 90))
    # окошко с луной
    wx, wy = 136, 40
    rect(img, wx, wy, wx + 36, wy + 40, hx("6E5BD6"))
    rect(img, wx + 2, wy + 2, wx + 34, wy + 38, hx("3B2C7A"))
    for y in range(wy + 2, wy + 38):
        t = (y - wy) / 40
        for x in range(wx + 2, wx + 34):
            img.putpixel((x, y), lerp(hx("3B2C7A"), hx("8E5BC8"), t))
    ellipse(img, wx + 24, wy + 12, 6, 6, hx("FFF4C9"))
    ellipse(img, wx + 21, wy + 10, 5, 5, lerp(hx("3B2C7A"), hx("8E5BC8"), 0.25))
    for p in [(wx + 8, wy + 8), (wx + 12, wy + 22), (wx + 28, wy + 28), (wx + 6, wy + 31)]:
        sparkle(img, p[0], p[1], 1, hx("FFFFFF", 200))
    rect(img, wx + 17, wy + 2, wx + 19, wy + 38, hx("6E5BD6"))
    rect(img, wx + 2, wy + 19, wx + 34, wy + 21, hx("6E5BD6"))
    rect(img, wx - 2, wy + 40, wx + 38, wy + 43, hx("FFFFFF"))

    # сердце за логотипом
    hrt = heart(104, 84, PINK, PINK_L, hx("F58CCB"), HOT)
    paste(img, hrt, 232 - 52, 29)
    # логотип
    lg = logo()
    paste(img, lg, 232 - lg.width // 2, 53)


    # стойка
    for y in range(186, cy1):
        for x in range(cx0, cx1):
            if y < 189:
                c = hx("E6FBFF")
            elif y < 191:
                c = hx("8FD3F4")
            else:
                c = hx("7BC3EC") if ((x + y) // 3) % 5 else hx("A4E0F8")
            img.putpixel((x, y), c)
    rect(img, cx0, 189, cx1, 190, hx("5B8FD6"))

    ms = milkshake()
    paste(img, ms, 150, 188 - ms.height + 3)
    ap = icon_apple()
    paste(img, ap, 184, 188 - 14)

    # сердечки в заголовке главного окна
    HB = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
    for k in range(3):
        for yy, row in enumerate(HB):
            for xx, ch in enumerate(row):
                if ch == "#":
                    put(img, 131 + k * 10 + xx, 22 + yy, hx("FF5FA8") if yy > 0 or xx not in (1,) else hx("FFFFFF"))
        put(img, 132 + k * 10, 23, hx("FFFFFF"))

    # ---------- левое верхнее окно
    ax0, ay0, ax1, ay1 = window(img, 6, 10, 112, 104)
    # фотка: лесная полянка
    px0, py0, px1, py1 = 34, 26, 114, 108
    rect(img, px0 - 1, py0 - 1, px1 + 1, py1 + 1, hx("6E5BD6"))
    for y in range(py0, py1):
        t = (y - py0) / (py1 - py0)
        for x in range(px0, px1):
            img.putpixel((x, y), lerp(hx("BFE9FF"), hx("FFD6F0"), t))
    ellipse(img, 98, 40, 6, 6, hx("FFF4C9"))
    paste(img, cloud(30, 12, random.Random(1)), 40, 34)
    for x in range(px0, px1):
        hh = int(90 + 6 * math.sin(x / 9.0))
        for y in range(hh, py1):
            img.putpixel((x, y), hx("9BE3A8") if y < hh + 2 else hx("7ACB8C"))
    for tx in (44, 58, 104):
        rect(img, tx, 74, tx + 3, 92, hx("9C6B55"))
        ellipse(img, tx + 1.5, 70, 7, 9, hx("6FC48A"))
        ellipse(img, tx - 1, 67, 3, 3, hx("A8E8B5"))
    hs = hedgehog_side()
    paste(img, hs, 70, 90)
    for p in [(66, 101), (92, 100), (100, 97)]:
        put(img, p[0], p[1], hx("FF9ED8")); put(img, p[0] + 1, p[1], hx("FFE36E"))
    # иконки слева
    paste(img, icon_apple(), 12, 26)
    paste(img, icon_mushroom(), 12, 46)
    paste(img, icon_play(), 12, 66)
    paste(img, icon_note(), 13, 82)
    paste(img, icon_pad(), 11, 99)

    # ---------- левое нижнее окно (ежата)
    bx0, by0, bx1, by1 = window(img, 6, 146, 112, 68)
    for y in range(by0, by1):
        t = (y - by0) / (by1 - by0)
        for x in range(bx0, bx1):
            img.putpixel((x, y), lerp(hx("FFF3FB"), hx("E7DCFF"), t))
    # одеялко
    for x in range(bx0, bx1):
        for y in range(196, by1):
            c = hx("FFB8E0") if ((x // 5) + (y // 5)) % 2 == 0 else hx("FFD6EE")
            img.putpixel((x, y), c)
    rect(img, bx0, 195, bx1, 197, hx("FFFFFF"))
    for i, (hx_, closed) in enumerate([(22, True), (50, False), (78, True)]):
        head = hedgehog_head(closed)
        paste(img, head, hx_, 196 - head.height + 7)
    # вернём одеяло поверх подбородков
    for x in range(bx0, bx1):
        for y in range(200, by1):
            c = hx("FFB8E0") if ((x // 5) + (y // 5)) % 2 == 0 else hx("FFD6EE")
            img.putpixel((x, y), c)
    rect(img, bx0, 199, bx1, 201, hx("FFFFFF"))
    # «z z»
    zc = hx("8E7BE8")
    for zx, zy in [(40, 166), (46, 162), (96, 168)]:
        rect(img, zx, zy, zx + 4, zy + 1, zc); put(img, zx + 2, zy + 1, zc); put(img, zx + 1, zy + 2, zc)
        rect(img, zx, zy + 3, zx + 4, zy + 4, zc)

    # ---------- окно статуса (правое верхнее)
    window(img, 318, 2, 78, 64)

    # ---------- декор
    paste(img, heart(22, 18, PINK, PINK_L, hx("F58CCB"), HOT), 368, 204)
    paste(img, heart(12, 10, CYAN, hx("E4FBFF"), CYAN_D, hx("3A8FC0")), 118, 124)
    paste(img, heart(10, 9, PINK, PINK_L, hx("F58CCB"), HOT), 110, 212)
    # пузырь с ёжиком
    bub = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    ellipse(bub, 12, 12, 11, 11, hx("FFFFFF"))
    ellipse(bub, 12, 13, 9, 9, hx("FFF0FA"))
    outline(bub, hx("B6A8F5"))
    paste(img, bub, 334, 199)
    fh = hedgehog_head(False, 20, 16)
    paste(img, fh, 336, 203)
    for p in [(122, 12), (360, 72), (8, 132), (300, 8), (392, 128), (118, 218), (212, 214)]:
        sparkle(img, p[0], p[1], 2, hx("FFFFFF"), hx("FFFFFF"))
        put(img, p[0] + 1, p[1] + 1, hx("CFF6FF"))
    img.save(OUT + "panel.png")

def make_hedgehog():
    hb = hedgehog_big(False)
    hb.save(OUT + "hedgehog.png")
    hedgehog_big(True).save(OUT + "hedgehog_blink.png")
    return hb

def make_icon():
    hb = hedgehog_big(False)
    s = 128
    ic = Image.new("RGBA", (s, s), hx("FFD6EE"))
    bg = heart(120, 100, PINK, PINK_L, hx("F58CCB"), HOT)
    ic.alpha_composite(bg, (4, 16))
    small = hb.resize((hb.width, hb.height), Image.NEAREST)
    ic.alpha_composite(small, ((s - small.width) // 2, s - small.height - 6))
    ic.save(ICON_OUT)

if __name__ == "__main__":
    make_sky()
    make_clouds()
    make_panel()
    hb = make_hedgehog()
    print("hedgehog size", hb.size)
    make_icon()
    # превью композиции
    sky = Image.open(OUT + "sky.png").convert("RGBA")
    clouds = Image.open(OUT + "clouds.png").convert("RGBA")
    sky.alpha_composite(clouds)
    panel = Image.open(OUT + "panel.png")
    prev = sky.resize((800, 450), Image.NEAREST)
    comp = panel.resize((784, 441), Image.NEAREST)
    prev.alpha_composite(comp, (8, 4))
    prev.save(os.path.join(_ROOT, "docs/preview_raw.png"))
