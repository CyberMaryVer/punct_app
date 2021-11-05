"""Tools for text postprocessing"""

MAX_SENTENCE_LEN = 250
NEXT_SENTENCE_START = [
    "на самом", "добрый день", "меня зовут", "то есть", "вот например", "это еще", "ну конечно", "тем более",
    "ну например", "потому что"
]
EXCLUSIONS = [
    "которых", "которым", "которые", "которой", "которого", "которому", "которая", "который"
]
LETTERS_TO_FILTER = "бгдеёжзйлмнпртфхцчщьыъэю"


def _merge_txt(txt_file=None, data=None):
    """Splits a sentence with length over 1000 chars into smaller sentences"""
    rows_to_merge = []
    if txt_file is not None:
        with open(txt_file, "r", encoding="utf-8") as reader:
            data = reader.readlines()
    elif data is not None and "\n" in data:
        data = data.split("\n")
    elif data is not None and len(data) > 1000:
        words = data.split()
        data = []
        sent = ""
        for idx, word in enumerate(words):
            sent += word + " "
            if idx % 500 == 0:
                data.append(sent)
                sent = ""
            elif idx == len(words) - 1:
                data.append(sent)
    elif data is not None:
        data = [data, ]

    for idx, row in enumerate(data):
        row = row.strip()
        try:
            next_word = data[idx + 1].split()[0]
            next_next_word = data[idx + 1].split()[1]
            if next_word in ["но", "а"]:
                sep = "."
            elif next_word + " " + next_next_word in NEXT_SENTENCE_START or \
                    (next_word in ["я", "это", "например", "вот"] and row.split()[-1] not in EXCLUSIONS):
                # print(data[idx + 1])
                sep = "."
            else:
                sep = ","
            row = row + sep if len(row) > 0 else ""
        except Exception as e:
            print(f"idx {idx}: {e}")
        rows_to_merge.append(row)

    rows_with_punkt = []
    for row in rows_to_merge:
        if len(row) > MAX_SENTENCE_LEN:
            row = row.replace(" я ", ". я ").replace(" например ", ". например ").replace(" ну ", ". ну ")
            row = row.replace(" а ", ". а ").replace(" но ", ". но ")
            row = row.replace(", а ", ". а ").replace(", но ", ". но ")
            for st in NEXT_SENTENCE_START:
                row = row.replace(f" {st}", f". {st}")

            # sts = len(row.split("."))
            # print(f"total number of sentences: {sts} for {row[:100]}...")
            for sent in row.split("."):
                rows_with_punkt.append(sent + ".")
        else:

            rows_with_punkt.append(row)

    rows_filtered = []
    for row in rows_with_punkt:
        for letter in LETTERS_TO_FILTER:
            _letter = f" {letter} "
            row = row.replace(_letter, " ")
        rows_filtered.append(row)

    merged = " ".join(rows_filtered)

    return merged


def get_time_steps(merged_text, time_steps):
    end = [0, ]
    merged_text = merged_text.split(".")
    subtitles = []
    for row in merged_text:
        row_time = []
        for word in row.split():
            word_time = {}
            for idx, item in enumerate(time_steps):
                if item['word'] == word.strip().lower() and end[-1] < item['start_time']:
                    end.append(item['end_time'])
                    word_time["start"] = item['start_time']
                    word_time["end"] = item['end_time']
                    row_time.append(word_time)
                    break
        try:
            # print(f"{row[:10]} {row_time[0]['start']:.2f}, {row[-10:]} {row_time[-1]['end']:.2f}")
            subtitles.append({"sentence": row,
                              "start": row_time[0]['start'],
                              "end": row_time[-1]['end']})
        except IndexError:
            # print("end")
            pass
    return subtitles


if __name__ == "__main__":
    pass
