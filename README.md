[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Kodoku05/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Kodoku05/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The World Today

An entry for make.fun **news-image-20261126**, “Sum up 26 November's world news in one image”. Thursday 26 November 2026 is presented as an original newspaper front page: four illustrated leads and 46 numbered briefs, with adjacent source tags, a Gulf oil explainer, UTC timeline, dotted location map and an older-news exclusion panel.

The 50 stories span seven regions (Americas, Europe, Africa, Middle East, South Asia, East Asia and Oceania) and 18 editorial fields. `draw_poster.py` contains the explicit assignments and verifies these counts. Its Pillow shapes and measured text produce the committed 1024 × 1024 `entry.png`. Dense briefs use compact typography to fit all requested content; the requested 30 px headlines and 20 px decks cannot fit 50 stories on this canvas. Briefs require viewing at native resolution.

`main.ts` uses only Node standard-library modules and copies the committed image without rendering, network access, clock reads or randomness. Use Node 22 with native TypeScript support (or newer):

```sh
MAKEFUN_OUTPUT_DIR=./out node main.ts
```

Without that environment variable it writes `/output/entry.png`. Copy failures are reported to stderr and return a nonzero exit status. Pillow and local DejaVu Sans fonts (Noto Sans fallback) are used only to regenerate the artwork:

```sh
python3 draw_poster.py
```

MIT licensed. No submission, bundle, or payment is performed by this repository.
