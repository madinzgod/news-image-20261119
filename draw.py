#!/usr/bin/env python3
"""Render entry.png: 19 November 2026 world news as one newspaper front page.

Flat vector-style illustration drawn entirely with PIL primitives and real
fonts (Noto Sans). No photos, no generated lettering. Running this script
regenerates entry.png byte-for-byte.

Usage: python3 draw.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

W = H = 1024
MARGIN = 48
CONTENT_W = W - 2 * MARGIN
CX = W // 2

CREAM = (247, 242, 231)      # paper background
NAVY = (20, 33, 61)          # ink
RED = (179, 32, 44)          # accent
GOLD = (201, 162, 39)        # muted gold
GREYBLUE = (126, 151, 168)   # secondary shapes
PANEL = (233, 238, 241)      # soft grey-blue panel wash
DARK = (10, 16, 30)          # figure silhouettes

FONT_DIR = "/usr/share/fonts/truetype/noto"
BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
REGULAR = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


# ---------------------------------------------------------------- helpers

def text_w(d, text, fnt):
    return d.textlength(text, font=fnt)


def fit_font(d, text, max_w, start, minimum=10, bold=True):
    """Largest font (<= start) whose text fits max_w."""
    size = start
    while size > minimum:
        fnt = font(size, bold)
        if text_w(d, text, fnt) <= max_w:
            return fnt
        size -= 1
    return font(minimum, bold)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if text_w(d, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(d, cx, y, text, fnt, fill):
    d.text((cx - text_w(d, text, fnt) / 2, y), text, font=fnt, fill=fill)


def spaced_centered(d, cx, y, text, fnt, fill, spacing):
    """Draw text with extra letter spacing, centred on cx."""
    widths = [text_w(d, ch, fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        d.text((x, y), ch, font=fnt, fill=fill)
        x += wch + spacing


def wrapped_centered(d, cx, y, text, fnt, max_w, line_h, fill):
    for line in wrap(d, text, fnt, max_w):
        centered(d, cx, y, line, fnt, fill)
        y += line_h
    return y


def rule(d, y, h, fill, x0=MARGIN, x1=W - MARGIN):
    d.rectangle([x0, y, x1, y + h], fill=fill)


# ---------------------------------------------------------------- scene art

def skyline(d, base):
    """City skyline silhouette sitting on baseline `base`."""
    towers = [
        # (x, width, height, colour) -- heights sized for the scene panel
        (70, 54, 30, GREYBLUE), (132, 40, 46, NAVY), (180, 62, 26, NAVY),
        (250, 36, 56, NAVY), (294, 58, 34, GREYBLUE), (360, 44, 62, NAVY),
        (412, 66, 40, NAVY), (486, 40, 50, GREYBLUE), (534, 60, 32, NAVY),
        (602, 38, 58, NAVY), (648, 56, 38, NAVY), (712, 42, 48, GREYBLUE),
        (762, 60, 28, NAVY), (830, 38, 52, NAVY), (876, 58, 34, NAVY),
    ]
    for x, w, h, col in towers:
        d.rectangle([x, base - h, x + w, base], fill=col)
        # lit windows on the navy towers: deterministic arithmetic pattern
        if col == NAVY:
            for ri, r in enumerate(range(4, h - 5, 11)):
                for ci, c in enumerate(range(4, w - 5, 10)):
                    if (ri + ci) % 3 == 0:
                        d.rectangle([x + c, base - h + r,
                                     x + c + 4, base - h + r + 5], fill=GOLD)
    # one tower with a pointed spire (Ping An style)
    d.rectangle([672, base - 48, 706, base], fill=NAVY)
    d.polygon([(672, base - 48), (706, base - 48), (689, base - 66)],
              fill=NAVY)


def summit_scene(d):
    """Lead scene: skyline, three flag bars, three seated figures, a table."""
    top, bottom = 144, 326
    d.rectangle([MARGIN, top, W - MARGIN, bottom], fill=PANEL)
    skyline(d, base=214)

    centres = [300, 512, 724]
    bar_cols = [NAVY, RED, GOLD]
    for cx, col in zip(centres, bar_cols):
        d.rectangle([cx - 46, 222, cx + 46, 296], fill=col)

    # seated figures: head circle + shoulder dome, cream outline separates
    # the silhouette from the coloured bar behind it; the dome ends exactly
    # at the panel's bottom edge so nothing spills past the table
    for cx in centres:
        d.ellipse([cx - 58, 276, cx + 58, bottom], fill=DARK, outline=CREAM,
                  width=3)
        d.ellipse([cx - 25, 232, cx + 25, 282], fill=DARK, outline=CREAM,
                  width=3)

    # the long table, seen from the front (drawn last, over the domes)
    d.rectangle([MARGIN, 296, W - MARGIN, bottom], fill=NAVY)
    d.rectangle([MARGIN, 296, W - MARGIN, 299], fill=GOLD)
    for cx in centres:  # nameplates
        d.rectangle([cx - 22, 305, cx + 22, 316], fill=CREAM)


# ---------------------------------------------------------------- icons

def icon_tanker(d, cx, y0):
    """Tanker silhouette on waves, sun disc behind."""
    d.ellipse([cx + 40, y0 - 2, cx + 66, y0 + 24], fill=GOLD)
    # containers on deck
    for i, col in enumerate([RED, GOLD, GREYBLUE]):
        d.rectangle([cx - 62 + i * 26, y0 + 14, cx - 40 + i * 26, y0 + 28],
                    fill=col)
    # superstructure
    d.rectangle([cx + 44, y0 + 6, cx + 62, y0 + 28], fill=NAVY)
    d.rectangle([cx + 56, y0 - 4, cx + 60, y0 + 6], fill=NAVY)
    # hull
    d.polygon([(cx - 74, y0 + 28), (cx + 74, y0 + 28), (cx + 58, y0 + 46),
               (cx - 58, y0 + 46)], fill=NAVY)
    d.rectangle([cx - 74, y0 + 28, cx + 74, y0 + 32], fill=RED)
    # waves
    for row, yy in enumerate([y0 + 50, y0 + 57]):
        pts = [(x, yy + 3 * math.sin((x + row * 22) / 11.0))
               for x in range(cx - 74, cx + 75, 4)]
        d.line(pts, fill=GREYBLUE, width=3)


def icon_bridge(d, cx, y0):
    """Arched bridge with the middle span broken and hanging."""
    deck_y = y0 + 34
    for tx in (cx - 54, cx + 44):  # towers
        d.rectangle([tx, y0 + 4, tx + 10, y0 + 52], fill=NAVY)
    # arch under the deck
    d.arc([cx - 62, y0 + 18, cx + 62, y0 + 74], start=180, end=360,
          fill=NAVY, width=5)
    # cables from tower tops
    d.line([cx - 49, y0 + 4, cx - 80, deck_y], fill=NAVY, width=3)
    d.line([cx + 49, y0 + 4, cx + 80, deck_y], fill=NAVY, width=3)
    # intact deck segments and the gap between them
    d.line([cx - 80, deck_y, cx - 10, deck_y], fill=NAVY, width=6)
    d.line([cx + 14, deck_y, cx + 80, deck_y], fill=NAVY, width=6)
    # broken span, tilted down into the gap
    d.line([cx - 10, deck_y, cx + 8, deck_y + 17], fill=RED, width=6)
    d.line([cx - 80, y0 + 56, cx + 80, y0 + 56], fill=GREYBLUE, width=3)


def icon_court(d, x0, y0):
    """Courthouse front: pediment, four columns, steps."""
    d.polygon([(x0, y0 + 22), (x0 + 96, y0 + 22), (x0 + 48, y0)], fill=NAVY)
    d.ellipse([x0 + 41, y0 + 8, x0 + 55, y0 + 22], fill=GOLD)
    d.rectangle([x0, y0 + 24, x0 + 96, y0 + 30], fill=NAVY)
    for i in range(4):
        cx0 = x0 + 10 + i * 22
        d.rectangle([cx0, y0 + 34, cx0 + 9, y0 + 72], fill=NAVY)
    d.rectangle([x0 - 2, y0 + 74, x0 + 98, y0 + 79], fill=NAVY)
    d.rectangle([x0 - 6, y0 + 81, x0 + 102, y0 + 86], fill=NAVY)


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    rule(d, 14, 4, NAVY)
    rule(d, 23, 2, RED)
    spaced_centered(d, CX, 32, "THE WORLD IN ONE PICTURE", font(26), NAVY, 6)
    title_f = fit_font(d, "THURSDAY 19 NOVEMBER 2026", CONTENT_W, 60)
    centered(d, CX, 62, "THURSDAY 19 NOVEMBER 2026", title_f, NAVY)
    rule(d, 132, 4, NAVY)

    # --- lead story ----------------------------------------------------
    summit_scene(d)
    head_f = font(54)
    centered(d, CX, 338, "TRUMP · XI · PUTIN", head_f, NAVY)
    centered(d, CX, 400, "FIRST THREE-WAY SUMMIT", head_f, NAVY)
    wrapped_centered(
        d, CX, 470,
        "The US, Chinese and Russian presidents meet in Shenzhen, "
        "on the sidelines of the APEC summit",
        font(27, bold=False), CONTENT_W, 34, NAVY)

    # --- two half-width stories ----------------------------------------
    d.line([CX, 566, CX, 782], fill=NAVY, width=2)
    half_f = font(36)
    sub_f = font(23, bold=False)

    icon_tanker(d, 266, 560)
    y = wrapped_centered(d, 266, 622, "IRAN STRIKES GULF STATES",
                         half_f, 436, 43, NAVY)
    wrapped_centered(
        d, 266, y + 8,
        "Retaliation after US strikes on Qeshm Island; a tanker is hit "
        "in the Strait of Hormuz",
        sub_f, 436, 28, NAVY)

    icon_bridge(d, 758, 560)
    y = wrapped_centered(d, 758, 622, "CRIMEAN BRIDGE HIT AGAIN",
                         half_f, 436, 43, NAVY)
    wrapped_centered(
        d, 758, y + 8,
        "Ukraine's third strike on the crossing this week closes it "
        "to traffic",
        sub_f, 436, 28, NAVY)

    # --- wide story ------------------------------------------------------
    icon_court(d, 56, 812)
    wide_f = fit_font(d, "WORLD COURT DELIVERS ROHINGYA JUDGMENT", 800, 40)
    d.text((176, 812), "WORLD COURT DELIVERS ROHINGYA JUDGMENT",
           font=wide_f, fill=NAVY)
    y = 862
    for line in wrap(d, "The ICJ in The Hague rules on Myanmar's 2017 "
                        "campaign against the Rohingya, in the case "
                        "brought by The Gambia", font(23, bold=False), 800):
        d.text((176, y), line, font=font(23, bold=False), fill=NAVY)
        y += 28

    # --- bottom strip ----------------------------------------------------
    rule(d, 922, 2, RED)
    strip_f = fit_font(
        d, "ANTHROPIC'S RECORD MARKET DEBUT  •  VAN GOGH SELLS FOR A "
           "RECORD $190M", CONTENT_W, 24)
    segments = [("ANTHROPIC'S RECORD MARKET DEBUT", NAVY),
                ("  •  ", RED),
                ("VAN GOGH SELLS FOR A RECORD $190M", NAVY)]
    total = sum(text_w(d, t, strip_f) for t, _ in segments)
    x = CX - total / 2
    for t, col in segments:
        d.text((x, 936), t, font=strip_f, fill=col)
        x += text_w(d, t, strip_f)
    centered(d, CX, 968, "VOYAGER 1 NEARS ONE LIGHT-DAY FROM EARTH",
             strip_f, NAVY)
    rule(d, 1008, 3, NAVY)

    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    build().save(out, format="PNG")
    print("wrote", out)
