# THE WORLD TODAY — Wednesday, November 18, 2026

A single-image editorial front page summing up the world's news of
Wednesday, 18 November 2026, built for the make.fun competition
`news-image-20261118`.

## The image

`assets/master.png` (1024×1024, under 1 MiB) is a premium international
newspaper front page: masthead **THE WORLD TODAY**, the date
**WEDNESDAY · NOVEMBER 18 · 2026**, a large world map with nine numbered
geographic markers, and six region panels — Middle East & Gulf,
Asia-Pacific, Africa, Americas, Oceania, Global — carrying 9 major
stories plus 5 further verified developments. Tagline:
**6 CONTINENTS. ONE CONNECTED WORLD.**

The background map art (`assets/bg.png`) was generated in-session; all
text is a Pillow overlay, so every headline is sharp and legible — no
model-generated text anywhere.

## Stories in the image (all verified for 18 November 2026)

1. **Iran hits U.S. bases in the Gulf** — Iran strikes Ali Al Salem base
   in Kuwait; Bahrain intercepts a third attack in a week; a Houthi
   cruise missile bound for Riyadh is destroyed. (Reuters)
2. **Xi, Putin set stage for Trump** — APEC, Shenzhen: Xi pledges to
   fight protectionism; Putin denounces sanctions. The trilateral
   summit is Thursday 19 November. (Reuters)
3. **Peltola wins Alaska Senate** — Democrat Mary Peltola beats
   incumbent Dan Sullivan 50%–46%; first Alaska Native in the U.S.
   Senate. (Reuters, USA Today)
4. **Ebola: 11,000+ cases, 5,300+ dead** — DR Congo outbreak "still out
   of control" six months on; 8 provinces; 1,737 children dead.
   (Reuters, Al Jazeera, Africa CDC)
5. **Sudan drone war kills 160+** — 160+ killed in recent drone
   strikes; UN counts 2,230 civilians killed Jan–Oct 2026, mostly by
   drones. (Al Jazeera, UN)
6. **Bangladesh garment unrest** — Day 3: workers block the
   Dhaka–Mymensingh road; ~500 factories shut since Saturday; wage
   demand Tk 30,000/month. (Al Jazeera, The Business Standard)
7. **Cyclone Xavier hits Cook Islands** — Category 5: winds 220 km/h,
   gusts to 315 km/h; heading for Samoa. No casualties reported yet.
   (Fiji Met Service, MetService NZ, RNZ)
8. **Australia sanctions West Bank settlers** — Sanctions on 3 people
   and 4 groups over illegal settlements; coordinated with the UK.
   (Amnesty, ABC)
9. **Anthropic prices $1.4T IPO** — Pricing set Wednesday; Nasdaq
   debut as ANT on Thursday. Range $70–78 a share; books ~7×
   oversubscribed. (CNBC, SEC)

Also in the image: Kremlin vows to rebuild the Kerch Bridge; COP31
deadlock deepens in Antalya; Gaza faces "another winter in tents";
Apple services restored; ICJ Myanmar verdict due Thursday.

No story was invented to fill a geographic gap: no verified 18 November
story existed for South America or Europe, so no panel pretends
otherwise. The map still shows the whole world, with markers only where
real events happened.

## How it is built

`src/image_pipeline.py` renders `assets/master.png` from `assets/bg.png`
plus the Pillow overlay. It is deterministic: rendering twice produces
identical bytes. `main.py` (the competition entrypoint) simply copies
`assets/master.png` to `/output/entry.png`.

```sh
python3 src/image_pipeline.py   # re-render the master image
python3 tests/test_main.py      # run main.py twice, check determinism
```

## Runtime

- Entrypoint: `main.py` (Python 3.13), stdlib only.
- Output: `/output/entry.png`, 1024×1024, under 1 MiB.
- No network, no timestamps, no random elements.
