#!/usr/bin/env python3
"""Render the 19 November 2026 world-news front page as a 1024x1024 PNG.

Pure PIL drawing: flat colours, simple geometric illustrations, wrapped
headlines. Fully deterministic -- no randomness, no timestamps, no network.
Run: python3 gen.py  ->  writes entry.png next to this file.

Stories (all reported on Thursday 19 November 2026):
  hero  Trump, Xi and Putin hold first three-way summit in Shenzhen (AP/Reuters)
  1     ICJ: Myanmar committed genocide against the Rohingya, 9-6 (UN News/Reuters/AP)
  2     Anthropic debuts on Nasdaq in biggest IPO ever, $107bn raised (NPR/Reuters)
  3     Ukraine hits Crimean Bridge for third time in a week (Reuters)
  4     Missile hits Riyadh tower as Iran war widens (NYT/Le Temps)
  5     IAEA: North Korea expanding uranium enrichment at Yongbyon (AP)
  also  COP31 final-stage talks; Cyclone Akvan nears India; migrant boat
        sinks off Senegal
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)      # warm newsprint
INK = (17, 17, 17)
RED = (178, 34, 34)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 40)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 42)
F_HERO_SUB = font("DejaVuSans.ttf", 21)
F_CAT = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSans-Bold.ttf", 24)
F_SUB = font("DejaVuSans.ttf", 16)
F_FOOT = font("DejaVuSans.ttf", 18)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
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


def draw_centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def starburst(draw, cx, cy, r, fill):
    """Simple 12-point explosion star."""
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons

def icon_summit(draw, x, y, w, h):
    """Shenzhen skyline at dusk with the US, China and Russia flags."""
    sky = (250, 196, 120)
    draw.rectangle([x, y, x + w, y + h], fill=sky)
    # sun
    draw.ellipse([x + w - 52, y + 8, x + w - 16, y + 44], fill=(255, 140, 40))
    # skyline
    base = y + h
    towers = [(0.04, 0.42), (0.16, 0.60), (0.30, 0.48), (0.44, 0.70),
              (0.60, 0.55), (0.74, 0.66), (0.86, 0.46)]
    for fx, fh in towers:
        tw = w * 0.10
        tx = x + w * fx
        draw.rectangle([tx, base - h * fh, tx + tw, base], fill=(52, 58, 74))
    # three flags on poles above the skyline
    pole_y0 = y + 6
    pole_y1 = y + 52
    fx0 = x + 24
    # US flag: red/white stripes, blue canton
    draw.line([fx0, pole_y0, fx0, pole_y1], fill=INK, width=3)
    draw.rectangle([fx0 + 2, pole_y0 + 2, fx0 + 62, pole_y0 + 34],
                   fill=WHITE, outline=INK, width=1)
    for i in range(7):
        yy = pole_y0 + 2 + i * 5
        if i % 2 == 0:
            draw.rectangle([fx0 + 2, yy, fx0 + 62, yy + 5], fill=(178, 34, 34))
    draw.rectangle([fx0 + 2, pole_y0 + 2, fx0 + 26, pole_y0 + 16],
                   fill=(27, 42, 74))
    # China flag: red field, yellow stars
    cx0 = x + w // 2 - 30
    draw.line([cx0, pole_y0, cx0, pole_y1], fill=INK, width=3)
    draw.rectangle([cx0 + 2, pole_y0 + 2, cx0 + 62, pole_y0 + 34],
                   fill=(222, 41, 16), outline=INK, width=1)
    star5(draw, cx0 + 16, pole_y0 + 12, 7, (255, 222, 0))
    star5(draw, cx0 + 34, pole_y0 + 9, 3, (255, 222, 0))
    star5(draw, cx0 + 42, pole_y0 + 16, 3, (255, 222, 0))
    star5(draw, cx0 + 34, pole_y0 + 24, 3, (255, 222, 0))
    # Russia flag: white / blue / red tricolour
    rx0 = x + w - 86
    draw.line([rx0, pole_y0, rx0, pole_y1], fill=INK, width=3)
    draw.rectangle([rx0 + 2, pole_y0 + 2, rx0 + 62, pole_y0 + 34],
                   outline=INK, width=1)
    draw.rectangle([rx0 + 2, pole_y0 + 2, rx0 + 62, pole_y0 + 13], fill=WHITE)
    draw.rectangle([rx0 + 2, pole_y0 + 13, rx0 + 62, pole_y0 + 24],
                   fill=(0, 57, 166))
    draw.rectangle([rx0 + 2, pole_y0 + 24, rx0 + 62, pole_y0 + 34],
                   fill=(213, 0, 50))


def icon_scales(draw, x, y, w, h):
    """Scales of justice on a deep-blue field."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 234, 244))
    cx, cy = x + w / 2, y + h / 2 + 8
    # pillar + crossbar
    draw.line([cx, cy - 42, cx, cy + 40], fill=(27, 42, 74), width=6)
    draw.line([cx - 52, cy - 42, cx + 52, cy - 42], fill=(27, 42, 74), width=5)
    draw.ellipse([cx - 6, cy - 54, cx + 6, cy - 42], fill=(178, 146, 40))
    draw.rectangle([cx - 26, cy + 40, cx + 26, cy + 48], fill=(27, 42, 74))
    # pans
    for sgn in (-1, 1):
        px = cx + sgn * 52
        draw.line([px, cy - 42, px, cy - 12], fill=(27, 42, 74), width=3)
        draw.line([cx + sgn * 52, cy - 42, px - 14, cy - 12],
                  fill=(27, 42, 74), width=2)
        draw.line([cx + sgn * 52, cy - 42, px + 14, cy - 12],
                  fill=(27, 42, 74), width=2)
        draw.polygon([(px - 20, cy - 12), (px + 20, cy - 12),
                      (px, cy + 10)], fill=(178, 146, 40))


def icon_chart(draw, x, y, w, h):
    """Rising market line with an ANT ticker tag."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    # grid
    for gy in range(1, 4):
        yy = y + h * gy / 4
        draw.line([x + 8, yy, x + w - 8, yy], fill=(190, 205, 190), width=1)
    # rising line + arrow
    pts = [(x + 12, y + h - 22), (x + w * 0.30, y + h - 44),
           (x + w * 0.52, y + h - 34), (x + w * 0.72, y + h - 56),
           (x + w - 16, y + 18)]
    draw.line(pts, fill=(30, 107, 74), width=5)
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 16, ey + 2), (ex - 2, ey + 16)],
                 fill=(30, 107, 74))
    # ticker tag
    draw.rectangle([x + 12, y + 8, x + 78, y + 32], fill=(27, 42, 74))
    draw.text((x + 20, y + 11), "ANT", font=font("DejaVuSans-Bold.ttf", 16),
              fill=WHITE)
    draw.text((x + w - 62, y + h - 26), "+34%", font=font("DejaVuSans-Bold.ttf", 20),
              fill=(30, 107, 74))


def icon_bridge(draw, x, y, w, h):
    """Crimean Bridge over water, explosion above the deck."""
    sky = (214, 228, 240)
    draw.rectangle([x, y, x + w, y + h], fill=sky)
    water_y = y + int(h * 0.66)
    draw.rectangle([x, water_y, x + w, y + h], fill=(58, 110, 160))
    for i in range(2):  # wave lines
        wy = water_y + 8 + i * 10
        draw.line([x + 8, wy, x + w - 8, wy], fill=(140, 185, 220), width=3)
    # bridge deck + arch + pylons
    deck_y = water_y - 12
    draw.line([x + 6, deck_y, x + w - 6, deck_y], fill=INK, width=7)
    draw.arc([x + w * 0.28, deck_y - 34, x + w * 0.72, deck_y + 14],
             start=180, end=360, fill=INK, width=6)
    for px in (0.32, 0.5, 0.68):
        draw.line([x + w * px, deck_y - 30, x + w * px, deck_y], fill=INK, width=4)
    # broken gap + explosion at centre, kept inside the icon box
    draw.rectangle([x + w * 0.47, deck_y - 4, x + w * 0.53, deck_y + 4], fill=sky)
    starburst(draw, x + w * 0.5, deck_y - 22, 16, (255, 140, 0))
    starburst(draw, x + w * 0.5, deck_y - 22, 9, (255, 210, 0))


def icon_tower(draw, x, y, w, h):
    """Riyadh tower at night, blast at the crown."""
    draw.rectangle([x, y, x + w, y + h], fill=(30, 32, 48))
    # stars
    for sx, sy in ((0.12, 0.14), (0.85, 0.10), (0.70, 0.22), (0.30, 0.08)):
        star5(draw, x + w * sx, y + h * sy, 3, WHITE)
    cx = x + w / 2
    base = y + h
    # tower body, tapering
    draw.polygon([(cx - 34, base), (cx - 18, y + 26), (cx + 18, y + 26),
                  (cx + 34, base)], fill=(120, 128, 150))
    for wy in range(6):  # lit windows
        yy = y + 34 + wy * 12
        ww = 26 - wy * 2
        draw.rectangle([cx - ww / 2, yy, cx + ww / 2, yy + 5], fill=(255, 210, 0))
    # blast at the crown
    starburst(draw, cx, y + 22, 24, (255, 140, 0))
    starburst(draw, cx, y + 22, 12, (255, 210, 0))
    # small buildings
    draw.rectangle([x + 8, base - 22, x + 52, base], fill=(52, 58, 74))
    draw.rectangle([x + w - 52, base - 30, x + w - 8, base], fill=(52, 58, 74))


def icon_atom(draw, x, y, w, h):
    """Atom: nucleus with horizontal and vertical electron orbits."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 230, 240))
    cx, cy = x + w / 2, y + h / 2
    # horizontal orbit (fits the wide icon box) + vertical orbit (fits height)
    draw.ellipse([cx - 118, cy - 15, cx + 118, cy + 15],
                 outline=(91, 44, 111), width=3)
    draw.ellipse([cx - 15, cy - 34, cx + 15, cy + 34],
                 outline=(91, 44, 111), width=3)
    # electrons on the orbits
    for ex, ey in ((cx - 118, cy), (cx + 118, cy), (cx, cy - 34), (cx, cy + 34)):
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(178, 34, 34))
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(27, 42, 74))
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 210, 0))


# ---------------------------------------------------------------- page

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # frame
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=4)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---- masthead
    draw_centered(d, W / 2, 30, "THE WORLD IN ONE DAY", F_TITLE, INK)
    d.line([60, 92, W - 60, 92], fill=INK, width=2)
    draw_centered(d, W / 2, 102, "THURSDAY  ·  19 NOVEMBER 2026", F_DATE, RED)
    d.line([60, 152, W - 60, 152], fill=INK, width=3)

    # ---- hero: Shenzhen summit
    hx, hy, hw, hh = 24, 164, W - 48, 296
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=WHITE, outline=INK, width=2)
    d.rectangle([hx, hy, hx + hw, hy + 30], fill=(27, 42, 74))
    draw_centered(d, hx + hw / 2, hy + 4, "DIPLOMACY  —  APEC IN SHENZHEN", F_CAT, WHITE)
    head = wrap(d, "TRUMP, XI AND PUTIN MEET IN SHENZHEN", F_HERO_HEAD, hw - 40)
    y = hy + 42
    for line in head:
        d.text((hx + 20, y), line, font=F_HERO_HEAD, fill=INK)
        y += 48
    d.text((hx + 20, y + 2),
           "First three-way summit; joint pledge on nuclear risks and oil flows",
           font=F_HERO_SUB, fill=GREY)
    icon_summit(d, hx + 20, hy + 172, hw - 40, 108)

    # ---- grid of five stories
    stories = [
        ("JUSTICE  ·  THE HAGUE", (27, 42, 74), icon_scales,
         "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
         "9–6 ruling; first state found guilty"),
        ("BUSINESS  ·  NASDAQ", (30, 107, 74), icon_chart,
         "ANTHROPIC DEBUTS IN BIGGEST IPO EVER",
         "$107bn IPO; shares opened +34%"),
        ("UKRAINE  —  WAR IN EUROPE", (122, 31, 31), icon_bridge,
         "UKRAINE HITS CRIMEAN BRIDGE AGAIN",
         "Third strike in a week — Moscow"),
        ("MIDDLE EAST", (178, 34, 34), icon_tower,
         "MISSILE HITS RIYADH TOWER AS WAR WIDENS",
         "Apparent Houthi strike on Riyadh"),
        ("ASIA  ·  NUCLEAR", (91, 44, 111), icon_atom,
         "NORTH KOREA EXPANDS URANIUM WORK",
         "IAEA: enrichment expanding"),
    ]
    gx, gy = 24, 476
    pw, ph = 314, 236
    gap = 12
    for i, (cat, accent, icon, headline, sub) in enumerate(stories):
        col, row = i % 3, i // 3
        px = gx + col * (pw + gap)
        py = gy + row * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=WHITE, outline=INK, width=2)
        d.rectangle([px, py, px + pw, py + 30], fill=accent)
        draw_centered(d, px + pw / 2, py + 4, cat, F_CAT, WHITE)
        icon(d, px + 14, py + 38, pw - 28, 76)
        lines = wrap(d, headline, F_HEAD, pw - 28)
        y = py + 120
        for line in lines[:3]:
            d.text((px + 14, y), line, font=F_HEAD, fill=INK)
            y += 28
        d.text((px + 14, py + 208), sub, font=F_SUB, fill=GREY)

    # sixth cell: ALSO TODAY
    px = gx + 2 * (pw + gap)
    py = gy + 1 * (ph + gap)
    d.rectangle([px, py, px + pw, py + ph], fill=(27, 42, 74), outline=INK, width=2)
    draw_centered(d, px + pw / 2, py + 10, "ALSO TODAY", F_CAT, (255, 210, 0))
    d.line([px + 16, py + 40, px + pw - 16, py + 40], fill=(255, 210, 0), width=2)
    also = [
        "COP31 talks enter final stage over fossil fuels",
        "Cyclone Akvan nears India's east coast",
        "Migrant boat sinks off Senegal; dozens missing",
    ]
    y = py + 54
    for item in also:
        d.text((px + 18, y), "•", font=F_SUB, fill=(255, 210, 0))
        for line in wrap(d, item, F_SUB, pw - 48):
            d.text((px + 36, y), line, font=F_SUB, fill=WHITE)
            y += 22
        y += 12

    # ---- footer
    d.line([60, 962, W - 60, 962], fill=INK, width=2)
    draw_centered(d, W / 2, 972, "Six stories, one day — Thursday 19 November 2026",
                  F_FOOT, INK)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
