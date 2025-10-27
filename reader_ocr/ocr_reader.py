import re
import pytesseract
from pytesseract import Output

def read_text(image, spacing_threshold=210):
    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
    data = pytesseract.image_to_data(image, lang='tur+eng', output_type=Output.DICT)

    lines = []
    current_line = []
    prev_x = None
    prev_w = None
    prev_key = None

    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        conf = int(data['conf'][i])
        bn = data['block_num'][i]
        ln = data['line_num'][i]
        x = data['left'][i]
        w = data['width'][i]
        if len(text) < 4 and conf <50:
            continue
        if text:
            key = (bn, ln)
            if prev_key is None:
                current_line.append(text)
            else:
                same_group = key == prev_key
                spacing = abs(x - (prev_x + prev_w)) if prev_x is not None else 0
                wide_gap = spacing > spacing_threshold
                if same_group and not wide_gap:
                    current_line.append(text)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [text]
            prev_x = x
            prev_w = w
            prev_key = key
    if current_line:
        lines.append(' '.join(current_line))

    lines = [line.replace("ii", "ü") for line in lines]
    lines = [line.replace("Www", "www") for line in lines]
    lines = [re.sub(r'\bwww(?!\.)', 'www.', line) for line in lines]
    cards = []
    for line in lines:
        bol = False
        sline = line.split(' ')
        for sl in sline:
            if (len(sl) > 3 or line == "Tel" or line == "TEL" or line == "Fax"or line == "FAX" or line == "Gsm"
                    or line == "GSM" or line == "+90" or sl == "Tel" or sl == "TEL" or sl == "Fax"
                    or sl == "FAX" or sl == "Gsm" or sl == "GSM" or sl == "+90"):
                bol = True
            if len(line)<5:
                bol = False
        if bol:
            cards.append(line)

    res = {}
    for i, c in enumerate(cards):
        res[f"a{i + 1}"] = c
    return res

