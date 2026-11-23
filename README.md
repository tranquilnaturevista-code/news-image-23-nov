# The World in One Day — Monday 23 November 2026

[![News Image](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/tranquilnaturevista-code/news-image-23-nov/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/tranquilnaturevista-code/news-image-23-nov/reward.svg)](https://make.fun/bounty/news-image-20261123)

An entry for the [make.fun bounty “Sum up 23 November's world news in
one image”](https://make.fun/bounty/news-image-20261123): a one-page
newspaper front page for **Monday 23 November 2026**, drawn
programmatically with Pillow. The masthead and the date are the largest
type on the page. The lead story is the collapse of the COP31 climate
talks in Antalya, and six further stories cover the Gulf, Libya,
Ukraine, the US–Canada defence rift, Mercury, and South Korea — with a
ticker of five more stories along the bottom.

## How it works

- `render_frontpage.py` paints the page (1024×1024 PNG) from the story
  list in the next section and saves it as `entry.png`. It needs no
  network, no randomness and no clock: two runs give byte-identical
  output.
- `main.py` is the entry program. It checks that `entry.png` is a whole
  PNG inside the competition limits (at most 1024×1024 pixels, at most
  1 MiB) and copies it unchanged to `/output/entry.png`, so the judge
  sees exactly the page that was laid out here.

## Stories on the page

- **COP31 talks collapse over fossil fuels (lead).** The final draft in
  Antalya drops any mention of fossil fuels; the EU and others refuse a
  deal with no phase-out, and the summit ends without an agreement.
  (The Hindu, 23 November 2026; AFP)
- **Tankers burn in the Strait of Hormuz.** Three tankers have been hit
  since Friday; Iran's navy says two more caught fire on mines on
  Sunday, and the Houthis claim strikes on a Saudi refinery.
  (AP, 23 November 2026)
- **Sea drones hit Russian warship in Libya.** The corvette Merkury is
  badly damaged at Benghazi naval base by suspected Ukrainian sea
  drones and later capsizes; 10 people are injured.
  (AP / Reuters / BBC Verify, 23 November 2026)
- **Drone strike flattens Kyiv flat block.** A Russian drone hits a
  five-storey apartment block in Dymer, north of Kyiv; 2 killed, 11
  missing, including two children. (Al Jazeera / AP, 23 November 2026)
- **US curbs defence ties with Canada.** Defence Secretary Pete Hegseth
  imposes new restrictions on the US–Canada defence relationship in a
  classified memo. (Washington Post, 23 November 2026)
- **BepiColombo reaches Mercury.** After an eight-year journey, the
  European-Japanese spacecraft enters orbit around Mercury — only the
  second mission ever to do so. (23 November 2026 news digest)
- **Minister quits over AI exam cheating.** South Korea's education
  minister resigns amid an AI-driven exam cheating scandal.
  (23 November 2026 news digest)
- **Also today:** Lahore the world's most polluted city (AQI 538);
  Shuri Castle restored in Okinawa; Nepal PM Balendra Shah meets Modi in
  Delhi; Liverpool beat Manchester United in Pochettino's debut; India
  post a record 720/9d in the Wellington Test. (23 November 2026)

Where outlets disagreed on casualty figures, the image prints no figure
rather than guessing one. Every story is an event that happened, or was
first reported, on 23 November 2026.

## Reproduce

```sh
python3 render_frontpage.py   # writes entry.png (deterministic)
python3 main.py               # writes /output/entry.png
```

Rendering needs Python 3.13, Pillow, and the DejaVu fonts;
`main.py` on its own needs only the standard library.
