import os
from PIL import Image, ImageDraw, ImageFont

# КАЖДЫЙ РАЗ НОВУЮ ПАПКУ УКАЗЫВАТЬ ПОД НОВЫЙ ШАБЛОН
# ТК ФАЙЛЫ ПЕРЕЗАПИСЫВАЮТСЯ И НИКУДА НЕ СОХРАНЯЮТСЯ

CONFIG = {
    "image_path": "rewards_shablon/tutor.png", #путь до шаблона относительно main.py
    "output_dir": "rewards_tutor_test", #папка куда сохранятся грамоты с фамилиями

    "font_path": "fonts/FoglihtenNo06_076.otf", #путь до шрифта
    "color": (41, 84, 74), #цвет в RGB
    "base_font_scale": 0.1, #базовый размер шрифта от ширины шаблона
    "min_font_size": 20, #минимальный размер шрифта
    "max_font_size": 140, #максимальный размер шрифта

    "max_text_width_ratio": 0.75, #максимально допустимый размер шрифта чтобы забить на длину имени
    "text_x_offset": 15, #сдвиг текста по x в px
    "center_y_ratio": .575, #.575 .61 #сдвиг текста по y в относительных единицах

    "line_spacing_scale": 1.3, #если имя в 2 строки то это отступ

    "debug": True #нужны ли логи
}

# Сюда список фамилий пишешь
fio_list = [
    "Федорову Глебасу",
    "Щеголихину Артему",
    "Фомину Владосу",
]

os.makedirs(CONFIG["output_dir"], exist_ok=True)

sample = Image.open(CONFIG["image_path"])
W, H = sample.size

MAX_TEXT_WIDTH = int(W * CONFIG["max_text_width_ratio"])
CENTER_Y = int(H * CONFIG["center_y_ratio"])

BASE_FONT_SIZE = int(W * CONFIG["base_font_scale"])


def load_font(size):
    return ImageFont.truetype(CONFIG["font_path"], size)

def text_width(drw, text, fnt):
    bbox = drw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0]

def split_fio(drw, _fio, fnt):
    parts = _fio.split()

    if text_width(drw, _fio, fnt) <= MAX_TEXT_WIDTH:
        return [_fio]

    if len(parts) >= 2:
        return [parts[0], " ".join(parts[1:])]

    return [_fio]

def fit_font(drw, _fio):
    size = BASE_FONT_SIZE

    while size > CONFIG["min_font_size"]:
        size = min(size, CONFIG["max_font_size"])

        fnt = load_font(size)
        lns = split_fio(drw, _fio, fnt)

        max_line = max(text_width(drw, l, fnt) for l in lns)

        if max_line <= MAX_TEXT_WIDTH:
            if CONFIG["debug"]:
                print(f"[OK] {_fio} -> font {size}")
            return fnt, lns

        size -= 2

    return load_font(CONFIG["min_font_size"]), [_fio]

def draw_centered(drw, text, coord_y, fnt):
    w = text_width(drw, text, fnt)
    x = (W - w) // 2 + CONFIG["text_x_offset"]
    drw.text((x, coord_y), text, font=fnt, fill=CONFIG["color"])

for i, fio in enumerate(fio_list, start=1):
    image = Image.open(CONFIG["image_path"]).convert("RGB")
    draw = ImageDraw.Draw(image)

    font, lines = fit_font(draw, fio)

    line_spacing = int(font.size * CONFIG["line_spacing_scale"])

    total_height = len(lines) * line_spacing
    y_start = CENTER_Y - total_height // 2

    for j, line in enumerate(lines):
        y = y_start + j * line_spacing
        draw_centered(draw, line, y, font)

    output_path = os.path.join(CONFIG["output_dir"], f"reward{i}.png")
    image.save(output_path, quality=95)

print("Грамоты созданы")