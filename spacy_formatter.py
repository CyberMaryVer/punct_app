import spacy
import datetime

nlp = spacy.load('ru_core_news_md')
ENTITIES = ["PER", "ORG", "DATE", "MONEY", "GPE"]


def format_red_text(text, url=""):
    return f'''<span style="background: rgb(204, 34, 34); padding: 0.45em 0.6em; margin: 0px 0.25em; line-height: '
                f'1; border-radius: 0.35em;">{text}</span>'''


def entity_info(text, eob):
    ent_info = f'''<b style="font-size:8px">    {eob}</b>''' if eob else ""
    return f'''<span style="background: rgb(255, 241, 209); padding: 0.2em 0.2em; margin: 0px 0.25em; line-height: '
                f'1; border-radius: 0.35em; border: 2px solid rgb(186, 0, 0);">{text}{ent_info}</span>'''


def format_time(sec):
    return str(datetime.timedelta(seconds=sec)).split(".")[0]


def text2html(text, ents):
    doc = nlp(text)
    space = " "
    html = ""
    for token in doc:
        if token.ent_type_ in ents:
            html += space + entity_info(token.text, False)
        elif token.tag_ == "PRP" or token.pos == "NUM":
            html += space + entity_info(token.text, False)
        elif token.is_punct:
            html += token.text
        else:
            html += space + token.text  # + (space+token.tag_)

    return html


def format_as_html(text, text_file=None):
    if text is None and text_file is not None:
        with open(text_file, "r") as reader:
            text = nlp(reader.read())
    elif text is None:
        return
    return text2html(text, ents=ENTITIES)


def format_subs(subs):
    html = """
          <head><meta charset=utf-8></head>
          <table border="1" style="border-collapse:collapse; border-color: rgb(217, 217, 217);">
          <tr>
            <th width="100">Start</th>
            <th width="100">End</th>
            <th width="700">Sentence</th>
          </tr>"""

    for sub in subs:
        sent = sub['sentence']
        start = format_time(sub['start'])
        end = format_time(sub['end'])
        sent_html = format_as_html(sent)
        html += f"""
        <tr border="1">
            <td border="1">{start}</td>
            <td border="1">{end}</td>
            <td border="1">{sent_html}</td>
        </tr>"""
    html += "</table>"
    return html
