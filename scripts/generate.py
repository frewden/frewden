
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
import random

# =============================================
# ANIMATED PCB GITHUB PROFILE
# Dark Navy + Orange + Cyan
# Monospace Programming Font
# =============================================

OUT = Path("assets")
OUT.mkdir(parents=True, exist_ok=True)

WIDTH = 960
FRAME_COUNT = 28
FRAME_MS = 90

BG = (5, 17, 30)
COPPER = (222, 107, 39)
ORANGE = (255, 155, 60)
CYAN = (65, 220, 250)
WHITE = (232, 242, 248)
MUTED = (139, 166, 185)

FONT_NORMAL = (
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSansMono.ttf"
)
FONT_BOLD = (
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSansMono-Bold.ttf"
)


def get_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_NORMAL
    return ImageFont.truetype(path, size)


def create_paths(height, hero=False):
    if hero:
        return [
            [(0, 35), (160, 35), (195, 70), (350, 70)],
            [(0, 100), (120, 100), (160, 140), (290, 140)],
            [(0, 260), (150, 260), (190, 220), (350, 220)],
            [(0, 315), (250, 315), (300, 265), (450, 265)],
            [(510, 25), (690, 25), (730, 65), (960, 65)],
            [(650, 120), (770, 120), (820, 170), (960, 170)],
            [(550, 310), (690, 310), (750, 250), (960, 250)],
            [(825, 0), (825, 42), (960, 42)],
        ]

    return [
        [(0, 15), (100, 15), (135, 50), (235, 50)],
        [(0, 85), (95, 85), (130, 50), (200, 50)],
        [(300, 0), (340, 38), (375, 38)],
        [(585, 0), (620, 35), (675, 35)],
        [(750, 15), (825, 15), (860, 50), (960, 50)],
        [(735, 100), (815, 100), (850, 65), (960, 65)],
        [(0, height-20), (150, height-20)],
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
        (x, y, x+size, y+size),
        radius=6,
        fill=(12, 37, 54),
        outline=ORANGE,
        width=2
    )

    draw.rectangle(
        (x+13, y+13, x+size-13, y+size-13),
        fill=(9, 23, 37),
        outline=(70, 135, 154)
    )

    for i in range(4):
        p = 10 + i * (size-20)/3

        draw.line(
            (x-9, y+p, x, y+p),
            fill=COPPER,
            width=3
        )

        draw.line(
            (x+size, y+p, x+size+9, y+p),
            fill=COPPER,
            width=3
        )

        draw.line(
            (x+p, y-9, x+p, y),
            fill=COPPER,
            width=3
        )

        draw.line(
            (x+p, y+size, x+p, y+size+9),
            fill=COPPER,
            width=3
        )


def background(draw, height, paths):
    draw.rectangle(
        (0, 0, WIDTH, height),
        fill=BG
    )

    # PCB dot grid
    for x in range(0, WIDTH, 28):
        for y in range(0, height, 28):
            draw.ellipse(
                (x, y, x+1, y+1),
                fill=(29, 56, 70)
            )

    # Copper traces
    for i, path in enumerate(paths):
        color = COPPER if i % 2 == 0 else (40, 118, 146)

        draw.line(
            path,
            fill=(24, 55, 70),
            width=9,
            joint="curve"
        )

        draw.line(
            path,
            fill=color,
            width=3,
            joint="curve"
        )

        for x, y in (path[0], path[-1]):
            draw.ellipse(
                (x-4, y-4, x+4, y+4),
                fill=BG,
                outline=color,
                width=2
            )


def electrons(draw, paths, frame):
    for index, path in enumerate(paths):
        phase = (
            frame / FRAME_COUNT
            + index * 0.17
        ) % 1

        x, y = path_position(path, phase)

        # Layered glowing electron
        for radius, color in [
            (13, (16, 55, 70)),
            (9, (23, 93, 116)),
            (6, (39, 155, 183)),
            (3, CYAN),
        ]:
            draw.ellipse(
                (
                    x-radius, y-radius,
                    x+radius, y+radius
                ),
                fill=color
            )

        # Secondary orange charge
        x2, y2 = path_position(
            path,
            (phase + 0.5) % 1
        )

        draw.ellipse(
            (x2-3, y2-3, x2+3, y2+3),
            fill=ORANGE
        )


def hero(frame):
    height = 340
    paths = create_paths(height, hero=True)

    img = Image.new(
        "RGB",
        (WIDTH, height),
        BG
    )
    draw = ImageDraw.Draw(img)

    background(draw, height, paths)
    electrons(draw, paths, frame)

    draw_chip(draw, 820, 102, 65)
    draw_chip(draw, 695, 195, 44)

    # Dark central display
    draw.rounded_rectangle(
        (60, 112, 665, 244),
        radius=10,
        fill=(7, 24, 40),
        outline=(28, 65, 85),
        width=2
    )

    draw.text(
        (80, 128),
        "> INITIALIZING PROFILE...",
        fill=CYAN,
        font=get_font(13, True)
    )

    draw.text(
        (80, 164),
        "VYSHNAV HARILAL",
        fill=WHITE,
        font=get_font(34, True)
    )

    draw.text(
        (82, 217),
        "ELECTRONICS // EMBEDDED SYSTEMS",
        fill=ORANGE,
        font=get_font(16, True)
    )

    draw.text(
        (75, 288),
        "[ OK ] HARDWARE SYSTEMS READY",
        fill=CYAN,
        font=get_font(12)
    )

    draw.text(
        (700, 307),
        "STATUS: ONLINE",
        fill=ORANGE,
        font=get_font(12, True)
    )

    return img


def section(frame, number, title, subtitle):
    height = 125
    paths = create_paths(height)

    img = Image.new(
        "RGB",
        (WIDTH, height),
        BG
    )
    draw = ImageDraw.Draw(img)

    background(draw, height, paths)
    electrons(draw, paths, frame)

    draw.rounded_rectangle(
        (240, 19, 725, 106),
        radius=9,
        fill=(7, 25, 41),
        outline=(45, 91, 116),
        width=2
    )

    draw.text(
        (263, 40),
        number + " // " + title,
        fill=ORANGE,
        font=get_font(22, True)
    )

    draw.text(
        (264, 78),
        subtitle,
        fill=CYAN,
        font=get_font(12)
    )

    return img


def save_gif(filename, generator):
    print("Generating:", filename)

    frames = []

    for i in range(FRAME_COUNT):
        frames.append(generator(i))

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
        (
            "about.gif",
            "01",
            "ABOUT ME",
            "USER PROFILE // INITIALIZED"
        ),
        (
            "skills.gif",
            "02",
            "TECHNICAL SKILLS",
            "HARDWARE // SOFTWARE // TOOLS"
        ),
        (
            "projects.gif",
            "03",
            "FEATURED PROJECTS",
            "DESIGN // DEVELOP // DEPLOY"
        ),
        (
            "contact.gif",
            "05",
            "CONTACT",
            "ESTABLISHING CONNECTION..."
        )
    ]

    for filename, number, title, subtitle in sections:
        save_gif(
            filename,
            lambda frame, n=number, t=title, s=subtitle:
                section(frame, n, t, s)
        )

    print("PCB animations generated!")


if __name__ == "__main__":
    main()
