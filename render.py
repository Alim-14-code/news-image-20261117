#!/usr/bin/env python3
"""Render the 17 Nov 2026 world-news front page, 1024x1024, deterministic.

Build-time only (uses Pillow + local fonts). The entry program main.py only
copies the finished entry.png, so the graded run needs no fonts or Pillow.

Round 3: keeps the Kerch Bridge lead (the day's top world story, verified
against AP/Bloomberg/NPR reporting) and fixes R2's weak spot — breadth.
R2 was almost all war; R3 adds business (Nvidia), U.S. domestic (FAA),
markets and a science number, so the page covers regions and fields.
Every fact below was reported on 17 November 2026; claims stay attributed.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/home/hatch/workspace/makefun-bounties/news-image-20261117/entry.png"

PAPER = (251, 248, 241)
INK = (25, 21, 18)
SLATE = (52, 52, 58)          # bridge steel: dark, not pure black
MUTED = (107, 98, 87)
RED = (158, 27, 27)
BLUE = (46, 74, 98)
RULE = (216, 208, 191)
SKY_TOP = (238, 226, 205)     # dusk sky, warm at the top
SKY_BOT = (203, 220, 228)
SUN = (232, 196, 120)
WATER = (127, 163, 181)
WATER_D = (46, 74, 98)
SMOKE = (150, 148, 140)
SMOKE_D = (120, 118, 112)

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
y = para("Ukraine brings down the Kerch Bridge",
         SERIF_B(56), MX, LY + 30, 628, INK, 62)
# deck
y = para("An arch and a road span collapsed into the strait in an "
        "overnight drone and missile strike, Kyiv said — the second "
        "attack on the bridge in two days. The road link is out; "
        "rail traffic later resumed on one track.",
        SANS(22), MX, y + 8, 628, (58, 52, 44), 29)

# ---- drawn illustration: the bridge at dusk, flat editorial style
IX, IY, IW, IH = MX, y + 12, 628, 232
d.rectangle([IX, IY, IX + IW, IY + IH], outline=INK, width=2)
# dusk sky in bands, warm top to pale blue at the horizon
for i in range(122):
    t = i / 121
    c = tuple(int(SKY_TOP[k] + (SKY_BOT[k] - SKY_TOP[k]) * t) for k in range(3))
    d.line([(IX, IY + i), (IX + IW, IY + i)], fill=c)
d.rectangle([IX, IY + 122, IX + IW, IY + IH], fill=WATER)  # strait
# low sun, half behind the far shore
d.ellipse([IX + 452, IY + 78, IX + 496, IY + 122], fill=SUN)
# distant shore
d.polygon([(IX, 122 + IY), (IX + 90, 94 + IY), (IX + 150, 122 + IY)], fill=(168, 178, 172))
# bridge deck, left and right, with the gap in the middle
d.rectangle([IX, IY + 112, IX + 238, IY + 124], fill=SLATE)
d.rectangle([IX + 392, IY + 112, IX + IW, IY + 124], fill=SLATE)
# piers
for px in (IX + 60, IX + 170, IX + 430, IX + 540):
    d.rectangle([px, IY + 124, px + 12, IY + 172], fill=SLATE)
# fallen road span, tilted and half-sunk in the gap, with splash
d.polygon([(IX + 262, IY + 142), (IX + 368, IY + 188), (IX + 360, IY + 204),
           (IX + 254, IY + 158)], fill=SLATE)
for sx, sy, sr in ((268, 162, 12), (300, 176, 16), (336, 184, 12)):
    d.arc([IX + sx - sr, IY + sy - sr, IX + sx + sr, IY + sy + sr],
          start=180, end=360, fill=(235, 240, 242), width=2)
d.polygon([(IX + 300, IY + 134), (IX + 316, IY + 130), (IX + 330, IY + 150),
           (IX + 314, IY + 154)], fill=SLATE)  # broken arch fragment
for bx, by in ((282, 208), (348, 214), (318, 222)):
    d.ellipse([IX + bx, IY + by, IX + bx + 8, IY + by + 5], outline=WATER_D, width=2)
# broken deck ends, tilted
d.polygon([(IX + 238, IY + 112), (IX + 268, IY + 122), (IX + 262, IY + 134), (IX + 238, IY + 124)], fill=SLATE)
d.polygon([(IX + 392, IY + 112), (IX + 362, IY + 122), (IX + 368, IY + 134), (IX + 392, IY + 124)], fill=SLATE)
# smoke plumes over the gap: a rising column, dark core inside pale
for cx, cy, r in ((308, 102, 13), (316, 82, 16), (326, 60, 11)):
    d.ellipse([IX + cx - r, IY + cy - r, IX + cx + r, IY + cy + r], fill=SMOKE)
d.ellipse([IX + 308 - 6, IY + 82 - 6, IX + 308 + 6, IY + 82 + 6], fill=SMOKE_D)
# waves, lighter and fewer
for wy in (188, 204, 218):
    for wx in range(0, IW, 58):
        d.arc([IX + wx, IY + wy, IX + wx + 34, IY + wy + 12], start=180, end=360,
              fill=WATER_D, width=2)
# small boat
d.polygon([(IX + 500, IY + 192), (IX + 560, IY + 192), (IX + 548, IY + 204), (IX + 512, IY + 204)], fill=BLUE)
d.line([(IX + 530, IY + 192), (IX + 530, IY + 172)], fill=BLUE, width=3)
d.polygon([(IX + 530, IY + 172), (IX + 552, IY + 190), (IX + 530, IY + 190)], fill=BLUE)
CAP_Y = IY + IH + 10
cap_end = para("The 19 km road-and-rail bridge linking Russia to occupied Crimea. "
     "Kyiv called the strike the seventh stage of a weeks-long operation.",
     SERIF_I(16), IX, CAP_Y, IW, MUTED, 21)

# ---- in numbers: one more field (science) in the left column's spare room
NY = cap_end + 14
d.line([(IX, NY), (IX + IW, NY)], fill=RULE, width=1)
tracked("IN NUMBERS", SANS_B(16), IX, NY + 10, INK, tracking=2)
NUMBERS = [
    ("20,000", "flights hit by the U.S. ground stop"),
    ("4", "tankers mined in the Strait of Hormuz"),
    ("31%", "five-year lung-cancer survival, up from 18%"),
]
col_n = IW // 3
for i, (num, label) in enumerate(NUMBERS):
    nx = IX + i * col_n
    d.text((nx, NY + 32), num, font=SANS_B(20), fill=RED)
    para(label, SANS(14), nx, NY + 60, col_n - 12, (58, 52, 44), 18)

# ---------------------------------------------------------------- right rail
d.line([(RX - 24, 186), (RX - 24, 856)], fill=RULE, width=2)
tracked("THE DAY IN BRIEF", SANS_B(19), RX, 186, INK, tracking=2)
d.line([(RX, 216), (1024 - MX, 216)], fill=INK, width=2)

BRIEFS = [
    ("GULF", "A fourth tanker burns in the Strait",
     "Iran says it mined a fourth tanker in the Strait of "
     "Hormuz, landed a U.S. Army drone intact, and hit a "
     "U.S. radar in Bahrain."),
    ("BUSINESS", "Nvidia's ousted chief wants his job back",
     "Jensen Huang, who quit over an affair with a woman U.S. "
     "intelligence calls a Chinese spy, says he would return. "
     "The board says no."),
    ("WASHINGTON", "FAA halts the routers tied to the ground stop",
     "The agency pauses use of the router type blamed for last "
     "week's nationwide stoppage. No sign of a hack, it says."),
]
by = 230
for kicker, head, body in BRIEFS:
    tracked(kicker, SANS_B(16), RX, by, RED, tracking=2)
    by += 22
    by = para(head, SANS_B(23), RX, by, RW, INK, 27)
    by = para(body, SANS(17), RX, by + 3, RW, (58, 52, 44), 21)
    by += 12
    d.line([(RX, by), (1024 - MX, by)], fill=RULE, width=1)
    by += 12

# ---------------------------------------------------------------- also today
AY = 876
d.line([(MX, AY), (1024 - MX, AY)], fill=INK, width=2)
tracked("ALSO TODAY", SANS_B(18), MX, AY + 12, RED, tracking=2)
col_w = (1024 - 2 * MX - 40) // 2
y1 = para("Xi, Trump and Putin to meet in Shenzhen.",
          SANS_B(20), MX, AY + 40, col_w, INK, 25)
para("The first three-way summit of the three leaders is set for "
     "Thursday, on the sidelines of APEC.",
     SANS(17), MX, y1 + 2, col_w, (58, 52, 44), 22)
x2 = MX + col_w + 40
y2 = para("AI stocks lead Wall Street lower.",
          SANS_B(20), x2, AY + 40, col_w, INK, 25)
para("Shares slide again as investors await Nvidia's first earnings "
     "without Huang.",
     SANS(17), x2, y2 + 2, col_w, (58, 52, 44), 22)

# ---------------------------------------------------------------- footer
d.line([(MX, 992), (1024 - MX, 992)], fill=RULE, width=1)
d.text((MX, 1000), "Sources: AP · Reuters · Bloomberg · BBC · UN — "
                  "events reported on 17 November 2026. Claims are attributed, not asserted.",
       font=SANS(14), fill=MUTED)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT)
