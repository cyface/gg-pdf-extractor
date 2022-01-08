import shutil
from io import StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()


# Set the working dir to a dir named what you want the adventure named,
# with a file called file_path.txt that has the PDF file path in it

with open("./file_path.txt") as pdf_path_file:
    pdf_path = pdf_path_file.read().strip()

with open(pdf_path, "rb") as fin:
    extract_text_to_fp(
        fin, output_string, laparams=LAParams(), output_type="html", codec=None
    )

with open("./output.html", "w") as out:
    output_string.seek(0)
    shutil.copyfileobj(output_string, out)
