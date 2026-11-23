# Complete Series Finder

A small Flask web app that accepts a Goodreads-style bookshelf text export and returns the complete series found in it. The original command-line workflow is still available through `main.py`.

## Run locally

Requires Python 3.9 or newer.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>, choose a UTF-8 `.txt` file, and select **Find complete series**. Results are shown in the page and can be downloaded as `series_completas.txt`. Uploads are processed in memory and are not saved to disk. The app limits uploads to 2 MiB.

## Input and output

The file may contain comma-separated or whitespace-separated entries, one or more per line. For example:

```text
to-read, amazon, experiment-x-2
experiment-x-2
```

A token ending in `-N` is considered complete when it occurs exactly `N` times. Known shelf labels (`to-read`, `amazon`, `kobo`, `googlebooks`, `tor`, `ibooks`, `currently-reading`, and `collections`) are excluded. Results are formatted as `series-name,count`, one per line.

## Command-line use

Put `bookshelves.txt` beside `main.py`, then run:

```bash
python main.py
```

The results are written to `series_completas.txt`.
