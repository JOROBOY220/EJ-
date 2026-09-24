"""Генератор текстур интерфейса «Ты Еж»: стиль ванильных кнопок, слайдеров,
полей ввода, вкладок, списков + спрайты ёжика для экранов загрузки.

Ванильные текстуры переопределяются через assets/minecraft/..., поэтому
стиль автоматически применяется ко ВСЕМ экранам (настройки, выбор и создание
мира, меню паузы и т.д.). Запуск: python3 tools/gen_ui.py (нужен Pillow).
"""
import json
import math
import os

from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MC = os.path.join(ROOT, "src/main/resources/assets/minecraft/textures/gui/")
WIDGET = os.path.join(MC, "sprites/widget/")
OWN = os.path.join(ROOT, "src/main/resources/assets/tyezh/textures/gui/")
os.makedirs(WIDGET, exist_ok=True)
os.makedirs(OWN, exist_ok=True)


def hx(s, a=255):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)


def lerp(c1, c2, t):
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * t)) for i in range(4))


def put(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), c)


def rect(img, x0, y0, x1, y1, c):
    if x1 > x0 and y1 > y0:
        ImageDraw.Draw(img).rectangle([x0, y0, x1 - 1, y1 - 1], fill=c)


def save_sprite(img, name, mcmeta):
    img.save(WIDGET + name + ".png")
    with open(WIDGET + name + ".png.mcmeta", "w", encoding="utf-8") as f:
        json.dump({"gui": {"scaling": mcmeta}}, f, indent=2)


def nine(w, h, border):
    return {"type": "nine_slice", "width": w, "height": h, "border": border}


# ------------------------------------------------------------------ кнопки
def candy(w, h, border, top, bottom, hilite, shade, rounded=True):
    """Пастельная «конфетная» кнопка: рамка, градиент, блик сверху, тень снизу."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rect(img, 0, 0, w, h, border)
    for y in range(1, h - 1):
        c = lerp(top, bottom, (y - 1) / max(1, h - 3))
        rect(img, 1, y, w - 1, y + 1, c)
    rect(img, 1, 1, w - 1, 2, hilite)
    put(img, 1, 2, hilite)
    put(img, w - 2, 2, hilite)
    rect(img, 1, h - 2, w - 1, h - 1, shade)
    if rounded:
        for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
            put(img, x, y, (0, 0, 0, 0))
    return img


def make_buttons():
    b = nine(200, 20, 3)
    save_sprite(candy(200, 20, hx("4A3A9A"), hx("B3A5F7"), hx("8876E4"), hx("D9CEFF"), hx("6E5BD6")), "button", b)
    save_sprite(candy(200, 20, hx("FFFFFF"), hx("FFA3D6"), hx("F06CB8"), hx("FFD6EE"), hx("C94F97")), "button_highlighted", b)
    save_sprite(candy(200, 20, hx("8A84A8"), hx("D3CDE6"), hx("BDB6D6"), hx("E6E1F3"), hx("A9A2C4")), "button_disabled", b)


def make_sliders():
    b = nine(200, 20, 3)
    track = candy(200, 20, hx("4A3A9A"), hx("5B4BC4"), hx("6E5BD6"), hx("3F318F"), hx("8876E4"))
    save_sprite(track, "slider", b)
    track_h = candy(200, 20, hx("FFFFFF"), hx("6A56D0"), hx("7C68E0"), hx("4A3A9A"), hx("9C8CF0"))
    save_sprite(track_h, "slider_highlighted", b)
    hb = nine(8, 20, 2)
    save_sprite(candy(8, 20, hx("4A3A9A"), hx("FFD0EE"), hx("FF9ED8"), hx("FFFFFF"), hx("E07BBE")), "slider_handle", hb)
    save_sprite(candy(8, 20, hx("FFFFFF"), hx("FFE3F4"), hx("FFB8E0"), hx("FFFFFF"), hx("F06CB8")), "slider_handle_highlighted", hb)


def make_text_fields():
    b = nine(200, 20, 1)
    for name, edge in [("text_field", hx("9C8CF0")), ("text_field_highlighted", hx("FF9ED8"))]:
        img = Image.new("RGBA", (200, 20), (0, 0, 0, 0))
        rect(img, 0, 0, 200, 20, edge)
        rect(img, 1, 1, 199, 19, hx("2A1E5E"))
        save_sprite(img, name, b)


def make_tabs():
    b = nine(130, 24, {"left": 2, "top": 2, "right": 2, "bottom": 0})

    def tab(border, top, bottom, line):
        img = Image.new("RGBA", (130, 24), (0, 0, 0, 0))
        rect(img, 0, 0, 130, 24, border)
        for y in range(1, 24):
            rect(img, 1, y, 129, y + 1, lerp(top, bottom, (y - 1) / 22))
        rect(img, 1, 1, 129, 2, line)
        put(img, 0, 0, (0, 0, 0, 0))
        put(img, 129, 0, (0, 0, 0, 0))
        return img

    save_sprite(tab(hx("4A3A9A"), hx("9C8CF0"), hx("7C68E0"), hx("C5B8FF")), "tab", b)
    save_sprite(tab(hx("FFFFFF"), hx("B3A5F7"), hx("9C8CF0"), hx("FFD6EE")), "tab_highlighted", b)
    save_sprite(tab(hx("4A3A9A"), hx("C5B8FF"), hx("B3A5F7"), hx("FF9ED8")), "tab_selected", b)
    save_sprite(tab(hx("FFFFFF"), hx("D9CEFF"), hx("C5B8FF"), hx("FF6FB5")), "tab_selected_highlighted", b)


def make_scroller():
    b = nine(6, 32, 1)
    img = Image.new("RGBA", (6, 32), (0, 0, 0, 0))
    rect(img, 0, 0, 6, 32, hx("FFFFFF"))
    rect(img, 1, 1, 5, 31, hx("FF9ED8"))
    rect(img, 1, 1, 3, 31, hx("FFC4E6"))
    save_sprite(img, "scroller", b)
    bg = Image.new("RGBA", (6, 32), hx("2A1E5E", 170))
    save_sprite(bg, "scroller_background", b)


# ------------------------------------------------------------------ фоны списков и разделители
def make_backgrounds():
    lst = Image.new("RGBA", (32, 32), hx("3F318F", 180))
    for (x, y) in [(8, 8), (24, 24)]:
        for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            put(lst, x + dx, y + dy, hx("8E7BE8", 170))
        put(lst, x, y, hx("C5B8FF", 190))
    lst.save(MC + "menu_list_background.png")

    bg = Image.new("RGBA", (32, 32), hx("5B4BC4", 90))
    put(bg, 16, 16, hx("FFFFFF", 110))
    bg.save(MC + "menu_background.png")

    for name, rows in [("header_separator", [hx("FFD6EE"), hx("FF9ED8")]),
                       ("footer_separator", [hx("FF9ED8"), hx("FFD6EE")])]:
        img = Image.new("RGBA", (32, 2))
        for y, c in enumerate(rows):
            for x in range(32):
                img.putpixel((x, y), c)
        img.save(MC + name + ".png")


# ------------------------------------------------------------------ ёжик для загрузки
LINE = hx("4A2E6B")
DARK = hx("3A2553")


def outline(img, col):
    src = img.copy()
    sp, dp = src.load(), img.load()
    for y in range(img.height):
        for x in range(img.width):
            if sp[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < img.width and 0 <= ny < img.height and sp[nx, ny][3]:
                        dp[x, y] = col
                        break


def ellipse(img, cx, cy, rx, ry, c):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                put(img, x, y, c)


def walker(frame):
    """Ёжик в профиль, идёт вправо. frame 0/1 — шаг."""
    img = Image.new("RGBA", (34, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    b = 1 if frame else 0
    # тело
    ellipse(img, 14, 15 - b, 11, 6, hx("C77BC9"))
    # иголки: острые треугольники, наклонённые назад, по дуге спины
    for i in range(9):
        a = math.pi * (0.98 - i * 0.1)          # от хвоста к голове
        bx = 14 + math.cos(a) * 10
        by = 15 - b - math.sin(a) * 5.5
        tipx = bx - 4 + i * 0.3
        tipy = by - 6 + abs(i - 4) * 0.4
        d.polygon([(bx - 2.5, by + 1), (bx + 2.5, by + 1), (tipx, tipy)],
                  fill=hx("B06BC0") if i % 2 else hx("D98BD2"))
        put(img, int(tipx), int(tipy) + 1, hx("F9CDEF"))
    ellipse(img, 13, 14 - b, 9, 4.5, hx("EFA6DD"))
    for i in range(6):
        put(img, 7 + i * 2, 12 - b + (i % 2), hx("B06BC0"))
    # мордочка
    d.polygon([(21, 11 - b), (31, 16 - b), (21, 19 - b)], fill=hx("FFE8D6"))
    ellipse(img, 22, 15 - b, 3.8, 3.8, hx("FFE8D6"))
    put(img, 31, 16 - b, DARK)
    put(img, 32, 16 - b, DARK)
    put(img, 25, 14 - b, DARK)
    put(img, 25, 13 - b, DARK)
    put(img, 24, 13 - b, hx("FFFFFF"))
    put(img, 24, 17 - b, hx("FF9CC2"))
    put(img, 23, 17 - b, hx("FF9CC2"))
    ellipse(img, 22, 10 - b, 1.8, 1.8, hx("FFE8D6"))
    # бантик
    d.polygon([(17, 6 - b), (14, 4 - b), (14, 8 - b)], fill=hx("8FE8FF"))
    d.polygon([(17, 6 - b), (20, 4 - b), (20, 8 - b)], fill=hx("8FE8FF"))
    # лапки
    feet = [(7, 22), (18, 21)] if frame == 0 else [(9, 21), (16, 22)]
    for fx, fy in feet:
        rect(img, fx, fy - 2, fx + 3, fy + 1, hx("E8B9A2"))
    outline(img, LINE)
    return img


def peek():
    """Сонная голова ёжика, выглядывающая из-за края экрана."""
    w, h = 30, 24
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2 + 2

    def star(ro, ri, dy):
        pts = []
        for i in range(22):
            a = -math.pi / 2 + i * math.pi / 11
            r = ro if i % 2 == 0 else ri
            pts.append((cx + math.cos(a) * r[0], cy + dy + math.sin(a) * r[1]))
        return pts

    d.polygon(star((14.4, 11.5), (10.8, 8.6), 0), fill=hx("B06BC0"))
    d.polygon(star((13.2, 10.5), (9.9, 7.9), -1), fill=hx("EFA6DD"))
    ellipse(img, cx, cy + 3, 9, 6.7, hx("FFE8D6"))
    ey = int(cy + 2)
    for ex in (int(cx - 4), int(cx + 3)):
        put(img, ex - 1, ey, DARK)
        put(img, ex, ey + 1, DARK)
        put(img, ex + 1, ey, DARK)
    put(img, int(cx), ey + 3, DARK)
    put(img, int(cx) - 1, ey + 3, DARK)
    rect(img, int(cx - 7), ey + 3, int(cx - 5), ey + 5, hx("FF9CC2"))
    rect(img, int(cx + 5), ey + 3, int(cx + 7), ey + 5, hx("FF9CC2"))
    outline(img, LINE)
    return img


if __name__ == "__main__":
    make_buttons()
    make_sliders()
    make_text_fields()
    make_tabs()
    make_scroller()
    make_backgrounds()
    walker(0).save(OWN + "hedgehog_walk_0.png")
    walker(1).save(OWN + "hedgehog_walk_1.png")
    peek().save(OWN + "hedgehog_peek.png")
    print("ok")
