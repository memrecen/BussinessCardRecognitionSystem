import cv2
import numpy as np

def edit_black(image_path):
    img = cv2.imread(image_path)

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gamma = 1.5
    look_up_table = np.array([((i / 255.0) ** (1 / gamma)) * 255 for i in range(256)]).astype("uint8")
    img = cv2.LUT(img, look_up_table)

    img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    blur = cv2.GaussianBlur(img, (0, 0), 3)
    img = cv2.addWeighted(img, 1.3, blur, -0.3, 0)

    _, img = cv2.threshold(img, 110, 255, cv2.THRESH_TOZERO)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 1001,3)

    return img









