#!/usr/bin/env python3
"""Render the 17 Nov 2026 world-news front page, 1024x1024, deterministic.

Build-time only (uses Pillow + local fonts). The entry program main.py only
copies the finished entry.png, so the graded run needs no fonts or Pillow.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/home/hatch/workspace/makefun-bounties/news-image-20261117/entry.png"

PAPER = (251, 248, 241)
INK = (25, 21, 18)
MUTED = (107, 98, 87)
RED = (158, 27, 27)
BLUE = (46, 74, 98)
RULE = (216, 208, 191)
SKY = (222, 232, 236)
WATER = (127, 163, 181)
WATER_D = (46, 74, 98)
SMOKE = (150, 148, 140)

F = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = lambda s: font("NotoSerif-Bold.ttf", s)
SERIF = lambda s: font("NotoSerif-Regular.ttf", s)
SERIF_I = lambda s: font("NotoSerif-Italic.ttf", s)
SANS_B = lambda s: font("NotoSans-Bold.ttf", s)
SANS = lambda s: font("NotoSans-Regular.ttf", s)
SANS_I = lambda s: font("NotoSans-Italic.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(text, fnt, x, y, width, fill, leading):
    """Draw wrapped paragraph; returns y after last line."""
    for line in wrap(text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y

def tracked(text, fnt, x, y, fill, tracking=2):
    """Draw letterspaced caps text; returns width used."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=fnt, fill=fill)
        cx += d.textlength(ch, font=fnt) + tracking
    return cx - x

MX = 36            # side margin
RX = 700           # right rail x
RW = 1024 - MX - RX  # right rail width = 288

# ---------------------------------------------------------------- masthead
d.text((MX, 26), "WORLD NEWS", font=SERIF_B(86), fill=INK)
d.text((1024 - MX - d.textlength("ONE DAY · 17 NOV 2026", font=SANS_B(20)), 96),
       "ONE DAY · 17 NOV 2026", font=SANS_B(20), fill=RED)
tracked("TUESDAY, 17 NOVEMBER 2026  —  THE WORLD IN ONE PAGE",
        SANS_B(17), MX, 128, MUTED, tracking=1)
d.line([(MX, 158), (1024 - MX, 158)], fill=INK, width=3)
d.line([(MX, 164), (1024 - MX, 164)], fill=RED, width=2)

# ---------------------------------------------------------------- lead story
LY = 186
tracked("UKRAINE  ·  THE WAR", SANS_B(19), MX, LY, RED, tracking=2)
y = para("Ukraine brings down the Kerch Bridge road span",
         SERIF_B(52), MX, LY + 30, 628, INK, 60)
# deck
y = para("An arch and a road section collapsed into the strait in an "
        "overnight drone and missile strike, Kyiv said — the second "
        "attack on the bridge in two days. Russia hit Kyiv's river "
        "bridges the same day.",
        SANS(22), MX, y + 6, 628, (58, 52, 44), 30)

# ---- drawn illustration: the bridge, flat editorial style
IX, IY, IW, IH = MX, y + 14, 628, 252
d.rectangle([IX, IY, IX + IW, IY + IH], outline=INK, width=2)
d.rectangle([IX, IY, IX + IW, IY + 138], fill=SKY)                    # sky
d.rectangle([IX, IY + 138, IX + IW, IY + IH], fill=WATER)             # strait
# distant shore
d.polygon([(IX, 138 + IY), (IX + 90, 108 + IY), (IX + 150, 138 + IY)], fill=(168, 178, 172))
# bridge deck, left and right, with the gap in the middle
d.rectangle([IX, IY + 118, IX + 238, IY + 132], fill=INK)
d.rectangle([IX + 392, IY + 118, IX + IW, IY + 132], fill=INK)
# piers
for px in (IX + 60, IX + 170, IX + 430, IX + 540):
    d.rectangle([px, IY + 132, px + 12, IY + 178], fill=INK)
# fallen road span, tilted and half-sunk in the gap
d.polygon([(IX + 262, IY + 150), (IX + 368, IY + 196), (IX + 360, IY + 212),
           (IX + 254, IY + 166)], fill=INK)
d.polygon([(IX + 300, IY + 142), (IX + 316, IY + 138), (IX + 330, IY + 158),
           (IX + 314, IY + 162)], fill=INK)  # broken arch fragment
for bx, by in ((282, 224), (348, 230), (318, 238)):
    d.ellipse([IX + bx, IY + by, IX + bx + 8, IY + by + 5], outline=WATER_D, width=2)
# broken deck ends, tilted
d.polygon([(IX + 238, IY + 118), (IX + 268, IY + 128), (IX + 262, IY + 140), (IX + 238, IY + 132)], fill=INK)
d.polygon([(IX + 392, IY + 118), (IX + 362, IY + 128), (IX + 368, IY + 140), (IX + 392, IY + 132)], fill=INK)
# smoke plumes over the gap: one rising column
for cx, cy, r in ((308, 108, 13), (316, 88, 16), (326, 66, 11)):
    d.ellipse([IX + cx - r, IY + cy - r, IX + cx + r, IY + cy + r], fill=SMOKE)
# waves
for wy in (196, 216, 236):
    for wx in range(0, IW, 46):
        d.arc([IX + wx, IY + wy, IX + wx + 30, IY + wy + 12], start=180, end=360,
              fill=WATER_D, width=2)
# small boat
d.polygon([(IX + 500, IY + 196), (IX + 560, IY + 196), (IX + 548, IY + 208), (IX + 512, IY + 208)], fill=BLUE)
d.line([(IX + 530, IY + 196), (IX + 530, IY + 176)], fill=BLUE, width=3)
d.polygon([(IX + 530, IY + 176), (IX + 552, IY + 194), (IX + 530, IY + 194)], fill=BLUE)
CAP_Y = IY + IH + 10
para("The 19 km road-and-rail bridge linking Russia to occupied Crimea. "
     "Rail traffic later resumed on one track; the road link is out of action.",
     SERIF_I(16), IX, CAP_Y, IW, MUTED, 21)

# ---------------------------------------------------------------- right rail
d.line([(RX - 24, 186), (RX - 24, 856)], fill=RULE, width=2)
tracked("THE DAY IN BRIEF", SANS_B(19), RX, 186, INK, tracking=2)
d.line([(RX, 216), (1024 - MX, 216)], fill=INK, width=2)

BRIEFS = [
    ("GULF", "Iran fires drones at a U.S. radar in Bahrain",
     "Bahrain says it was intercepted; no casualties or damage."),
    ("DIPLOMACY", "Xi, Trump and Putin to meet in Shenzhen",
     "China confirms a first three-way meeting on Thursday, at APEC."),
    ("GULF", "Tankers struck near the Strait of Hormuz",
     "Two tankers hit mines, Tehran says; a third U.S. carrier arrives."),
    ("ASIA", "Japan scrambles jets over Russian planes",
     "Two suspected Russian aircraft entered Japanese airspace."),
]
by = 230
for kicker, head, body in BRIEFS:
    tracked(kicker, SANS_B(16), RX, by, RED, tracking=2)
    by += 22
    by = para(head, SANS_B(23), RX, by, RW, INK, 27)
    by = para(body, SANS(17), RX, by + 3, RW, (58, 52, 44), 21)
    by += 12
    if kicker != "ASIA":
        d.line([(RX, by), (1024 - MX, by)], fill=RULE, width=1)
        by += 12

# ---------------------------------------------------------------- also today
AY = 884
d.line([(MX, AY), (1024 - MX, AY)], fill=INK, width=2)
tracked("ALSO TODAY", SANS_B(18), MX, AY + 12, RED, tracking=2)
col_w = (1024 - 2 * MX - 40) // 2
y1 = para("Pentagon fails its ninth straight audit.",
          SANS_B(20), MX, AY + 40, col_w, INK, 25)
para("Most of its units pass for the first time, covering a majority of assets.",
     SANS(17), MX, y1 + 2, col_w, (58, 52, 44), 22)
x2 = MX + col_w + 40
y2 = para("Britain sanctions eight settlement builders.",
          SANS_B(20), x2, AY + 40, col_w, INK, 25)
para("The firms build Israeli settlements in the occupied West Bank, London says.",
     SANS(17), x2, y2 + 2, col_w, (58, 52, 44), 22)

# ---------------------------------------------------------------- footer
d.line([(MX, 986), (1024 - MX, 986)], fill=RULE, width=1)
d.text((MX, 994), "Sources: Associated Press · Reuters · Bloomberg · BBC · Just Security — "
                  "events reported on 17 November 2026. Claims are attributed, not asserted.",
       font=SANS(14), fill=MUTED)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT)
