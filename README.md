# Goodman Games PDF Text Extractor

1) Create a local dir under `output` with the name of the module, and add a file in there called file_path.txt that has the local path on your filesystem to the PDF.
2) From within that dir, run:
3) `dump_to_html.py`
4) `parse_html.py`
5) Move `formatted.html` that it generates to your adventure project, under assets/text.  You can break it up into as many .html files as you want separate journals.
6) In the adventure, run `npm run compile-journals`, and it will add the .html text to the -text journal.

There is currently an issue where it gets very confused with breakout sidebars, and tends to duplicate text and move it to the wrong place.

So that requires manual cleanup.
