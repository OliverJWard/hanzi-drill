# hanzi-drill

Flashcard drills for Chinese characters and words, HSK 1–7 (HSK 3.0; level 7 covers HSK 7–9).

## Use it

**On a phone:** open https://oliverjward.github.io/hanzi-drill/ in Chrome (or Safari on iPhone) and choose **Add to Home screen** / **Install app**. It downloads everything once (about 9 MB), then works fully offline and updates itself when you're online.

**On a computer:** use the same link, or [download the ZIP](https://github.com/OliverJWard/hanzi-drill/archive/refs/heads/main.zip), unzip it, and open `hanzi-drill.html`.

Progress is saved only on your device, never uploaded. Use Export in Settings to back it up or move it to another device.

## Files

- `hanzi-drill.html`: the app
- `hsk1.js` … `hsk7.js`: the word list for each level, loaded by the app
- `strokes1.js` … `strokes7.js`: stroke data for each level's characters, used by Draw mode
- `vendor/`: the Hanzi Writer drawing library and its licenses
- `manifest.webmanifest`, `sw.js`, `icons/`: make the app installable and available offline
- `data/1.json` … `data/7.json`: the source word lists from [complete-hsk-vocabulary](https://github.com/drkameleon/complete-hsk-vocabulary)
- `build.py`: regenerates the level files from the source lists: `python3 build.py` (all levels) or `python3 build.py 3` (one level)
- `build_strokes.py`: regenerates the stroke files (rerun after changing the word lists): `python3 build_strokes.py`
- `build_site.py`, `.github/workflows/pages.yml`: publish the app to GitHub Pages automatically on every push to `main`

Word list data and Hanzi Writer are MIT-licensed; stroke data is under the Arphic Public License. See `LICENSE`.
