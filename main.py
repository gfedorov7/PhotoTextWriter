import os
from PIL import Image, ImageDraw, ImageFont


CONFIG = {
    "image_path": "rewards_shablon/pervak.png",
    "output_dir": "rewards_pervak",

    "font_path": "fonts/FoglihtenNo06_076.otf",
    "color": (41, 84, 74),
    "base_font_scale": 0.1,
    "min_font_size": 20,
    "max_font_size": 150,

    "max_text_width_ratio": 0.75,
    "text_x_offset": 35,
    "center_y_ratio": .59,

    "line_spacing_scale": 1.3,

    "debug": True
}

# #ПЕРВАКИ
fio_list = [
    "Дружинину Даниилу",
    "Дьячкову Ивану",
    "Гаранину Илье",
    "Тропиной Анастасии",
    "Сташевской Камиле",
    "Загорской Эле",
    "Лукуткину Никите",
    "Ястребову Артёму",
    "Рогожиной Дарье",
    "Кисловой Полине",
    "Толкачеву Антону",
    "Строганову Глебу",
    "Бубнышевой Анастасии",
    "Серовой Елене",
    "Комаровой Марии",
    "Долгову Анатолию",
    "Савиновой Арине",
    "Фадиной Елизавете",
]

# #КУЛЬТМАСС
# fio_list = [
    # "Коршуновой Виктории",
    # "Кирсанову Степану",
    # "Рожнову Сергею",
    # "Толоконниковой Ксении",
    # "Докиной Анастасии",
    # "Ежикову Егору",
    # "Кульковлй Екатерине",
    # "Сташевской Камиле",
    # "Кашириной Ксении",
    # "Склокиной Валерии"
# ]

# #ВЫПУСКНИКИ
# fio_list = [
#     "Панферову Александру",
    # "Монахову Дмитрию",
    # "Гордеевой Дарье",
    # "Паранюшкиной Дарье",
    # "Кобозевой Алине",
    # "Аникиной Алине",
    # "Петровой Светлане",
    # "Рожнову Сергею",
    # "Федотову Дмитрию",
    # "Першиной Екатерине",
    # "Крошечкиной Марине",
    # "Тахировой Малике",
    # "Трусову Алексею",
    # "Бростиловой Дарье",
    # "Гиясовой Виктории",
    # "Кугушевой Валерии",
    # "Ермакову Ивану",
    # "Рожнову Олегу"
# ]

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