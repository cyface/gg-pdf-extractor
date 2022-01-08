import re

from bs4 import BeautifulSoup, NavigableString

BOLD_STYLE = "font-family: BookAntiqua-Bold; font-size:10px"
H1_STYLE = "font-family: Duvall; font-size:24px"
H2_STYLE = "font-family: Duvall-Bold; font-size:14px"
H3_STYLE = "font-family: Duvall-Bold-SC700; font-size:9px"
INITCAP_STYLE = "font-family: RomantiqueInitials; font-size:48px"
ITALIC_STYLE = "font-family: BookAntiqua-Italic"
INTRO_H1 = "<h1>Introduction</h1>"
ENCOUNTER_TITLE_STYLE = "font-family: CooperBlack; font-size:9px"

soup = BeautifulSoup(open("./output.html"), "html.parser")


def clean_text(text_to_clean):
    text_to_clean = re.sub(r"-\n", "", text_to_clean)
    text_to_clean = re.sub(r"\n", " ", text_to_clean)
    text_to_clean = re.sub(r"’", "'", text_to_clean)
    text_to_clean = re.sub(r"“", '"', text_to_clean)
    text_to_clean = re.sub(r"”", '"', text_to_clean)
    text_to_clean = re.sub(r"—", " - ", text_to_clean)
    text_to_clean = re.sub(r"×", "*", text_to_clean)
    text_to_clean = re.sub(r"•", "*", text_to_clean)
    text_to_clean = re.sub(r"…", "...", text_to_clean)
    text_to_clean = re.sub(r"</em><em>", "", text_to_clean)
    text_to_clean = re.sub(r"(\dd\d+)([\+\-\*]\d+)?", r"[[/roll \1\2]]", text_to_clean)
    text_to_clean = re.sub(r"  ", " ", text_to_clean)
    return text_to_clean


def clean_spaces(text_to_clean):
    text_to_clean = re.sub(r"  ", "", text_to_clean)
    text_to_clean = re.sub(r"<p> ", "<p>", text_to_clean)
    text_to_clean = re.sub(r" </p>", "</p>", text_to_clean)
    text_to_clean = re.sub(r"<em> ", "<em>", text_to_clean)
    text_to_clean = re.sub(r" </em>", "</em>", text_to_clean)
    text_to_clean = re.sub(r"</p><p>", "</p>\n<p>", text_to_clean)
    text_to_clean = re.sub(r"<p></p>", "<p>&nbsp;</p>", text_to_clean)
    text_to_clean = re.sub(r"<h1> ", "<h1>", text_to_clean)
    text_to_clean = re.sub(r"<h2> ", "<h2>", text_to_clean)
    text_to_clean = re.sub(r"<h3> ", "<h3>", text_to_clean)
    text_to_clean = re.sub(r" </h1>", "</h1>", text_to_clean)
    text_to_clean = re.sub(r" </h2>", "</h2>", text_to_clean)
    text_to_clean = re.sub(r" </h3>", "</h3>", text_to_clean)
    return text_to_clean.strip()


# Remove Breaks
for br in soup.find_all("br"):
    br.decompose()

# Remove Initcaps
init_caps = soup.find_all("span", {"style": INITCAP_STYLE})
for init_cap in init_caps:
    next_span = init_cap.find_next()
    next_span.string = init_cap.get_text() + next_span.string
    init_cap.decompose()

# Remove Page Numbers
page_numbers = soup.find_all(string=re.compile(r"Page \d+"))
for page_number in page_numbers:
    parent = page_number.find_parent()
    parent.decompose()

output_text = INTRO_H1
for headline in soup.find_all("span", {"style": H2_STYLE}):
    output_text += f"\n<h2>{clean_text(headline.get_text()).title()}</h2>\n"
    for item in headline.find_all_next("div"):
        # If this item is a new section, eject
        if item.find("span", {"style": H2_STYLE}):
            break

        # Format Subheadings
        if item.find("span", {"style": H1_STYLE}):
            output_text += f"\n<h1>{clean_text(item.get_text()).title()}</h1>\n"
            continue
        if item.find("span", {"style": H3_STYLE}):
            output_text += f"\n<h3>{clean_text(item.get_text()).title()}</h3>\n"
            continue

        output_text += "<p>"
        for sub_item in item.children:
            if isinstance(sub_item, NavigableString):
                output_text += clean_text(sub_item)
                continue

            if ITALIC_STYLE in sub_item.attrs.get("style", ""):
                output_text += f"  <em>{clean_text(sub_item.get_text())}</em>  "
                continue

            if BOLD_STYLE in sub_item.attrs.get("style", ""):
                output_text += f"  <strong>{clean_text(sub_item.get_text())}</strong>  "
                continue

            if ENCOUNTER_TITLE_STYLE in sub_item.attrs.get("style", ""):
                output_text += f"  <strong>{clean_text(sub_item.get_text())}</strong>  "
                continue

            output_text += clean_text(sub_item.get_text())

        output_text += "</p>"

output_text = clean_spaces(output_text)
print(output_text)
with open("./formatted.html", 'w') as out_file:
    out_file.write(output_text)
