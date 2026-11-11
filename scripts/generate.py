from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path("assets")
OUT.mkdir(parents=True, exist_ok=True)

WIDTH = 960
FRAME_COUNT = 28
FRAME_MS = 90

BG = (0, 0, 0)
GRID = (0, 28, 0)
TRACE_DARK = (0, 45, 0)
TRACE = (0, 115, 0)
TRACE_BRIGHT = (0, 180, 40)
TEXT = (0, 210, 60)
TEXT_BRIGHT = (80, 255, 120)
TEXT_DIM = (0, 130, 40)
PANEL = (0, 10, 0)

FONT_NORMAL = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def get_font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_NORMAL, size)

def create_paths(height, hero=False):
    if hero:
        return [
            [(0, 35), (180, 35), (220, 75), (370, 75)],
            [(0, 95), (120, 95), (170, 145), (310, 145)],
            [(0, 260), (180, 260), (220, 215), (390, 215)],
            [(0, 315), (250, 315), (300, 265), (470, 265)],
            [(520, 25), (700, 25), (745, 70), (960, 70)],
            [(640, 120), (760, 120), (815, 175), (960, 175)],
            [(560, 305), (700, 305), (760, 245), (960, 245)],
            [(825, 0), (825, 45), (960, 45)],
        ]
    return [
        [(0, 18), (100, 18), (140, 58), (240, 58)],
        [(0, 90), (95, 90), (135, 55), (225, 55)],
        [(300, 0), (340, 38), (390, 38)],
        [(570, 0), (610, 40), (680, 40)],
        [(760, 18), (835, 18), (875, 58), (960, 58)],
        [(735, 105), (815, 105), (860, 65), (960, 65)],
        [(0, height - 22), (150, height - 22)],
    ]

def path_position(path, progress):
    lengths = []
    total = 0
    for p1, p2 in zip(path[:-1], path[1:]):
        dist = math.dist(p1, p2)
        lengths.append(dist)
        total += dist

    remaining = (progress % 1) * total
    for i, length in enumerate(lengths):
        if remaining <= length:
            p1 = path[i]
            p2 = path[i + 1]
            t = remaining / length if length else 0
            return (
                p1[0] + (p2[0] - p1[0]) * t,
                p1[1] + (p2[1] - p1[1]) * t
            )
        remaining -= length
    return path[-1]

def draw_chip(draw, x, y, size=60):
    draw.rounded_rectangle(
        (x, y, x + size, y + size),
        radius=6,
        fill=(0, 18, 0),
        outline=TRACE_BRIGHT,
        width=2
    )
    draw.rectangle(
        (x + 13, y + 13, x + size - 13, y + size - 13),
        fill=(0, 8, 0),
        outline=TRACE
    )

    for i in range(4):
        p = 10 + i * (size - 20) / 3
        draw.line((x - 9, y + p, x, y + p), fill=TRACE_BRIGHT, width=3)
        draw.line((x + size, y + p, x + size + 9, y + p), fill=TRACE_BRIGHT, width=3)
        draw.line((x + p, y - 9, x + p, y), fill=TRACE_BRIGHT, width=3)
        draw.line((x + p, y + size, x + p, y + size + 9), fill=TRACE_BRIGHT, width=3)

def background(draw, height, paths):
    draw.rectangle((0, 0, WIDTH, height), fill=BG)

    for x in range(0, WIDTH, 28):
        for y in range(0, height, 28):
            draw.ellipse((x, y, x + 1, y + 1), fill=GRID)

    for i, path in enumerate(paths):
        color = TRACE if i % 2 == 0 else TRACE_BRIGHT
        draw.line(path, fill=TRACE_DARK, width=9, joint="curve")
        draw.line(path, fill=color, width=3, joint="curve")

        for x, y in (path[0], path[-1]):
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=BG, outline=color, width=2)

def electrons(draw, paths, frame):
    for index, path in enumerate(paths):
        phase = (frame / FRAME_COUNT + index * 0.17) % 1
        x, y = path_position(path, phase)

        for radius, color in [
            (13, (0, 30, 0)),
            (9, (0, 70, 0)),
            (6, (0, 130, 30)),
            (3, TEXT_BRIGHT),
        ]:
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)

        x2, y2 = path_position(path, (phase + 0.5) % 1)
        draw.ellipse((x2 - 3, y2 - 3, x2 + 3, y2 + 3), fill=TRACE_BRIGHT)

def hero(frame):
    height = 340
    paths = create_paths(height, hero=True)
    img = Image.new("RGB", (WIDTH, height), BG)
    draw = ImageDraw.Draw(img)

    background(draw, height, paths)
    electrons(draw, paths, frame)
    draw_chip(draw, 820, 102, 65)
    draw_chip(draw, 695, 195, 44)

    draw.rounded_rectangle(
        (55, 108, 690, 245),
        radius=10,
        fill=PANEL,
        outline=TRACE,
        width=2
    )

    draw.text((75, 126), "> INITIALIZING PROFILE...", fill=TEXT_BRIGHT, font=get_font(13, True))
    draw.text((75, 162), "VYSHNAV HARILAL", fill=TEXT_BRIGHT, font=get_font(34, True))
    draw.text((77, 216), "ELECTRONICS // EMBEDDED SYSTEMS", fill=TEXT, font=get_font(16, True))
    draw.text((72, 287), "[ OK ] SYSTEM READY", fill=TEXT_BRIGHT, font=get_font(12))
    draw.text((730, 307), "STATUS: ONLINE", fill=TEXT, font=get_font(12, True))

    return img

def section(frame, number, title, subtitle):
    height = 125
    paths = create_paths(height)
    img = Image.new("RGB", (WIDTH, height), BG)
    draw = ImageDraw.Draw(img)

    background(draw, height, paths)
    electrons(draw, paths, frame)

    draw.rounded_rectangle(
        (225, 19, 740, 106),
        radius=9,
        fill=PANEL,
        outline=TRACE,
        width=2
    )

    draw.text((248, 40), number + " // " + title, fill=TEXT_BRIGHT, font=get_font(22, True))
    draw.text((250, 78), subtitle, fill=TEXT_DIM, font=get_font(12))
    return img

def save_gif(filename, generator):
    frames = [generator(i) for i in range(FRAME_COUNT)]
    frames[0].save(
        OUT / filename,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
        disposal=2
    )

def main():
    save_gif("hero.gif", hero)

    sections = [
        ("about.gif", "01", "ABOUT ME", "USER PROFILE // INITIALIZED"),
        ("skills.gif", "02", "TECHNICAL SKILLS", "HARDWARE // SOFTWARE // TOOLS"),
        ("projects.gif", "03", "FEATURED PROJECTS", "DESIGN // DEVELOP // DEPLOY"),
        ("contact.gif", "05", "CONTACT", "ESTABLISHING CONNECTION..."),
    ]

    for filename, number, title, subtitle in sections:
        save_gif(
            filename,
            lambda frame, n=number, t=title, s=subtitle: section(frame, n, t, s)
        )

if __name__ == "__main__":
    main()
