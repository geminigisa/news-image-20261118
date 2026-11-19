#!/usr/bin/env python3
"""Render the entry image: a one-page broadsheet for Wednesday 18 November 2026.

36 stories, every one occurring or first reported on the date: 3 illustrated
leads (one an annotated evidence map), 10 numbered grid stories, 23 numbered
briefs. Dual region/field tallies, a UTC day-by-hours ticker, a navy-gold
key-figures band, a locator map and a DATE CHECK box. Original geometric
artwork drawn with Pillow — no photographs, no third-party art. Facts as
reported on 18 Nov 2026 (UTC) by Reuters, AP, AFP, BBC, Al Jazeera, Euronews,
CNBC, NPR, NASA, the European Commission, the Fed, Pew, Sotheby's, allAfrica
and The Morning Brief; disputed claims are attributed.

Run:  python3 tools/make_image.py   (writes entry.png at the repository root)
Renders at 2x with a deterministic paper grain, downsamples with Lanczos.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
S = 2
W = H = 1024
M = 36
CW = W - 2 * M

PAPER = (247, 242, 232)
CARD = (252, 249, 241)
INK = (24, 24, 22)
GRAY = (104, 98, 86)
RED = (178, 38, 28)
GOLD = (196, 162, 88)
LINE = (60, 56, 48)
PANEL = (238, 232, 218)
NAVY = (20, 28, 44)
LAND = (72, 88, 108)
LAND_EDGE = (96, 114, 136)

REGIONS = {
    "EUROPE": (66, 108, 168),
    "AMERICAS": (58, 128, 80),
    "ASIA": (178, 38, 28),
    "MIDEAST": (198, 118, 40),
    "AFRICA": (138, 88, 50),
    "OCEANIA": (118, 78, 148),
    "WORLD": (108, 103, 93),
}

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(round(size * S)))


def R(x0, y0, x1, y1):
    return [x0 * S, y0 * S, x1 * S, y1 * S]


def T(x, y):
    return (x * S, y * S)


def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw * S:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, fnt, maxw, fill, leading=1.22, maxlines=None):
    x, y = xy
    lh = fnt.size * leading
    lines = wrap(d, text, fnt, maxw)
    if maxlines is not None and len(lines) > maxlines:
        raise OverflowError(f"text needs {len(lines)} lines (max {maxlines}): {text[:60]!r}")
    for ln in lines:
        d.text(T(x, y), ln, font=fnt, fill=fill)
        y += lh / S
    return y


def star(d, cx, cy, r, fill, rot=-90):
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.42
        a = math.radians(rot + i * 36)
        pts.append(T(cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=fill)


def flag_us(d, x, y, w, h):
    sh = h / 13
    for i in range(13):
        d.rectangle(R(x, y + i * sh, x + w, y + (i + 1) * sh),
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    cw, ch = w * 0.42, sh * 7
    d.rectangle(R(x, y, x + cw, y + ch), fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            star(d, x + cw * (c + 0.5) / 5, y + ch * (r + 0.5) / 4, 1.7, (255, 255, 255))
    d.rectangle(R(x, y, x + w, y + h), outline=INK, width=S)


# ── lead illustrations (panels ~306 x 83) ────────────────────────────────────

def art_gulf(d, x, y, w, h):
    """Annotated evidence map: the Gulf strikes, labelled and traced."""
    d.rectangle(R(x, y, x + w, y + h), fill=(198, 214, 222))
    landc = (226, 218, 198)
    # Iran (top), Arabia (bottom-left), UAE/Oman (right), Qatar, Bahrain
    d.polygon([T(x, y), T(x + w, y), T(x + w, y + 20), T(x + 250, y + 26),
               T(x + 210, y + 22), T(x + 160, y + 30), T(x + 110, y + 24),
               T(x + 60, y + 30), T(x + 20, y + 26), T(x, y + 30)], fill=landc, outline=LINE)
    d.polygon([T(x, y + 38), T(x + 60, y + 34), T(x + 120, y + 44), T(x + 160, y + 52),
               T(x + 178, y + 60), T(x + 170, y + h), T(x, y + h)], fill=landc, outline=LINE)
    d.polygon([T(x + 244, y + 40), T(x + w, y + 34), T(x + w, y + h), T(x + 250, y + h),
               T(x + 238, y + 56)], fill=landc, outline=LINE)
    d.polygon([T(x + 182, y + 48), T(x + 192, y + 46), T(x + 194, y + 58), T(x + 184, y + 58)], fill=landc, outline=LINE)
    d.ellipse(R(x + 198, y + 40, x + 205, y + 46), fill=landc, outline=LINE)
    d.ellipse(R(x + 246, y + 28, x + 262, y + 34), fill=landc, outline=RED)  # Qeshm
    f6 = font(F_SANS_B, 6.5)
    d.text(T(x + 140, y + 10), "IRAN", font=f6, fill=GRAY, anchor="mm")
    d.text(T(x + 34, y + 44), "KUWAIT", font=f6, fill=GRAY, anchor="mm")
    d.text(T(x + 214, y + 36), "BAHRAIN", font=f6, fill=GRAY, anchor="mm")
    d.text(T(x + 268, y + 46), "UAE", font=f6, fill=GRAY, anchor="mm")
    d.text(T(x + 90, y + 66), "SAUDI ARABIA", font=f6, fill=GRAY, anchor="mm")
    d.text(T(x + 254, y + 22), "QESHM", font=font(F_SANS_B, 6), fill=RED, anchor="mm")
    # strike traces (dashed) from the Iranian coast to the two targets
    for (tx, ty) in [(x + 34, y + 52), (x + 201, y + 43)]:
        sx0, sy0 = x + 150, y + 28
        for i in range(6):
            t0, t1 = i / 6, (i + 0.5) / 6
            d.line([T(sx0 + (tx - sx0) * t0, sy0 + (ty - sy0) * t0),
                    T(sx0 + (tx - sx0) * t1, sy0 + (ty - sy0) * t1)], fill=RED, width=S)
    for (tx, ty, tag) in [(x + 34, y + 52, "BASE HIT"), (x + 201, y + 43, "RADAR HIT")]:
        d.ellipse(R(tx - 3, ty - 3, tx + 3, ty + 3), fill=RED, outline=PAPER, width=S)
        d.rectangle(R(tx - 20, ty + 4, tx + 20, ty + 12), fill=RED)
        d.text(T(tx, ty + 8), tag, font=font(F_SANS_B, 5.5), fill=(255, 255, 255), anchor="mm")
    d.rectangle(R(x, y + h - 11, x + w, y + h), fill=NAVY)
    d.text(T(x + w / 2, y + h - 5.5), "FIRST STRIKES IN TWO MONTHS · HORMUZ BLOCKED",
           font=font(F_SANS_B, 7), fill=(232, 228, 216), anchor="mm")


def art_ipo(d, x, y, w, h):
    for i in range(int(h)):
        t = i / h
        d.rectangle(R(x, y + i, x + w, y + i + 1),
                    fill=(int(22 - 8 * t), int(32 - 10 * t), int(27 - 8 * t)))
    d.text(T(x + 10, y + 8), "ANT · NASDAQ · PRICED WEDNESDAY", font=font(F_SANS_B, 8), fill=(150, 220, 170))
    ax0, ax1 = x + 24, x + w - 24

    def px(v):
        return ax0 + (v - 65) / 25 * (ax1 - ax0)

    ay = y + 52
    d.line([T(ax0, ay), T(ax1, ay)], fill=(120, 150, 130), width=S)
    for v in (65, 70, 75, 80, 85, 90):
        d.line([T(px(v), ay - 2), T(px(v), ay + 2)], fill=(120, 150, 130), width=S)
        d.text(T(px(v), ay + 5), f"${v}", font=font(F_SANS, 7), fill=(130, 160, 140), anchor="ma")
    d.rectangle(R(px(70), y + 30, px(78), y + 44), fill=(70, 92, 80))
    d.text(T((px(70) + px(78)) / 2, y + 24), "MARKETED $70–78", font=font(F_SANS_B, 7), fill=(150, 220, 170), anchor="mm")
    d.line([T(px(83), y + 18), T(px(83), ay)], fill=(255, 120, 100), width=2 * S)
    d.rectangle(R(px(83) - 16, y + 6, px(83) + 16, y + 18), fill=RED)
    d.text(T(px(83), y + 12), "$83", font=font(F_SANS_B, 8.5), fill=(255, 255, 255), anchor="mm")
    d.rectangle(R(x, y + h - 12, x + w, y + h), fill=(10, 16, 14))
    d.text(T(x + w / 2, y + h - 6), "ABOVE RANGE · ~$1.5TN VALUE · DEBUTS THURSDAY", font=font(F_SANS_B, 7.5), fill=(150, 220, 170), anchor="mm")


def art_gta(d, x, y, w, h):
    for i in range(int(h)):
        t = i / h
        c = (int(24 + 96 * t), int(16 + 26 * t), int(54 + 36 * t))
        d.rectangle(R(x, y + i, x + w, y + i + 1), fill=c)
    sx, sy, sr = x + 232, y + 30, 20
    d.ellipse(R(sx - sr, sy - sr, sx + sr, sy + sr), fill=(255, 138, 92))
    for i in range(5):
        yy = sy + 2 + i * 4
        d.rectangle(R(sx - sr, yy, sx + sr, yy + 1.6),
                    fill=(int(24 + 96 * (yy - y) / h), int(16 + 26 * (yy - y) / h), int(54 + 36 * (yy - y) / h)))
    for bx, bw, bh in [(16, 20, 12), (44, 16, 18), (84, 22, 14), (120, 18, 20),
                       (156, 24, 12), (196, 16, 16), (240, 20, 14), (268, 18, 18)]:
        d.rectangle(R(x + bx, y + 60 - bh, x + bx + bw, y + 66), fill=(62, 32, 78))
    buildings = [(10, 26, 16), (30, 18, 22), (52, 30, 14), (70, 22, 20), (94, 34, 16),
                 (114, 20, 24), (142, 28, 14), (160, 16, 20), (184, 32, 16), (204, 22, 26),
                 (234, 26, 14), (252, 18, 22), (278, 30, 18)]
    for bx, bw, bh in buildings:
        d.rectangle(R(x + bx, y + 66 - bh, x + bx + bw, y + 66), fill=(14, 10, 26))
        for wi in range(bw // 5):
            for wj in range(bh // 6):
                if (wi * 7 + wj * 13 + bx) % 4 == 0:
                    d.rectangle(R(x + bx + 2 + wi * 5, y + 66 - bh + 2 + wj * 6,
                                  x + bx + 4 + wi * 5, y + 66 - bh + 4 + wj * 6), fill=(255, 214, 120))
    for gx in range(0, int(w) + 1, 24):
        x2 = min(max(x + w / 2 + (gx - w / 2) * 1.8, x), x + w)
        d.line([T(x + gx, y + 66), T(x2, y + 74)], fill=(255, 110, 180), width=S)
    d.line([T(x, y + 66), T(x + w, y + 66)], fill=(255, 110, 180), width=S)
    d.line([T(x, y + 70), T(x + w, y + 70)], fill=(200, 80, 150), width=S)

    def palm(px, py, ph):
        topx, topy = px + 3, py - ph
        d.polygon([T(px - 1.5, py), T(px + 1.5, py), T(topx + 1, topy), T(topx - 1, topy)], fill=(10, 8, 20))
        for a in (-170, -130, -90, -50, -10, 30):
            ar = math.radians(a)
            L = 13
            tipx = topx + L * math.cos(ar)
            tipy = topy + L * math.sin(ar) * 0.55 + 4
            midx = topx + L * 0.55 * math.cos(ar)
            midy = topy + L * 0.55 * math.sin(ar) * 0.3 - 2
            d.polygon([T(topx, topy), T(midx, midy - 1.5), T(tipx, tipy), T(midx, midy + 1.5)], fill=(10, 8, 20))
    palm(x + 26, y + 66, 26)
    palm(x + 64, y + 66, 20)
    d.text(T(x + 150, y + 34), "VI", font=font(F_SERIF_B, 34), fill=(255, 120, 180), anchor="mm")
    d.text(T(x + 150, y + 56), "V I C E  C I T Y", font=font(F_SANS_B, 8), fill=(255, 200, 230), anchor="mm")
    d.rectangle(R(x, y + h - 12, x + w, y + h), fill=(14, 10, 26))
    d.text(T(x + w / 2, y + h - 6), "FIRST UNLOCK · NEW ZEALAND 11:00 GMT", font=font(F_SANS_B, 8), fill=(255, 200, 230), anchor="mm")


# ── grid icons (22 px boxes) ─────────────────────────────────────────────────

def ic_eu(d, cx, cy, s):
    r = s / 2
    d.rectangle(R(cx - r * 0.8, cy - r * 0.6, cx + r * 0.8, cy + r * 0.6), fill=(40, 60, 130))
    for i in range(8):
        a = math.radians(i * 45 - 90)
        star(d, cx + r * 0.42 * math.cos(a), cy + r * 0.42 * math.sin(a), r * 0.12, (255, 222, 0))


def ic_tank(d, cx, cy, s):
    r = s / 2
    d.rounded_rectangle(R(cx - r * 0.85, cy + r * 0.15, cx + r * 0.85, cy + r * 0.6), radius=r * 0.2, fill=INK)
    for wx in (-0.6, -0.2, 0.2, 0.6):
        d.ellipse(R(cx + r * wx - r * 0.13, cy + r * 0.24, cx + r * wx + r * 0.13, cy + r * 0.5), fill=PAPER)
    d.rounded_rectangle(R(cx - r * 0.6, cy - r * 0.15, cx + r * 0.55, cy + r * 0.18), radius=r * 0.08, fill=INK)
    d.pieslice(R(cx - r * 0.35, cy - r * 0.5, cx + r * 0.25, cy - r * 0.05), 180, 360, fill=INK)
    d.line([T(cx + r * 0.2, cy - r * 0.3), T(cx + r * 0.95, cy - r * 0.5)], fill=INK, width=2 * S)
    d.line([T(cx - r * 0.85, cy + r * 0.72), T(cx + r * 0.85, cy + r * 0.72)], fill=RED, width=2 * S)


def ic_capitol(d, cx, cy, s):
    r = s / 2
    d.pieslice(R(cx - r * 0.45, cy - r * 0.6, cx + r * 0.45, cy + r * 0.1), 180, 360, fill=INK)
    d.line([T(cx, cy - r * 0.6), T(cx, cy - r * 0.85)], fill=INK, width=S)
    d.rectangle(R(cx - r * 0.7, cy + r * 0.1, cx + r * 0.7, cy + r * 0.55), fill=INK)
    for wx in (-0.5, -0.17, 0.17, 0.5):
        d.line([T(cx + r * wx, cy + r * 0.14), T(cx + r * wx, cy + r * 0.5)], fill=PAPER, width=S)
    d.line([T(cx - r * 0.85, cy + r * 0.62), T(cx + r * 0.85, cy + r * 0.62)], fill=RED, width=2 * S)


def ic_probe(d, cx, cy, s):
    r = s / 2
    d.arc(R(cx - r * 0.7, cy - r * 0.3, cx + r * 0.3, cy + r * 0.7), 180, 360, fill=INK, width=2 * S)
    d.line([T(cx - r * 0.2, cy + r * 0.2), T(cx + r * 0.4, cy - r * 0.4)], fill=INK, width=2 * S)
    d.rectangle(R(cx + r * 0.3, cy - r * 0.55, cx + r * 0.6, cy - r * 0.25), fill=INK)
    for rr in (0.35, 0.6):
        d.arc(R(cx + r * 0.45 - r * rr, cy - r * 0.4 - r * rr, cx + r * 0.45 + r * rr, cy - r * 0.4 + r * rr), -70, 20, fill=RED, width=S)
    star(d, cx - r * 0.6, cy - r * 0.6, r * 0.12, GOLD)


def ic_bank(d, cx, cy, s):
    r = s / 2
    d.polygon([T(cx - r * 0.8, cy - r * 0.25), T(cx, cy - r * 0.75), T(cx + r * 0.8, cy - r * 0.25)], fill=INK)
    for wx in (-0.55, -0.18, 0.18, 0.55):
        d.rectangle(R(cx + r * wx - r * 0.09, cy - r * 0.2, cx + r * wx + r * 0.09, cy + r * 0.45), fill=INK)
    d.rectangle(R(cx - r * 0.8, cy + r * 0.5, cx + r * 0.8, cy + r * 0.65), fill=INK)
    d.line([T(cx - r * 0.8, cy + r * 0.78), T(cx + r * 0.8, cy + r * 0.78)], fill=RED, width=2 * S)


def ic_flood(d, cx, cy, s):
    r = s / 2
    d.polygon([T(cx - r * 0.55, cy - r * 0.1), T(cx, cy - r * 0.65), T(cx + r * 0.55, cy - r * 0.1)], fill=INK)
    d.rectangle(R(cx - r * 0.4, cy - r * 0.1, cx + r * 0.4, cy + r * 0.35), fill=INK)
    for wx in (-0.7, -0.2, 0.3):
        d.arc(R(cx + r * wx - r * 0.25, cy + r * 0.3, cx + r * wx + r * 0.25, cy + r * 0.62), 0, 180, fill=RED, width=2 * S)
    d.line([T(cx - r * 0.85, cy + r * 0.72), T(cx + r * 0.85, cy + r * 0.72)], fill=GRAY, width=S)


def ic_cyclone(d, cx, cy, s):
    r = s / 2
    for rr, a0, a1 in [(0.72, 0, 250), (0.48, 120, 380), (0.26, 240, 500)]:
        d.arc(R(cx - r * rr, cy - r * rr, cx + r * rr, cy + r * rr), a0, a1, fill=INK, width=2 * S)
    d.ellipse(R(cx - r * 0.1, cy - r * 0.1, cx + r * 0.1, cy + r * 0.1), fill=RED)


def ic_thermo(d, cx, cy, s):
    r = s / 2
    d.rectangle(R(cx - r * 0.16, cy - r * 0.75, cx + r * 0.16, cy + r * 0.25), outline=INK, width=2 * S)
    d.ellipse(R(cx - r * 0.32, cy + r * 0.15, cx + r * 0.32, cy + r * 0.78), fill=RED)
    d.rectangle(R(cx - r * 0.07, cy - r * 0.4, cx + r * 0.07, cy + r * 0.3), fill=RED)
    for i in range(3):
        d.line([T(cx + r * 0.24, cy - r * 0.6 + i * r * 0.3), T(cx + r * 0.44, cy - r * 0.6 + i * r * 0.3)], fill=INK, width=S)


def ic_exam(d, cx, cy, s):
    r = s / 2
    d.rectangle(R(cx - r * 0.55, cy - r * 0.75, cx + r * 0.45, cy + r * 0.75), outline=INK, width=2 * S, fill=CARD)
    for i in range(3):
        d.line([T(cx - r * 0.35, cy - r * 0.45 + i * r * 0.3), T(cx + r * 0.25, cy - r * 0.45 + i * r * 0.3)], fill=GRAY, width=S)
    d.line([T(cx + r * 0.15, cy + r * 0.55), T(cx + r * 0.75, cy - r * 0.35)], fill=RED, width=3 * S)
    d.polygon([T(cx + r * 0.75, cy - r * 0.35), T(cx + r * 0.62, cy - r * 0.42), T(cx + r * 0.68, cy - r * 0.2)], fill=INK)


def ic_gavel(d, cx, cy, s):
    r = s / 2
    d.rectangle(R(cx - r * 0.55, cy - r * 0.7, cx + r * 0.15, cy - r * 0.3), fill=INK)
    d.line([T(cx - r * 0.2, cy - r * 0.3), T(cx + r * 0.45, cy + r * 0.45)], fill=INK, width=3 * S)
    d.rectangle(R(cx - r * 0.75, cy + r * 0.55, cx + r * 0.25, cy + r * 0.72), fill=RED)


# ── the day's stories: Wednesday 18 November 2026 ────────────────────────────

LEADS = [
    dict(n=1, region="MIDEAST", city="THE GULF", topic="WAR", lat=29.4, lon=47.9,
         head="Iran hits Kuwait & Bahrain after US strike",
         body="Iran's first strikes in two months hit US sites in Kuwait and Bahrain after Tuesday's US strike on Qeshm Island. Trump threatens retaliation over a reported 'dirty bomb' plot; Hormuz stays blocked.",
         src="BBC · AP · The Hill", art=art_gulf),
    dict(n=2, region="AMERICAS", city="NEW YORK", topic="MARKETS", lat=40.7, lon=-74.0,
         head="Anthropic prices the biggest IPO ever",
         body="The Claude maker priced at $83 a share, above the $70–78 range, raising $81.3bn at a ~$1.5tn valuation. Amazon and Google stakes revealed; trading starts Thursday on Nasdaq as ANT.",
         src="Reuters · CNBC · NPR", art=art_ipo),
    dict(n=3, region="OCEANIA", city="AUCKLAND", topic="GAMES", lat=-36.8, lon=174.8,
         head="GTA VI unlocks first in New Zealand",
         body="Rockstar's crime saga opened at midnight in New Zealand (11:00 GMT) and rolls west through the night. Pre-orders passed $1.5bn; euphoric reviews for the $1bn+ production after a 13-year wait.",
         src="AP · AFP · Engadget", art=art_gta),
]

GRID = [
    dict(n=4, region="EUROPE", city="BRUSSELS", topic="POLITICS", lat=50.8, lon=4.4, icon=ic_eu,
         head="EU proposes €45bn loan for Kyiv",
         body="€25bn weapons, €20bn budget; repaid only from Russian reparations — two-thirds of Kyiv's €70bn gap."),
    dict(n=5, region="MIDEAST", city="NUSEIRAT", topic="WAR", lat=31.4, lon=34.4, icon=ic_tank,
         head="Gaza: tanks cross the Yellow Line",
         body="First advance since the Oct 2025 ceasefire; residents flee. Gaza authorities: 1,600 killed since the truce."),
    dict(n=6, region="AMERICAS", city="WASHINGTON", topic="POLITICS", lat=38.9, lon=-77.0, icon=ic_capitol,
         head="Jeffries nominated Speaker, 251–11",
         body="Uncontested secret ballot puts the first Black Speaker in line for Jan 3; Democrats hold at least 257 seats."),
    dict(n=7, region="AMERICAS", city="PASADENA", topic="SPACE", lat=34.2, lon=-118.2, icon=ic_probe,
         head="Voyager 1 reaches one light-day",
         body="16.1bn miles at 10:16 GMT after 49 years of flight; only a carrier signal since Nov 14 — no science data."),
    dict(n=8, region="AMERICAS", city="WASHINGTON", topic="ECONOMY", lat=38.95, lon=-77.05, icon=ic_bank,
         head="Fed minutes: hike was a close call",
         body="October minutes: some wanted a 25bp hike; December expectations broadly aligned. Released 2pm ET."),
    dict(n=9, region="AMERICAS", city="MIAMI", topic="WEATHER", lat=25.8, lon=-80.2, icon=ic_flood,
         head="Florida floods shut schools",
         body="12–15 in of rain in Broward; Miami-Dade and Broward shut Wednesday and Thursday; flash-flood warnings."),
    dict(n=10, region="ASIA", city="ODISHA", topic="STORM", lat=19.4, lon=85.0, icon=ic_cyclone,
         head="Akvan: 50,000 evacuated",
         body="CM reviews the coast Wednesday; landfall Friday near Puri, winds to 110 km/h; schools shut three days."),
    dict(n=11, region="MIDEAST", city="ANTALYA", topic="CLIMATE", lat=36.9, lon=30.7, icon=ic_thermo,
         head="COP31: finance deadlock session",
         body="Presidency convenes heads of delegation on finance; the $120bn tripling fight; talks end Friday."),
    dict(n=12, region="ASIA", city="SEOUL", topic="EDUCATION", lat=37.5, lon=127.0, icon=ic_exam,
         head="Suneung eve: anti-cheat scramble",
         body="551,864 registered for Thursday's last exam of its kind; device checks and emergency alarms planned."),
    dict(n=13, region="AMERICAS", city="NEW YORK", topic="CULTURE", lat=40.72, lon=-73.99, icon=ic_gavel,
         head="Van Gogh sells for record $190.4m",
         body="Sotheby's: $165m hammer plus fees; heirs' provenance settlement Tuesday; 4th-priciest artwork ever."),
]

BRIEFS = [
    dict(n=14, region="AMERICAS", city="JUNEAU", text="Peltola win confirmed; Senate 56–44", lat=58.3, lon=-134.4),
    dict(n=15, region="AMERICAS", city="UNITED STATES", text="US loses measles-free status", lat=39.0, lon=-98.0),
    dict(n=16, region="ASIA", city="KATHMANDU", text="Nepal seeks billions for survivors", lat=27.7, lon=85.3),
    dict(n=17, region="ASIA", city="NEW DELHI", text="CM orders smog inspections", lat=28.6, lon=77.2),
    dict(n=18, region="EUROPE", city="LONDON", text="'Thursday blackout' hoax; no outage", lat=51.5, lon=-0.1),
    dict(n=19, region="MIDEAST", city="HORMUZ", text="Shipping blocked as Gulf widens", lat=26.6, lon=56.3),
    dict(n=20, region="AMERICAS", city="NASHVILLE", text="Ella Langley sweeps CMA Awards", lat=36.2, lon=-86.8),
    dict(n=21, region="AMERICAS", city="LAS VEGAS", text="Houston upsets No. 1 Florida, 86–76", lat=36.2, lon=-115.1),
    dict(n=22, region="AMERICAS", city="WASHINGTON", text="Pew: Muslims top Christians 2035", lat=38.85, lon=-76.95),
    dict(n=23, region="EUROPE", city="LONDON", text="Robert Pattinson is the next Bond", lat=51.52, lon=-0.15),
    dict(n=24, region="AMERICAS", city="SAN FRANCISCO", text="Waymo halts freeway rides", lat=37.8, lon=-122.4),
    dict(n=25, region="AMERICAS", city="SANTA CLARA", text="Nvidia doubles revenue: $115.8bn", lat=37.4, lon=-122.0),
    dict(n=26, region="AMERICAS", city="SANTA CLARA", text="Intel cuts more jobs", lat=37.35, lon=-121.95),
    dict(n=27, region="AMERICAS", city="WASHINGTON", text="Democrats probe Lutnick–Nvidia", lat=38.92, lon=-77.02),
    dict(n=28, region="AMERICAS", city="WASHINGTON", text="White House pulls FDA nominee", lat=38.88, lon=-76.98),
    dict(n=29, region="AMERICAS", city="UNITED STATES", text="Iranian sentenced in Trump plot", lat=38.5, lon=-97.5),
    dict(n=30, region="AMERICAS", city="UNITED STATES", text="Outage attack fears dismissed", lat=39.2, lon=-98.2),
    dict(n=31, region="ASIA", city="SHENZHEN", text="Trump arrives for first trilateral", lat=22.5, lon=114.1),
    dict(n=32, region="AMERICAS", city="MIAMI", text="Heat host Bucks on Vice City court", lat=25.78, lon=-80.22),
    dict(n=33, region="WORLD", city="ON THIS DAY", text="Mickey 1928 · standard time 1883", lat=41.9, lon=12.45),
    dict(n=34, region="AFRICA", city="NAIROBI", text="Last Ebola patient discharged", lat=-1.3, lon=36.8),
    dict(n=35, region="AFRICA", city="KHARTOUM", text="UN: 2,230 civilians killed in Sudan", lat=15.6, lon=32.5),
    dict(n=36, region="AMERICAS", city="DURHAM", text="Stojakovic torches Duke for 46", lat=36.0, lon=-78.9),
]

STATS = [
    ("$81.3bn", "raised in the record IPO"),
    ("$190.4m", "Van Gogh auction record"),
    ("16.1bn mi", "Voyager 1's distance"),
    ("251–11", "Jeffries' speaker vote"),
    ("50,000", "evacuated for Akvan"),
    ("€45bn", "EU loan proposed for Kyiv"),
]

FIELD_OF = {
    1: "WAR & SECURITY", 2: "ECONOMY & LABOUR", 3: "SOCIETY & CULTURE",
    4: "POLITICS & DIPLOMACY", 5: "WAR & SECURITY", 6: "POLITICS & DIPLOMACY",
    7: "SCIENCE & TECH", 8: "ECONOMY & LABOUR", 9: "DISASTERS & WEATHER",
    10: "DISASTERS & WEATHER", 11: "CLIMATE & ENVIRONMENT", 12: "SOCIETY & CULTURE",
    13: "SOCIETY & CULTURE", 14: "POLITICS & DIPLOMACY", 15: "SOCIETY & CULTURE",
    16: "DISASTERS & WEATHER", 17: "CLIMATE & ENVIRONMENT", 18: "SCIENCE & TECH",
    19: "WAR & SECURITY", 20: "SOCIETY & CULTURE", 21: "SOCIETY & CULTURE",
    22: "SOCIETY & CULTURE", 23: "SOCIETY & CULTURE", 24: "SCIENCE & TECH",
    25: "ECONOMY & LABOUR", 26: "ECONOMY & LABOUR", 27: "POLITICS & DIPLOMACY",
    28: "POLITICS & DIPLOMACY", 29: "JUSTICE", 30: "SCIENCE & TECH",
    31: "POLITICS & DIPLOMACY", 32: "SOCIETY & CULTURE", 33: "SOCIETY & CULTURE",
    34: "SOCIETY & CULTURE", 35: "WAR & SECURITY", 36: "SOCIETY & CULTURE",
}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 72), (-80, 70), (-65, 60), (-55, 50),
     (-70, 44), (-75, 38), (-81, 31), (-81, 25), (-90, 29), (-97, 26), (-97, 20),
     (-105, 20), (-110, 24), (-117, 33), (-124, 40), (-125, 49), (-135, 58), (-152, 60)],
    [(-58, 64), (-45, 60), (-22, 70), (-20, 76), (-35, 79), (-55, 78)],
    [(-78, 8), (-62, 10), (-52, 4), (-44, -2), (-35, -8), (-38, -15), (-48, -25),
     (-53, -34), (-58, -39), (-65, -45), (-68, -52), (-72, -50), (-73, -40),
     (-71, -30), (-70, -18), (-76, -10), (-80, -3)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 52), (5, 58), (10, 58), (18, 56),
     (22, 60), (28, 60), (30, 66), (40, 66), (45, 60), (40, 50), (30, 46), (28, 41),
     (22, 38), (15, 38), (10, 44), (3, 43), (-2, 36)],
    [(-17, 15), (-10, 25), (-5, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 12), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
     (12, -18), (9, -5), (5, 5), (-5, 5), (-10, 8)],
    [(30, 46), (40, 50), (45, 60), (40, 66), (50, 70), (70, 72), (100, 72), (130, 70),
     (160, 66), (170, 62), (160, 58), (150, 50), (140, 45), (130, 40), (122, 35),
     (120, 28), (110, 20), (105, 10), (100, 5), (98, 10), (92, 20), (88, 22),
     (80, 10), (77, 8), (72, 20), (66, 25), (58, 25), (52, 28), (48, 30), (43, 12),
     (35, 28), (32, 31), (28, 41)],
    [(114, -22), (122, -18), (130, -12), (136, -12), (142, -11), (146, -15), (150, -22),
     (153, -28), (150, -35), (144, -38), (138, -35), (132, -32), (124, -33), (116, -34), (114, -28)],
    [(-5, 50), (-3, 53), (-5, 58), (-2, 57), (0, 52)],
    [(130, 31), (135, 34), (140, 36), (141, 41), (143, 44), (140, 42), (136, 36), (131, 33)],
    [(95, 5), (102, -2), (106, -6), (103, -5), (97, 2)],
    [(109, 1), (115, 4), (119, 1), (116, -3), (110, -2)],
    [(105, -6), (112, -7), (114, -8), (108, -7)],
    [(44, -12), (48, -14), (50, -18), (47, -24), (44, -20)],
    [(173, -35), (175, -38), (174, -40), (172, -44), (168, -46), (170, -43), (172, -40)],
]


def draw_map(d, x, y, w, h):
    d.rectangle(R(x, y, x + w, y + h), fill=NAVY)
    lon0, lon1, lat0, lat1 = -180, 180, 78, -58

    def proj(lon, lat):
        return (x + (lon - lon0) / (lon1 - lon0) * w, y + (lat0 - lat) / (lat0 - lat1) * h)

    for glon in range(-150, 180, 30):
        a, b = proj(glon, lat0), proj(glon, lat1)
        d.line([T(*a), T(*b)], fill=(32, 42, 62), width=S)
    for glat in range(-30, 78, 30):
        a, b = proj(lon0, glat), proj(lon1, glat)
        d.line([T(*a), T(*b)], fill=(32, 42, 62), width=S)
    for poly in CONTINENTS:
        d.polygon([T(*proj(lon, lat)) for lon, lat in poly], fill=LAND, outline=LAND_EDGE)
    for s in BRIEFS:
        px, py = proj(s["lon"], s["lat"])
        d.ellipse(R(px - 2.2, py - 2.2, px + 2.2, py + 2.2), fill=(186, 186, 180))
    pins = [[*proj(s["lon"], s["lat"]), s["n"]] for s in LEADS + GRID]
    for _ in range(40):
        for i in range(len(pins)):
            for j in range(i + 1, len(pins)):
                dx = pins[j][0] - pins[i][0]
                dy = pins[j][1] - pins[i][1]
                dist = math.hypot(dx, dy)
                if dist < 15:
                    if dist < 0.01:
                        dx, dy, dist = 1.0, 0.3, 1.04
                    push = (15 - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    pins[i][0] -= ux * push
                    pins[i][1] -= uy * push
                    pins[j][0] += ux * push
                    pins[j][1] += uy * push
    for px, py, n in pins:
        px = min(max(px, x + 6), x + w - 6)
        py = min(max(py, y + 6), y + h - 6)
        d.ellipse(R(px - 5.5, py - 5.5, px + 5.5, py + 5.5), fill=RED, outline=PAPER, width=S)
        d.text(T(px, py + 0.3), str(n), font=font(F_SANS_B, 7), fill=(255, 255, 255), anchor="mm")


def grain(img):
    """Deterministic paper-grain overlay."""
    import random
    rng = random.Random(20261118)
    tile = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    px = tile.load()
    for ty in range(128):
        for tx in range(128):
            r = rng.random()
            if r < 0.06:
                v = 0 if r < 0.03 else 255
                px[tx, ty] = (v, v, v, 10)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for oy in range(0, img.size[1], 128):
        for ox in range(0, img.size[0], 128):
            overlay.paste(tile, (ox, oy))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def main():
    all_stories = LEADS + GRID + BRIEFS
    assert len(all_stories) == 36, f"story count {len(all_stories)} != 36"
    assert [s["n"] for s in all_stories] == list(range(1, 37))
    tally = {}
    for s in all_stories:
        tally[s["region"]] = tally.get(s["region"], 0) + 1
    assert sum(tally.values()) == 36

    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    f_run = font(F_SANS_B, 10.5)
    f_date = font(F_SERIF_B, 44)
    f_deck = font(F_SERIF, 13)
    f_tally = font(F_SANS_B, 9)
    f_field = font(F_SANS_B, 8)
    f_time = font(F_SANS, 8.5)
    f_timeb = font(F_SANS_B, 8.5)
    f_stat = font(F_SERIF_B, 22)
    f_statcap = font(F_SANS, 9)
    f_kick = font(F_SANS_B, 10.5)
    f_lhead = font(F_SERIF_B, 18)
    f_lbody = font(F_SANS, 10.4)
    f_src = font(F_SANS, 8.5)
    f_gkick = font(F_SANS_B, 9)
    f_ghead = font(F_SERIF_B, 13.8)
    f_gbody = font(F_SANS, 9.9)
    f_sec = font(F_SANS_B, 12)
    f_brief = font(F_SANS, 9.6)
    f_briefb = font(F_SANS_B, 9.6)
    f_dc = font(F_SANS, 10)
    f_dcb = font(F_SANS_B, 10.2)
    f_foot = font(F_SANS, 9.8)

    # ── running head + nameplate date ──
    d.text(T(M, 16), "THE WORLD TODAY · WORLD EDITION · DAY 322 OF 2026", font=f_run, fill=GRAY)
    d.text(T(W - M, 16), "36 STORIES · 7 REGIONS · 8 FIELDS · 13 ILLUSTRATED", font=f_run, fill=RED, anchor="ra")
    d.line([T(M, 27), T(W - M, 27)], fill=INK, width=3 * S)
    d.line([T(M, 31), T(W - M, 31)], fill=GOLD, width=S)
    d.text(T(W / 2, 52), "Wednesday 18 November 2026", font=f_date, fill=INK, anchor="mm")
    deck = "Iran hits Kuwait & Bahrain · Anthropic prices a record IPO · GTA VI unlocks in New Zealand · Voyager 1 reaches one light-day"
    assert d.textlength(deck, font=f_deck) <= CW * S, "deck too wide"
    d.text(T(W / 2, 82), deck, font=f_deck, fill=RED, anchor="mm")
    d.line([T(M, 92), T(W - M, 92)], fill=INK, width=S)

    # ── region tally bar ──
    order = ["EUROPE", "AMERICAS", "ASIA", "MIDEAST", "AFRICA", "OCEANIA", "WORLD"]
    tx = M
    segw = CW / len(order)
    for reg in order:
        cnt = tally.get(reg, 0)
        d.rectangle(R(tx, 96, tx + segw, 114), fill=REGIONS[reg])
        d.text(T(tx + segw / 2, 105), f"{reg} {cnt}", font=f_tally, fill=(255, 255, 255), anchor="mm")
        tx += segw

    # ── field tally bar ──
    ford = ["WAR & SECURITY", "POLITICS & DIPLOMACY", "ECONOMY & LABOUR", "SOCIETY & CULTURE",
            "JUSTICE", "CLIMATE & ENVIRONMENT", "DISASTERS & WEATHER", "SCIENCE & TECH"]
    ftally = {}
    for s in all_stories:
        f = FIELD_OF[s["n"]]
        ftally[f] = ftally.get(f, 0) + 1
    assert sum(ftally.values()) == 36 and len(ftally) == 8
    d.rectangle(R(M, 116, W - M, 132), fill=INK)
    fshort = {"WAR & SECURITY": "WAR & SEC.", "POLITICS & DIPLOMACY": "POLITICS",
              "ECONOMY & LABOUR": "ECONOMY", "SOCIETY & CULTURE": "SOCIETY",
              "JUSTICE": "JUSTICE", "CLIMATE & ENVIRONMENT": "CLIMATE",
              "DISASTERS & WEATHER": "WEATHER", "SCIENCE & TECH": "SCI & TECH"}
    fw = CW / 8
    for i, f in enumerate(ford):
        label = f"{fshort[f]} {ftally[f]}"
        assert d.textlength(label, font=f_field) <= (fw - 4) * S, f"field label too wide: {label}"
        d.text(T(M + i * fw + fw / 2, 124), label, font=f_field, fill=GOLD, anchor="mm")

    # ── the day by hours (UTC) ──
    d.text(T(M, 140), "THE DAY BY HOURS · UTC", font=f_timeb, fill=RED)
    ticker = "10:16 Voyager 1 light-day · 11:00 GTA unlocks NZ · 19:00 Fed minutes · EVENING Van Gogh record · CMA Awards"
    assert d.textlength(ticker, font=f_time) <= (CW - 150) * S, "ticker too wide"
    d.text(T(M + 150, 140), ticker, font=f_time, fill=GRAY)

    # ── key figures: navy band, gold serif figures ──
    d.rectangle(R(M, 150, W - M, 196), fill=(24, 32, 48))
    d.line([T(M, 150), T(W - M, 150)], fill=GOLD, width=S)
    d.line([T(M, 196), T(W - M, 196)], fill=GOLD, width=S)
    cellw = CW / 6
    for i, (num, cap) in enumerate(STATS):
        cx = M + i * cellw
        if i:
            d.line([T(cx, 156), T(cx, 190)], fill=(52, 62, 82), width=S)
        d.text(T(cx + cellw / 2, 168), num, font=f_stat, fill=GOLD, anchor="mm")
        lines = wrap(d, cap, f_statcap, cellw - 12)
        assert len(lines) == 1, f"stat caption wraps: {cap}"
        d.text(T(cx + cellw / 2, 184), cap, font=f_statcap, fill=(232, 228, 216), anchor="mm")

    # ── three lead cards ──
    lw, lh, lgap = (CW - 2 * 17) / 3, 204, 17
    for i, s in enumerate(LEADS):
        x0 = M + i * (lw + lgap)
        y0 = 204
        d.rectangle(R(x0, y0, x0 + lw, y0 + lh), fill=CARD, outline=LINE, width=S)
        d.rectangle(R(x0 + 1, y0 + 1, x0 + lw - 1, y0 + 4), fill=REGIONS[s["region"]])
        s["art"](d, x0 + 1, y0 + 4, lw - 2, 83)
        d.text(T(x0 + 10, y0 + 96), f"{s['n']} · {s['city']} · {s['topic']}", font=f_kick, fill=RED)
        d.text(T(x0 + lw - 10, y0 + 97), s["src"], font=f_src, fill=GRAY, anchor="ra")
        hy = para(d, (x0 + 10, y0 + 110), s["head"], f_lhead, lw - 20, INK, 1.12, maxlines=2)
        by = para(d, (x0 + 10, hy + 2), s["body"], f_lbody, lw - 20, INK, 1.15, maxlines=4)
        assert by <= y0 + lh - 2, f"lead {s['n']} body overflows: {by}"

    d.line([T(M, 416), T(W - M, 416)], fill=INK, width=2 * S)

    # ── ten grid stories, 2 x 5 ──
    gw, gh, ggap = (CW - 4 * 8) / 5, 124, 8
    for i, s in enumerate(GRID):
        r, c = divmod(i, 5)
        x0 = M + c * (gw + ggap)
        y0 = 424 + r * (gh + ggap)
        d.rectangle(R(x0, y0, x0 + gw, y0 + gh), fill=CARD, outline=LINE, width=S)
        d.rectangle(R(x0 + 1, y0 + 1, x0 + gw - 1, y0 + 4), fill=REGIONS[s["region"]])
        d.ellipse(R(x0 + 5, y0 + 6, x0 + 23, y0 + 24), fill=RED)
        d.text(T(x0 + 14, y0 + 15.3), str(s["n"]), font=font(F_SANS_B, 9.5), fill=(255, 255, 255), anchor="mm")
        d.text(T(x0 + 28, y0 + 9), f"{s['city']} · {s['topic']}", font=f_gkick, fill=GRAY)
        s["icon"](d, x0 + gw - 20, y0 + 20, 22)
        hy = para(d, (x0 + 8, y0 + 30), s["head"], f_ghead, gw - 16, INK, 1.1, maxlines=2)
        by = para(d, (x0 + 8, hy + 3), s["body"], f_gbody, gw - 16, INK, 1.15, maxlines=4)
        assert by <= y0 + gh - 4, f"grid {s['n']} body overflows: {by} > {y0 + gh - 4}"

    d.line([T(M, 680), T(W - M, 680)], fill=INK, width=2 * S)

    # ── bottom split: locator map + 23 briefs ──
    d.text(T(M, 690), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    draw_map(d, M, 706, 380, 176)
    d.ellipse(R(M + 2, 888, M + 8, 894), fill=RED)
    d.text(T(M + 12, 886), "1–13 leads & grid", font=f_foot, fill=GRAY)
    d.ellipse(R(M + 108, 888, M + 114, 894), fill=(150, 150, 145))
    d.text(T(M + 118, 886), "14–36 briefs · positions approximate", font=f_foot, fill=GRAY)

    bx0 = M + 396
    d.text(T(bx0, 690), "ALSO ON WEDNESDAY — 23 MORE STORIES", font=f_sec, fill=INK)
    colw = (W - M - bx0 - 14) / 2
    for i, s in enumerate(BRIEFS):
        col, row = divmod(i, 12)
        x = bx0 + col * (colw + 14)
        y = 708 + row * 16.4
        num = str(s["n"])
        d.text(T(x, y), num, font=f_briefb, fill=RED)
        nx = x + d.textlength(num + " ", font=f_briefb) / S
        city = s["city"]
        d.text(T(nx, y), city + " — ", font=f_briefb, fill=INK)
        cx2 = nx + d.textlength(city + " — ", font=f_briefb) / S
        rest = colw - (cx2 - x)
        lines = wrap(d, s["text"], f_brief, rest)
        assert len(lines) == 1, f"brief {s['n']} wraps: {s['text']!r} ({rest:.0f}px left)"
        d.text(T(cx2, y), s["text"], font=f_brief, fill=INK)

    # ── date check box ──
    d.rectangle(R(M, 908, W - M, 952), outline=RED, width=2 * S)
    d.text(T(M + 8, 914), "DATE CHECK — NOT COUNTED: FIRST REPORTED BEFORE WEDNESDAY", font=f_dcb, fill=RED)
    l1 = "Tue 17: US strike on Qeshm Island (counted above as today's widening) · SAFF final: India 2–1 Pakistan in Dhaka · Mega Millions $600M drawing."
    l2 = "Mon 16: UK hoax first debunked (still spreading) · Akvan formed (today: evacuations) · first COP31 draft. Thursday's summit talks, ICJ ruling and ANT debut lie ahead — not counted."
    for ln in (l1, l2):
        assert d.textlength(ln, font=f_dc) <= (CW - 16) * S, f"date check line too wide: {ln[:50]}"
    d.text(T(M + 8, 928), l1, font=f_dc, fill=INK)
    d.text(T(M + 8, 940), l2, font=f_dc, fill=INK)

    # ── footer ──
    d.line([T(M, 962), T(W - M, 962)], fill=LINE, width=S)
    d.text(T(M, 970), "Sources: Reuters · AP · AFP · BBC · Al Jazeera · Euronews · CNBC · NPR · NASA · EC · Fed · Pew · Sotheby's · allAfrica — reporting of 18 Nov 2026 (UTC).", font=f_foot, fill=GRAY)
    d.text(T(M, 984), "Original geometric drawings · disputed claims attributed, not stated as fact · every story occurred or was first reported on the date.", font=f_foot, fill=GRAY)
    d.text(T(W - M, 984), "The World Today · make.fun", font=f_foot, fill=GRAY, anchor="ra")

    img = grain(img)
    final = img.resize((W, H), Image.LANCZOS)
    out = ROOT / "entry.png"
    final.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {final.size[0]}x{final.size[1]})")
    print("tally:", tally)
    print("fields:", ftally)


if __name__ == "__main__":
    main()
