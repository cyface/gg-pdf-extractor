# Goodman Games PDF Text Extractor

1) Create a local dir with the name of the module, and add a file in there called file_path.txt that has the local path on your filesystem to the PDF.
2) Run dump_to_html.py
3) Run parse_html.py
4) Move `formatted.html` to your adventure project, under assets/text.  You can break it up into as many .html files as you want separate journals.
5) In the adventure, run `npm run compile-journals`, and it will add the .html text to the -text journal.

There is currently an issue where it gets very confused with breakout sidebars, and tends to duplicate text and move it to the wrong place.

So that requires manual cleanup.
