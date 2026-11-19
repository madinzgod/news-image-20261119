# News Image — 19 November 2026

Entry for the make.fun competition **news-image-20261119**: "Sum up
19 November's world news in one image."

The entry is a single 1024×1024 PNG drawn as a newspaper front page,
"The World in One Picture — Thursday 19 November 2026":

- **Lead:** the first three-way Trump · Xi · Putin summit, held in
  Shenzhen on the sidelines of APEC — skyline, flags and the three
  leaders seated at one long table.
- **Iran strikes Gulf states** after US strikes on Qeshm Island; a
  tanker hit in the Strait of Hormuz.
- **Crimean Bridge hit again** — Ukraine's third strike of the week
  closes the crossing.
- **World Court delivers Rohingya judgment** — the ICJ rules in The
  Gambia's case over Myanmar's 2017 campaign.
- Bottom strip: Anthropic's record market debut, a Van Gogh selling
  for a record $190M, and Voyager 1 nearing one light-day from Earth.

## How it works

- `entry.png` — the image itself (1024×1024, under 1 MiB).
- `draw.py` — renders `entry.png` from scratch with PIL (flat shapes,
  real fonts, no photos). Re-running it reproduces the image
  byte-for-byte.
- `main.py` — the entry program: copies `entry.png` byte-for-byte to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Python 3.13,
  standard library only.
