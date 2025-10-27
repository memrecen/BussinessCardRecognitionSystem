import cv2
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

def is_qr(img):
    if isinstance(img, str):
        image = cv2.imread(img)
    else:
        image = img

    decoded_objects = decode(image, symbols=[ZBarSymbol.QRCODE])

    if len(decoded_objects) == 0:
        return False
    else:
        return True

def read_qr(img):
    if isinstance(img, str):
        image = cv2.imread(img)
    else:
        image = img
    decoded_objects = decode(image, symbols=[ZBarSymbol.QRCODE])
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        datas = data.strip().split('\n')
        if datas[0].startswith('MECARD'):
            lines = data.strip().split(';')
        else:
            lines = datas
        filtered = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('BEGIN') or line.startswith('END') or line.startswith('VERSION'):
                continue
            if line.startswith('N:'):
                filtered.append(line.replace('N:', '').strip())
            elif line.startswith('MECARD:N:'):
                filtered.append(line.replace('MECARD:N:', '').strip())
            elif line.startswith('EMAIL') or line.startswith('EMAIL;WORK;') or line.startswith('EMAIL;WORK;INTERNET'):
                filtered.append(line.split(':', 1)[-1].strip())
            elif line.startswith('ADR') or line.startswith('ADR;WORK:') or line.startswith('ADR;WORK:;;'):
                filtered.append(line.split(';;', 1)[-1].strip())
            elif line.startswith('FN:'):
                filtered.append(line.replace('FN:', '').strip())
            elif line.startswith('TITLE:'):
                filtered.append(line.replace('TITLE:', '').strip())
            elif line.startswith('URL:'):
                filtered.append(line.replace('URL:', '').strip())
            elif line.startswith('ORG:'):
                filtered.append(line.replace('ORG:', '').strip())
            elif line.startswith('NOTE:'):
                filtered.append(line.replace('NOTE:', '').strip())
            elif (line.startswith('TEL') or line.startswith('Tel') or line.startswith('Gsm')
                  or line.startswith('GSM') or line.startswith('Fax') or line.startswith('FAX')):
                num = line.split(':')[-1].strip()
                if num:
                    filtered.append(num)
            else:
                filtered.append(line)

        i = 1
        res = {}
        for item in filtered:
            if item.strip():
                res[f"q{i}"] = item
                i = i + 1
        return res



