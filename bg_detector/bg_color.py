import cv2
import numpy as np

def detect_bg_color(image_path, resize_dim=(100, 100), bins=(32, 32, 32)):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, resize_dim)

    pixels = image.reshape((-1, 3))

    hist, edges = np.histogramdd(pixels, bins=bins, range=((0, 256), (0, 256), (0, 256)))

    dominant_idx = np.unravel_index(np.argmax(hist), hist.shape)
    r = int((dominant_idx[0] + 0.5) * (256 / bins[0]))
    g = int((dominant_idx[1] + 0.5) * (256 / bins[1]))
    b = int((dominant_idx[2] + 0.5) * (256 / bins[2]))

    if r <= 110 and g <= 110 and b <= 110:
        return "B"
    else:
        return "-"