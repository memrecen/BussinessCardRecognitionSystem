import os
from reader_qr.qr_reader import read_qr
from reader_qr.qr_reader import is_qr
from bg_detector.bg_color import detect_bg_color
from editor.edit_black import edit_black
from editor.edit_other import edit_other
from reader_ocr.ocr_reader import read_text

def process_card(image_path):

    qr_data = {}
    if is_qr(image_path):
        qr_data = read_qr(image_path)
        print(qr_data)

    bg = detect_bg_color(image_path)

    if bg == "B":
        edited = edit_black(image_path)
    else:
        edited = edit_other(image_path)

    ocr_data = read_text(edited)
    print(ocr_data)

    os.makedirs("output", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join("output", f"{base_name}.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        if qr_data:
            f.write("--- QR DATA ---\n")
            for k, v in qr_data.items():
                f.write(f"{k}: {v}\n")
            f.write("\n")

        f.write("--- OCR DATA ---\n")
        for k, v in ocr_data.items():
            f.write(f"{k}: {v}\n")

    process_card("input/qr11.jpeg")

