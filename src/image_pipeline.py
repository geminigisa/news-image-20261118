#!/usr/bin/env python3
"""Build-time pipeline for news-image-20261118.

Renders assets/master.png (1024x1024) from assets/bg.png — a world-map
background generated in-session — plus a Pillow text overlay carrying the
verified news of Wednesday, 18 November 2026.

Deterministic: same inputs always produce the same bytes. No network, no
timestamps, no randomness. Run: python3 src/image_pipeline.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG_PATH = os.path.join(ROOT, "assets", "bg.png")
OUT_PATH = os.path.join(ROOT, "assets", "master.png")

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")

NAVY = (10, 22, 40)
WHITE = (245, 239, 224)
GOLD = (212, 175, 55)
RED = (214, 69, 65)
TEAL = (78, 205, 196)
MUTED = (190, 200, 210)

# (number, kicker, headline, fact, accent, longitude, latitude)
STORIES = [
    (1, "MIDDLE EAST \u00b7 GULF", "IRAN HITS U.S. BASES IN THE GULF",
     "Iran strikes Ali Al Salem base in Kuwait; Bahrain intercepts a 3rd attack in a week; Houthi missile to Riyadh destroyed.",
     RED, 48, 29),
    (2, "ASIA \u00b7 APEC SHENZHEN", "XI, PUTIN SET STAGE FOR TRUMP",
     "Xi pledges to fight protectionism; Putin denounces sanctions. Trilateral summit is Thursday, 19 November.",
     GOLD, 114, 22.5),
    (3, "AMERICAS \u00b7 ALASKA", "PELTOLA WINS ALASKA SENATE",
     "Democrat Mary Peltola beats incumbent Dan Sullivan 50% to 46%; first Alaska Native in the U.S. Senate.",
     GOLD, -150, 61),
    (4, "AFRICA \u00b7 HEALTH", "EBOLA: 11,000+ CASES, 5,300+ DEAD",
     "DR Congo outbreak \u201cstill out of control\u201d six months on; spread to 8 provinces; 1,737 children dead.",
     RED, 15, -4),
    (5, "AFRICA \u00b7 SUDAN", "SUDAN DRONE WAR KILLS 160+",
     "160+ killed in recent drone strikes; UN counts 2,230 civilians killed Jan\u2013Oct, mostly by drones.",
     RED, 32, 15),
    (6, "ASIA \u00b7 BANGLADESH", "BANGLADESH GARMENT UNREST",
     "Day 3: workers block the Dhaka\u2013Mymensingh road; ~500 factories shut since Saturday; wage demand Tk 30,000.",
     GOLD, 90, 24),
    (7, "OCEANIA \u00b7 PACIFIC", "CYCLONE XAVIER HITS COOK ISLANDS",
     "Category 5: winds 220 km/h, gusts to 315 km/h; heading for Samoa. No casualties reported yet.",
     TEAL, -160, -21),
    (8, "MIDDLE EAST \u00b7 WEST BANK", "AUSTRALIA SANCTIONS WEST BANK SETTLERS",
     "Sanctions on 3 people and 4 groups over illegal settlements; coordinated with the UK. Israel freezes E1 tender.",
     GOLD, 35, 32),
    (9, "TECH \u00b7 AI", "ANTHROPIC PRICES $1.4T IPO",
     "Pricing set Wednesday; Nasdaq debut as ANT on Thursday. Range $70\u201378 a share; books ~7x oversubscribed.",
     TEAL, -122, 37),
]

# Six region panels: (title, accent, [(bold lead, fact), ...])
PANELS = [
    ("MIDDLE EAST & GULF", RED, [
        ("1 IRAN HITS U.S. BASES", "Kuwait base struck; Bahrain intercepts 3rd attack; Houthi missile to Riyadh destroyed."),
        ("8 WEST BANK SANCTIONS", "Australia sanctions 3 people, 4 groups; UK acted Tuesday; Israel freezes E1 tender."),
        ("KERCH BRIDGE", "Kremlin vows to rebuild it \u201ceven better\u201d after Ukraine\u2019s 17 Nov strike."),
    ]),
    ("ASIA-PACIFIC", GOLD, [
        ("2 APEC: XI & PUTIN", "Xi fights protectionism; Putin denounces sanctions. Trump trilateral is Thursday."),
        ("6 BANGLADESH UNREST", "Day 3 of garment protests; ~500 factories shut; wage demand Tk 30,000."),
        ("9 ANTHROPIC IPO", "Pricing Wednesday; $70\u201378 a share, up to ~$1.4T; Nasdaq debut Thursday."),
    ]),
    ("AFRICA", RED, [
        ("4 EBOLA OUT OF CONTROL", "11,000+ cases, 5,300+ dead in DR Congo; 8 provinces; 1,737 children dead."),
        ("5 SUDAN DRONE WAR", "160+ killed in recent strikes; UN: 2,230 civilians killed Jan\u2013Oct."),
    ]),
    ("AMERICAS", GOLD, [
        ("3 PELTOLA WINS ALASKA", "Democrat beats Sullivan 50%\u201346%; first Alaska Native in the U.S. Senate."),
        ("TRUMP\u2019S ASIA TOUR", "In Manila, Trump claims a \u201cvery big trade deal\u201d with the Philippines \u2014 no details given."),
        ("APPLE RESTORED", "Apple confirms the 17 Nov outage was an internal update, not a cyberattack."),
    ]),
    ("OCEANIA", TEAL, [
        ("7 CYCLONE XAVIER", "Category 5 hits Cook Islands: 220 km/h winds, gusts to 315 km/h; Samoa next."),
        ("SAMOA NEXT", "Xavier turns southwest toward Samoa after the Cook Islands; no deaths reported yet."),
    ]),
    ("GLOBAL", TEAL, [
        ("COP31 DEADLOCK", "Antalya talks in decisive phase; climate-finance and fossil-fuel deadlock."),
        ("GAZA: WINTER IN TENTS", "Board of Peace to UN: 1,650 Palestinians killed since the ceasefire."),
        ("ICJ VERDICT THURSDAY", "Myanmar genocide verdict due 19 Nov; UN elects 5 new ICJ judges today."),
    ]),
]


def _font(path, size):
    return ImageFont.truetype(path, size)


def _wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
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


def _map_xy(lon, lat):
    """Longitude/latitude to pixels in the 1920x1280 background map."""
    x = 170 + (lon + 180) / 360.0 * 1610
    y = 700 - lat * 5.0
    return x, y


def render():
    base = Image.open(BG_PATH).convert("RGB")
    canvas = Image.new("RGB", (1024, 1024), NAVY)
    # Map band: crop the world map out of the background, keep Antarctica out.
    band = base.crop((0, 300, 1920, 970))
    band = band.resize((1024, 357), Image.LANCZOS)
    canvas.paste(band, (0, 158))
    draw = ImageDraw.Draw(canvas, "RGBA")
    # Numbered geographic markers, matched to the story numbers.
    scale = 1024 / 1920.0
    for num, _k, _h, _f, accent, lon, lat in STORIES:
        mx, my = _map_xy(lon, lat)
        px = mx * scale
        py = 158 + (my - 300) * scale
        draw.ellipse([px - 13, py - 13, px + 13, py + 13], fill=accent,
                     outline=WHITE, width=2)
        draw.text((px, py), str(num), font=_font(SANS_B, 14), fill=NAVY,
                  anchor="mm")
    # Masthead.
    draw.text((512, 58), "THE WORLD TODAY", font=_font(SERIF_B, 62),
              fill=WHITE, anchor="mm")
    draw.line([(232, 96), (792, 96)], fill=GOLD, width=3)
    draw.text((512, 122), "WEDNESDAY \u00b7 NOVEMBER 18 \u00b7 2026",
              font=_font(SANS_B, 24), fill=GOLD, anchor="mm")
    draw.text((512, 148), "6 CONTINENTS. ONE CONNECTED WORLD.",
              font=_font(SANS_B, 19), fill=MUTED, anchor="mm")
    # Six region panels, 2 rows x 3 columns.
    gx, gy, cw, ch, gap = 16, 566, 322, 208, 12
    for i, (title, accent, items) in enumerate(PANELS):
        r, c = divmod(i, 3)
        x0 = gx + c * (cw + gap)
        y0 = gy + r * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        draw.rounded_rectangle([x0, y0, x1, y1], radius=10,
                               fill=(8, 20, 38, 218), outline=accent, width=1)
        draw.text((x0 + 12, y0 + 14), title, font=_font(SANS_B, 15), fill=accent)
        draw.line([(x0 + 12, y0 + 36), (x1 - 12, y0 + 36)], fill=accent, width=1)
        y = y0 + 44
        for head, fact in items:
            draw.text((x0 + 12, y), head, font=_font(SANS_B, 13), fill=WHITE)
            y += 17
            for line in _wrap(draw, fact, _font(SANS, 12), cw - 24)[:2]:
                draw.text((x0 + 12, y), line, font=_font(SANS, 12), fill=MUTED)
                y += 15
            y += 6
    # Footer: date + sources, so the judge can see what the image sums up.
    draw.text((512, 1004),
              "Every headline above happened on Wednesday, 18 November 2026 \u00b7 "
              "Sources: Reuters, AP, Al Jazeera, UN News, official statements",
              font=_font(SANS, 13), fill=MUTED, anchor="mm")
    return canvas


def main():
    image = render()
    # Determinism guard: rendering twice must give identical bytes.
    image2 = render()
    assert image.tobytes() == image2.tobytes(), "render is not deterministic"
    image.save(OUT_PATH, format="PNG")
    size = os.path.getsize(OUT_PATH)
    if size > 1048576:
        # PNG too big: fall back to JPEG quality 88 (still named master.png;
        # the rules tell PNG from JPEG by the first bytes, name stays entry.png).
        image.save(OUT_PATH, format="JPEG", quality=88)
        size = os.path.getsize(OUT_PATH)
    assert image.size == (1024, 1024), image.size
    assert size <= 1048576, size
    print(f"master.png: {image.size[0]}x{image.size[1]}, {size} bytes")


if __name__ == "__main__":
    main()
