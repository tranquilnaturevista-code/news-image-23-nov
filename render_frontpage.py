#!/usr/bin/env python3
"""Draw the 23 November 2026 front page and save it as entry.png.

A one-day newspaper front page, drawn entirely with Pillow primitives:
no network, no randomness, no timestamps. Running this script twice
produces byte-identical output.

Stories were checked against reports published on Monday 23 November
2026 (Reuters, BBC, AP, Al Jazeera, The Hindu and the day's news
digests). Nothing is invented: casualty figures that differed between
outlets are left out rather than guessed.
"""

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (251, 246, 236)
INK = (25, 23, 19)
NAVY = (20, 54, 93)
NAVY_DARK = (13, 38, 66)
RED = (179, 38, 30)
GOLD = (201, 154, 43)
GREY = (92, 86, 76)
CARD_BG = (255, 255, 255)
LEAD_BG = (232, 240, 247)
RULE = (25, 23, 19)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)             # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)               # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_globe(draw, cx, cy, r, fill, line):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=line, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=line, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=line, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             0, 360, fill=line, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy - r * 0.25],
             180, 360, fill=line, width=3)


def icon_burst(draw, cx, cy, r, fill):
    starburst(draw, cx, cy, r, r * 0.45, 8, fill)
    draw.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22],
                 fill=(255, 255, 255))


def icon_tanker(draw, cx, cy, r, fill):
    # hull
    draw.polygon([(cx - r, cy - r * 0.1), (cx + r, cy - r * 0.1),
                  (cx + r * 0.7, cy + r * 0.55), (cx - r * 0.7, cy + r * 0.55)],
                 fill=fill)
    # containers
    draw.rectangle([cx - r * 0.7, cy - r * 0.75, cx - r * 0.1, cy - r * 0.15],
                   fill=fill)
    draw.rectangle([cx + r * 0.05, cy - r * 0.6, cx + r * 0.65, cy - r * 0.15],
                   fill=fill)
    # waves
    for k, yy in enumerate((cy + r * 0.75, cy + r * 0.9)):
        draw.arc([cx - r - 6 + k * 4, yy - 6, cx - r * 0.2 + k * 4, yy + 6],
                 180, 360, fill=fill, width=3)
        draw.arc([cx + r * 0.2 - k * 4, yy - 6, cx + r + 6 - k * 4, yy + 6],
                 180, 360, fill=fill, width=3)


def icon_drone(draw, cx, cy, r, fill):
    draw.ellipse([cx - r * 0.3, cy - r * 0.25, cx + r * 0.3, cy + r * 0.25],
                 fill=fill)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        px, py = cx + sx * r * 0.62, cy + sy * r * 0.55
        draw.line([px - r * 0.3, py, px + r * 0.3, py], fill=fill, width=4)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=fill)
    draw.line([cx - r * 0.3, cy, cx + r * 0.3, cy], fill=fill, width=3)


def icon_star(draw, cx, cy, r, fill):
    starburst(draw, cx, cy, r, r * 0.42, 5, fill)
    draw.ellipse([cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18],
                 fill=(255, 255, 255))


def icon_chart(draw, cx, cy, r, fill):
    draw.line([cx - r * 0.8, cy + r * 0.7, cx + r * 0.8, cy + r * 0.7],
              fill=fill, width=4)
    draw.line([cx - r * 0.8, cy + r * 0.7, cx - r * 0.8, cy - r * 0.7],
              fill=fill, width=4)
    pts = [(cx - r * 0.65, cy + r * 0.35), (cx - r * 0.2, cy - r * 0.1),
           (cx + r * 0.15, cy + r * 0.1), (cx + r * 0.7, cy - r * 0.55)]
    draw.line(pts, fill=fill, width=5, joint="curve")
    draw.polygon([(cx + r * 0.7, cy - r * 0.55), (cx + r * 0.45, cy - r * 0.5),
                  (cx + r * 0.55, cy - r * 0.28)], fill=fill)


def icon_ballot(draw, cx, cy, r, fill):
    # slip of paper above the box, check mark on the box
    draw.rectangle([cx - r * 0.32, cy - r * 0.9, cx + r * 0.32, cy - r * 0.05],
                   fill=fill)
    draw.rectangle([cx - r * 0.75, cy - r * 0.05, cx + r * 0.75, cy + r * 0.75],
                   fill=fill)
    draw.line([cx - r * 0.45, cy + r * 0.32, cx - r * 0.12, cy + r * 0.58,
               cx + r * 0.5, cy - r * 0.28 + r * 0.3], fill=(255, 255, 255),
              width=5, joint="curve")


def icon_rocket(draw, cx, cy, r, fill):
    # body
    draw.polygon([(cx, cy - r), (cx + r * 0.45, cy - r * 0.1),
                  (cx + r * 0.45, cy + r * 0.45),
                  (cx - r * 0.45, cy + r * 0.45),
                  (cx - r * 0.45, cy - r * 0.1)], fill=fill)
    # window
    draw.ellipse([cx - r * 0.18, cy - r * 0.45, cx + r * 0.18, cy - r * 0.05],
                 fill=(255, 255, 255))
    # fins
    draw.polygon([(cx - r * 0.45, cy + r * 0.25), (cx - r * 0.85, cy + r * 0.7),
                  (cx - r * 0.45, cy + r * 0.55)], fill=fill)
    draw.polygon([(cx + r * 0.45, cy + r * 0.25), (cx + r * 0.85, cy + r * 0.7),
                  (cx + r * 0.45, cy + r * 0.55)], fill=fill)
    # flame
    draw.polygon([(cx - r * 0.25, cy + r * 0.55), (cx + r * 0.25, cy + r * 0.55),
                  (cx, cy + r)], fill=fill)


def icon_shield(draw, cx, cy, r, fill):
    draw.polygon([(cx - r * 0.8, cy - r * 0.7), (cx + r * 0.8, cy - r * 0.7),
                  (cx + r * 0.8, cy + r * 0.1), (cx, cy + r * 0.9),
                  (cx - r * 0.8, cy + r * 0.1)], fill=fill)
    draw.line([cx - r * 0.4, cy + r * 0.05, cx - r * 0.1, cy + r * 0.35,
               cx + r * 0.45, cy - r * 0.35], fill=(255, 255, 255),
              width=5, joint="curve")


ICONS = {
    "globe": icon_globe,
    "burst": icon_burst,
    "tanker": icon_tanker,
    "drone": icon_drone,
    "star": icon_star,
    "chart": icon_chart,
    "ballot": icon_ballot,
    "rocket": icon_rocket,
    "shield": icon_shield,
}


def chip(draw, cx, cy, r, color, kind):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    fn = ICONS[kind]
    if kind == "globe":
        fn(draw, cx, cy, r * 0.72, (255, 255, 255), NAVY)
    else:
        fn(draw, cx, cy, r * 0.62, (255, 255, 255))


# ---------------------------------------------------------------- stories
LEAD = {
    "tag": "CLIMATE  •  ANTALYA, TURKEY",
    "headline": "COP31 talks collapse",
    "deck": ("The final draft drops any mention of fossil fuels, and the EU "
             "and others reject a deal without a phase-out. The summit ends "
             "with no agreement."),
}

CARDS = [
    {
        "tag": "THE GULF",
        "color": (180, 83, 9),
        "icon": "tanker",
        "headline": "Tankers burn in the Strait of Hormuz",
        "deck": ("Three tankers struck since Friday; Iran says two more "
                 "caught fire on mines."),
    },
    {
        "tag": "LIBYA",
        "color": (53, 80, 122),
        "icon": "drone",
        "headline": "Sea drones hit Russian warship in Libya",
        "deck": ("The corvette Merkury is badly damaged at Benghazi "
                 "and later capsizes; 10 injured."),
    },
    {
        "tag": "UKRAINE",
        "color": (15, 118, 110),
        "icon": "burst",
        "headline": "Drone strike flattens Kyiv flat block",
        "deck": ("A Russian drone hits a five-storey block in Dymer; "
                 "2 killed, 11 missing."),
    },
    {
        "tag": "USA–CANADA",
        "color": (169, 50, 38),
        "icon": "shield",
        "headline": "US curbs defence ties with Canada",
        "deck": ("Hegseth imposes new restrictions in a classified memo, "
                 "the Post reports."),
    },
    {
        "tag": "SPACE",
        "color": (47, 107, 51),
        "icon": "rocket",
        "headline": "BepiColombo reaches Mercury",
        "deck": ("After an eight-year journey, the craft enters orbit — "
                 "only the second ever."),
    },
    {
        "tag": "SOUTH KOREA",
        "color": (107, 78, 155),
        "icon": "ballot",
        "headline": "Minister quits over AI exam cheating",
        "deck": ("South Korea's education minister resigns amid an AI "
                 "exam cheating scandal."),
    },
]

TICKER = ("ALSO TODAY:  Lahore the world's most polluted city (AQI 538)  •  "
          "Shuri Castle restored  •  Nepal PM meets Modi  •  Liverpool beat "
          "Man United  •  India 720/9d")

FOOTER = ("All stories as reported on Monday 23 November 2026  •  "
          "Sources: Reuters, BBC, AP, Al Jazeera, The Hindu")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 10], fill=RED)
    d.rectangle([0, 10, W, 112], fill=NAVY)
    d.text((W // 2, 58), "THE WORLD IN ONE DAY",
           font=SERIF_B(62), fill=(255, 255, 255), anchor="mm")
    d.rectangle([0, 112, W, 116], fill=GOLD)

    # ---- date line ------------------------------------------------------
    d.text((W // 2, 150), "MONDAY 23 NOVEMBER 2026",
           font=SERIF_B(48), fill=NAVY_DARK, anchor="mm")
    d.text((W // 2, 192), "One day's world news — eight stories from every corner of the globe",
           font=SERIF(21), fill=GREY, anchor="mm")
    d.line([36, 212, W - 36, 212], fill=RULE, width=3)
    d.line([36, 218, W - 36, 218], fill=RULE, width=1)

    # ---- lead story ------------------------------------------------------
    lx, ly, lw, lh = 36, 230, W - 72, 138
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=LEAD_BG)
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=NAVY, width=2)
    d.rectangle([lx, ly, lx + 10, ly + lh], fill=RED)
    tx = lx + 28
    d.text((tx, ly + 14), LEAD["tag"], font=SANS_B(18), fill=RED)
    head_lines = wrap(d, LEAD["headline"], SANS_B(38), lw - 220)
    y = draw_lines(d, head_lines, tx, ly + 38, SANS_B(38), NAVY_DARK, 44)
    deck_lines = wrap(d, LEAD["deck"], SANS(20), lw - 220)
    draw_lines(d, deck_lines, tx, y + 2, SANS(20), INK, 25)
    chip(d, lx + lw - 82, ly + lh // 2, 56, NAVY, "globe")

    # ---- story grid ------------------------------------------------------
    gx, gy = 36, 382
    cw, ch, gap = (W - 72 - 12) // 2, 170, 12
    for i, card in enumerate(CARDS):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD_BG)
        d.rectangle([cx, cy, cx + cw, cy + ch], outline=(205, 198, 182), width=1)
        d.rectangle([cx, cy, cx + cw, cy + 6], fill=card["color"])
        pad = 16
        chip(d, cx + cw - 42, cy + 42, 28, card["color"], card["icon"])
        d.text((cx + pad, cy + 20), card["tag"], font=SANS_B(17),
               fill=card["color"])
        hl = wrap(d, card["headline"], SANS_B(27), cw - pad * 2 - 70)
        y = draw_lines(d, hl, cx + pad, cy + 48, SANS_B(27), INK, 31)
        dl = wrap(d, card["deck"], SANS(19), cw - pad * 2)
        draw_lines(d, dl, cx + pad, y + 4, SANS(19), (64, 60, 52), 23)

    # ---- ticker ----------------------------------------------------------
    ty = 382 + 3 * ch + 2 * gap + 8
    d.rectangle([36, ty, W - 36, ty + 56], fill=NAVY)
    ticker_lines = wrap(d, TICKER, SANS_B(19), W - 72 - 28)
    yy = ty + 28 - (len(ticker_lines) * 24) // 2
    for line in ticker_lines:
        d.text((W // 2, yy + 12), line, font=SANS_B(19),
               fill=(255, 255, 255), anchor="mm")
        yy += 24

    # ---- footer ----------------------------------------------------------
    fy = ty + 56 + 12
    d.line([36, fy, W - 36, fy], fill=(205, 198, 182), width=1)
    d.text((W // 2, fy + 6), FOOTER, font=SANS(14), fill=GREY, anchor="ma")

    return img


def main():
    # Build tool only: renders the page next to this script so the repo
    # holds the finished image. The entry program (main.py) is the one
    # that publishes it to /output/entry.png.
    here = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("RENDER_OUTPUT_DIR", str(here)))
    out_dir.mkdir(parents=True, exist_ok=True)
    img = build()
    target = out_dir / "entry.png"
    img.save(target, format="PNG")
    print(f"wrote {target} {img.size[0]}x{img.size[1]} "
          f"{target.stat().st_size} bytes")


if __name__ == "__main__":
    main()
