#!/usr/bin/env python3
"""Draw 'The World Today' — a 1024x1024 newspaper front page summing up
Thursday 19 November 2026. Deterministic: no randomness, no network, no
timestamps. Run: python3 tools/draw_frontpage.py  (writes entry.png)."""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 240)
INK = (20, 20, 20)
RED = (158, 27, 27)
BLUE = (31, 68, 110)
GREY = (90, 88, 82)
RULE = (60, 58, 52)
SKY = (214, 230, 240)
SEA = (46, 98, 138)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw a wrapped paragraph; return the y just below the last line."""
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def center(d, y, text, fnt, fill=INK, cx=W // 2):
    d.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def kicker(d, x, y, text, color=RED):
    d.text((x, y), text, font=font(SANS_B, 14), fill=color)
    return y + 18


def rule(d, x0, x1, y, width=1, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def vrule(d, x, y0, y1, width=1, fill=RULE):
    d.line([(x, y0), (x, y1)], fill=fill, width=width)


# ---------------------------------------------------------------- lead art
def draw_summit(d, x, y, w, h):
    """Kylin Villa state guesthouse in Shenzhen: pavilion roof, three flags."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun
    d.ellipse([x + w - 66, y + 6, x + w - 34, y + 38], fill=(240, 196, 90))
    # distant hills
    d.polygon([(x, y + h), (x + 140, y + 26), (x + 280, y + h)], fill=(122, 148, 122))
    d.polygon([(x + 200, y + h), (x + 390, y + 20), (x + w, y + h)], fill=(96, 128, 106))
    # ground
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(104, 138, 84))
    # villa body
    bx, bw = x + 180, 220
    top = y + h - 58
    d.rectangle([bx, top, bx + bw, y + h - 18], fill=(176, 62, 52))
    d.rectangle([bx + 14, top + 10, bx + bw - 14, y + h - 18], fill=(214, 196, 168))
    # columns
    for cx in range(bx + 30, bx + bw - 20, 44):
        d.rectangle([cx, top + 10, cx + 8, y + h - 18], fill=(250, 246, 236))
    # curved golden roof
    d.polygon([(bx - 26, top + 6), (bx + bw // 2, top - 22), (bx + bw + 26, top + 6),
               (bx + bw + 10, top + 6), (bx + bw // 2, top - 8), (bx + 10, top + 6)],
              fill=(214, 164, 60))
    d.rectangle([bx - 26, top + 2, bx + bw + 26, top + 10], fill=(190, 140, 44))
    # three flag poles: US, China, Russia
    flags = [
        ("us", [(200, 40, 40), (250, 246, 236), (200, 40, 40), (250, 246, 236)]),
        ("cn", [(222, 40, 32)]),
        ("ru", [(250, 246, 236), (40, 80, 160), (200, 40, 40)]),
    ]
    for i, (name, bands) in enumerate(flags):
        px = x + 56 + i * 50
        d.line([(px, y + 14), (px, y + h - 18)], fill=(70, 66, 60), width=3)
        fw, fh = 32, 20
        for j, col in enumerate(bands):
            bh = fh // len(bands)
            d.rectangle([px, y + 14 + j * bh, px + fw, y + 14 + (j + 1) * bh], fill=col)
        if name == "us":
            d.rectangle([px, y + 14, px + 13, y + 14 + 10], fill=(31, 68, 110))
            d.ellipse([px + 4, y + 17, px + 9, y + 22], fill=(250, 246, 236))
        if name == "cn":
            d.ellipse([px + 5, y + 17, px + 10, y + 22], fill=(250, 220, 60))
    # pine trees
    for tx in (x + 480, x + 516):
        d.polygon([(tx, y + h - 44), (tx + 11, y + h - 66), (tx + 22, y + h - 44)],
                  fill=(46, 92, 60))
        d.rectangle([tx + 9, y + h - 44, tx + 13, y + h - 18], fill=(90, 66, 44))


# ------------------------------------------------------------- right-column art
def draw_scales(d, x, y, w, h):
    """Scales of justice for the ICJ ruling; all geometry inside the box."""
    cx = x + w // 2
    d.rectangle([cx - 3, y + 4, cx + 3, y + h - 8], fill=(150, 118, 58))
    d.line([(cx - 48, y + 10), (cx + 48, y + 10)], fill=(150, 118, 58), width=4)
    for sx in (cx - 48, cx + 48):
        d.line([(sx, y + 10), (sx - 18, y + h - 12)], fill=(150, 118, 58), width=2)
        d.line([(sx, y + 10), (sx + 18, y + h - 12)], fill=(150, 118, 58), width=2)
        d.pieslice([sx - 20, y + h - 16, sx + 20, y + h], 0, 180, fill=(190, 150, 70))
    d.ellipse([cx - 6, y, cx + 6, y + 10], fill=(190, 150, 70))
    d.rectangle([cx - 24, y + h - 8, cx + 24, y + h - 3], fill=(150, 118, 58))


def draw_gulf(d, x, y, w, h):
    """Dusk sky over an air base: runway, hangar, drones."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 214, 188))
    d.ellipse([x + w - 40, y + 2, x + w - 16, y + 26], fill=(232, 150, 80))
    # sea strip
    d.rectangle([x, y + h - 8, x + w, y + h], fill=SEA)
    # runway
    d.polygon([(x, y + h - 8), (x + w, y + h - 16), (x + w, y + h - 8)],
              fill=(70, 70, 74))
    # hangar
    d.pieslice([x + 12, y + h - 22, x + 100, y + h - 8], 180, 360, fill=(120, 116, 108))
    d.rectangle([x + 12, y + h - 15, x + 100, y + h - 8], fill=(120, 116, 108))
    # drones
    for dx, dy, s in ((x + 150, y + 8, 9), (x + 205, y + 16, 7), (x + 250, y + 6, 6)):
        d.ellipse([dx - s, dy - 2, dx + s, dy + 2], fill=(40, 40, 44))
        d.line([(dx - s - 5, dy - 4), (dx + s + 5, dy - 4)], fill=(40, 40, 44), width=2)


# ---------------------------------------------------------------- panel art
def draw_ipo(d, x, y, w, h):
    """Rising bars and an arrow for the record IPO; fits inside the box."""
    bars = [h - 22, h - 14, h - 6]
    bx = x + 20
    for bh in bars:
        d.rectangle([bx, y + h - bh, bx + 24, y + h], fill=(34, 120, 74))
        bx += 24 + 14
    d.line([(x + 12, y + h - 8), (x + w - 16, y + 4)], fill=RED, width=3)
    d.polygon([(x + w - 16, y + 4), (x + w - 32, y + 6), (x + w - 18, y + 20)],
              fill=RED)


def draw_hormuz(d, x, y, w, h):
    """Tanker on a strait with mine buoys; fits inside the box."""
    h -= 10  # shrink art so the buoys/spikes clear the caption below
    d.rectangle([x, y, x + w, y + h], fill=(196, 224, 236))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=SEA)
    # tanker hull
    d.polygon([(x + 40, y + h - 10), (x + w - 40, y + h - 10),
               (x + w - 56, y + h - 20), (x + 56, y + h - 20)], fill=(140, 44, 36))
    # container band on deck
    d.rectangle([x + 70, y + h - 28, x + w - 70, y + h - 20], fill=(214, 196, 168))
    for cx in range(x + 76, x + w - 76, 24):
        d.rectangle([cx, y + h - 27, cx + 18, y + h - 21], fill=(31, 68, 110))
    # mine buoys
    for mx in (x + 16, x + w - 22):
        d.ellipse([mx - 6, y + h - 9, mx + 6, y + h + 1], fill=(30, 30, 32))
        for ang in range(0, 360, 45):
            ex = mx + 8 * math.cos(math.radians(ang))
            ey = y + h - 4 + 8 * math.sin(math.radians(ang))
            d.line([(mx, y + h - 4), (ex, ey)], fill=(30, 30, 32), width=1)


def draw_bridge(d, x, y, w, h):
    """A bridge span with a broken, smoking middle section."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 150, 170))
    # pylons
    for px in (x + 60, x + w - 76):
        d.rectangle([px, y + 4, px + 12, y + h - 12], fill=(90, 96, 104))
    # deck, broken in the middle
    mid = x + w // 2
    d.rectangle([x, y + h - 14, mid - 30, y + h - 8], fill=(70, 76, 84))
    d.rectangle([mid + 30, y + h - 14, x + w, y + h - 8], fill=(70, 76, 84))
    # cables
    d.line([(x + 66, y + 4), (mid - 30, y + h - 14)], fill=(120, 126, 134), width=2)
    d.line([(x + w - 70, y + 4), (mid + 30, y + h - 14)], fill=(120, 126, 134), width=2)
    # smoke over the break
    for sx, sy, r in ((mid - 8, y + 8, 6), (mid + 9, y + 4, 7), (mid + 2, y + 12, 5)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 150, 148))
    # fallen span piece
    d.polygon([(mid - 22, y + h - 8), (mid + 4, y + h - 16), (mid + 22, y + h - 8)],
              fill=(70, 76, 84))


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    R = W - M  # right edge

    # ---- masthead
    center(d, 10, "THE WORLD TODAY", font(SERIF_B, 56))
    rule(d, M, R, 88, 3)
    rule(d, M, R, 94, 1)
    center(d, 104, "THURSDAY 19 NOVEMBER 2026", font(SANS_B, 18))
    center(d, 128, "18 STORIES  ·  SIX CONTINENTS  ·  ONE DAY", font(SANS, 14), GREY)
    rule(d, M, R, 150, 2)

    # ---- lead story (left, wide)
    lx, lw = M, 600
    y = 162
    y = kicker(d, lx, y, "SHENZHEN  ·  THE TRILATERAL SUMMIT")
    y = para(d, lx, y, "Trump, Xi and Putin meet in first-ever three-way summit",
             font(SERIF_B, 36), lw, 40)
    y += 4
    draw_summit(d, lx, y, lw, 104)
    y += 104 + 6
    y = para(d, lx, y,
             "The three leaders agreed a joint \u201cpeace declaration\u201d after a "
             "90-minute meeting at the Kylin Villa state guesthouse on the APEC "
             "sidelines \u2014 nuclear arms, Ukraine and Iran on the table as the "
             "New START treaty lapses.",
             font(SERIF, 16), lw, 20)
    vrule(d, 640, 162, 500)

    # ---- right column: two stories
    rx, rw = 652, R - 652
    y = 162
    y = kicker(d, rx, y, "THE HAGUE  ·  WORLD COURT")
    y = para(d, rx, y, "ICJ: Myanmar committed genocide against the Rohingya",
             font(SERIF_B, 22), rw, 25)
    draw_scales(d, rx, y + 2, rw, 36)
    y += 38
    y = para(d, rx, y,
             "The UN court\u2019s first genocide ruling: about 10,000 killed. "
             "Myanmar must investigate and compensate victims.",
             font(SERIF, 13), rw, 16)
    rule(d, rx, R, 336, 1)
    y = 344
    y = kicker(d, rx, y, "THE GULF  ·  ESCALATION")
    y = para(d, rx, y, "Iran strikes US assets in Kuwait and Bahrain",
             font(SERIF_B, 22), rw, 25)
    draw_gulf(d, rx, y + 2, rw, 36)
    y += 38
    para(d, rx, y,
         "Drones hit Ali Al Salem air base after US jets struck Qeshm Island; "
         "both say the attacks were repelled.",
         font(SERIF, 13), rw, 16)

    # ---- three panels
    rule(d, M, R, 508, 2)
    cols = [(M, 324), (360, 324), (672, 324)]
    panels = [
        ("MARKETS  ·  IPO", "Anthropic\u2019s record $81bn debut", draw_ipo,
         "About $81bn raised at $83 a share; trading starts today."),
        ("ENERGY  ·  HORMUZ", "Crude flows through Hormuz halved", draw_hormuz,
         "Flows fall to ~8.5m barrels a day; an ADNOC vessel was struck, "
         "11 hurt, one missing."),
        ("UKRAINE  ·  CRIMEA", "Crimean Bridge hit a third time", draw_bridge,
         "Rail section hit, trains halted; Russian strikes killed five, "
         "power out in five regions."),
    ]
    for (px, pw), (kick, head, art, body) in zip(cols, panels):
        y = 516
        y = kicker(d, px, y, kick)
        y = para(d, px, y, head, font(SERIF_B, 21), pw, 24)
        art(d, px, y + 2, pw, 34)
        y += 34
        para(d, px, y, body, font(SERIF, 14), pw, 16)
    vrule(d, 352, 516, 652)
    vrule(d, 664, 516, 652)

    # ---- briefs
    rule(d, M, R, 660, 2)
    d.text((M, 668), "IN BRIEF", font=font(SANS_B, 15), fill=INK)
    rule(d, M, R, 690, 1)
    briefs = [
        ("Israel pushes into central Gaza",
         "A rare ground operation beyond the Yellow Line near Nuseirat."),
        ("North Korea expands enrichment",
         "The IAEA says uranium enrichment is growing at Yongbyon."),
        ("Unrest in Bangladesh",
         "Four killed and Muhammad Yunus\u2019s ancestral home set ablaze."),
        ("Cyclone Akvan nears India",
         "90\u2013100 km/h winds off the Andhra\u2013Odisha coast; landfall Friday."),
        ("South Florida floods",
         "Over a foot of rain near Hollywood; I-95 shut, high-water rescues."),
        ("Markets slide again",
         "Dow \u2212561 to 50,198; oil ~$82 (\u22124%); gold ~$3,730; Nvidia fell ~3%."),
    ]
    bw = 472
    for i, (head, body) in enumerate(briefs):
        bx = M if i % 2 == 0 else 524
        by = 698 + (i // 2) * 42
        para(d, bx, by, head, font(SERIF_B, 16), bw, 19)
        para(d, bx, by + 20, body, font(SERIF, 13), bw, 16)

    # ---- also today
    rule(d, M, R, 826, 2)
    d.text((M, 834), "ALSO TODAY", font=font(SANS_B, 15), fill=INK)
    rule(d, M, R, 856, 1)
    also = [
        "Denmark backs Greenland\u2013US Arctic deal 109\u20130.",
        "Migrant boat sinks off Senegal; ~100 aboard.",
        "COP31 deadlocked on fossil-fuel language.",
        "Trump bought up to $265k of Nvidia stock.",
        "LPG tanker Gas Husky sinks off Bulgaria.",
        "Bitcoin dips below $63,000.",
    ]
    for i, item in enumerate(also):
        ax = M + (i % 3) * 324
        ay = 864 + (i // 3) * 24
        para(d, ax, ay, "\u2022  " + item, font(SERIF, 13), 312, 16)

    # ---- day in figures
    rule(d, M, R, 912, 2)
    center(d, 920, "THE DAY IN FIGURES", font(SANS_B, 15))
    center(d, 942, "$81bn IPO  ·  8.5m bpd through Hormuz  ·  \u2212561 Dow  ·  "
                    "10,000 Rohingya killed  ·  ~100 aboard the Senegal boat",
           font(SERIF, 15), GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
