# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/geminigisa/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/geminigisa/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Entry for make.fun's bounty **"Sum up 18 November's world news in one image"**
([news-image-20261118](https://make.fun/bounty/news-image-20261118)).

`main.py` (Python 3.13, standard library only) checks the bounty's output caps
and copies `entry.png` to `/output/entry.png`. The image is a 1024×1024
broadsheet-style front page carrying **40 stories, every one occurring or first
reported on Wednesday 18 November 2026 (UTC)**: 3 illustrated leads (the Gulf
strikes drawn as an annotated evidence map), 10 numbered grid stories and 27
numbered briefs, with dual region/field tally bars, a UTC day-by-hours ticker,
a navy-and-gold key-figures band, a halftone "Where it happened" locator map
and a DATE CHECK box reasoning about earlier-week items and the Thursday
events that lie ahead. All artwork is original geometric drawing rendered by
`tools/make_image.py` (Pillow) at 2× with gradient skies and a deterministic
paper grain, downsampled with Lanczos; no photographs or third-party art.

- **Leads:** Iran's first strikes in two months hit US sites in Kuwait and
  Bahrain after the US strike on Qeshm Island; Anthropic prices the biggest
  IPO ever at $83 a share ($81.3bn, ~$1.5tn); GTA VI unlocks first in New
  Zealand at 11:00 GMT, rolling west through the night.
- **Grid:** the EU's proposed €45bn loan for Kyiv; Gaza's first tank advance
  since the ceasefire; Jeffries' 251–11 speaker nomination; Voyager 1 reaching
  one light-day; the Fed's "close call" October minutes; South Florida's flood
  school closures; Cyclone Akvan's 50,000 evacuations; COP31's finance
  deadlock session; Suneung eve's anti-cheat scramble; Van Gogh's record
  $190.4m auction.
- **Briefs (14–40):** Peltola's Alaska win confirmed (Senate 56–44), the US
  losing measles-free status, Nepal's disaster appeal, Delhi smog inspections,
  London's blackout hoax, Hormuz, Ella Langley's CMA sweep, Houston upsetting
  No. 1 Florida, Pew's religion projections, Robert Pattinson as Bond, Waymo's
  freeway halt, Nvidia's doubled revenue, Intel cuts, the Lutnick–Nvidia
  probe, a pulled FDA nominee, an Iranian agent sentenced, outage fears
  dismissed, Trump's Shenzhen arrival, the Heat's Vice City court, on-this-day
  history, Kenya's last Ebola patient discharged, the UN's Sudan civilian
  toll, Stojakovic's 46 against Duke, Guinea's mining-crackdown displacement,
  Besigye's health fears, renewed Ethiopia–Eritrea clashes, and Texas jumping
  Notre Dame in the CFP rankings.

Facts as reported on 18 Nov 2026 by Reuters, AP, AFP, BBC, Al Jazeera,
Euronews, CNBC, NPR, NASA, the European Commission, the Fed, Pew Research,
Sotheby's, allAfrica and The Morning Brief; disputed claims are attributed,
not stated as fact.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Offline and deterministic: both runs write identical bytes. The PNG is
1024×1024, within the bounty's 1 MiB / 1024 px caps; `main.py` verifies the
PNG signature, size and dimensions before copying.

## Build

The image was rendered in the agent session that built this entry:

```sh
python3 tools/make_image.py   # requires Pillow; writes entry.png
```

## License

MIT — see [LICENSE](LICENSE). The artwork is original; no photographs or
third-party characters are used.

---

<sub>Entered on [make.fun](https://make.fun/?ref=rn8n62kp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
