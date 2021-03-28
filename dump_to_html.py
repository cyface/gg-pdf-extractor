import shutil
from io import StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()

with open(
    "/Users/twhite/Dropbox/Personal/Gaming/Dungeon Crawl Classics/DCC Lankhmar/DCCL11 - Rats of Ilthmar/DCC11 - Rats of Ilthmar.pdf",
    "rb",
) as fin:
    extract_text_to_fp(
        fin, output_string, laparams=LAParams(), output_type="html", codec=None
    )

with open("output/output.html", "w") as out:
    output_string.seek(0)
    shutil.copyfileobj(output_string, out)
