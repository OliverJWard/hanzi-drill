# hanzi-drill

Flashcard drills for Chinese characters and words, HSK 1–7 (HSK 3.0; level 7 covers HSK 7–9).

## Use it

[Download the ZIP](https://github.com/OliverJWard/hanzi-drill/archive/refs/heads/main.zip), unzip it, and open `hanzi-drill.html`. It works fully offline from then on. Progress is saved in your browser; use Export in Settings to back it up.

## Files

- `hanzi-drill.html`: the app
- `hsk1.js` … `hsk7.js`: the word list for each level, loaded by the app
- `strokes1.js` … `strokes7.js`: stroke data for each level's characters, used by Draw mode
- `vendor/`: the Hanzi Writer drawing library and its licenses
- `data/1.json` … `data/7.json`: the source word lists from [complete-hsk-vocabulary](https://github.com/drkameleon/complete-hsk-vocabulary)
- `build.py`: regenerates the level files from the source lists: `python3 build.py` (all levels) or `python3 build.py 3` (one level)
- `build_strokes.py`: regenerates the stroke files (rerun after changing the word lists): `python3 build_strokes.py`

Word list data and Hanzi Writer are MIT-licensed; stroke data is under the Arphic Public License. See `LICENSE`.
