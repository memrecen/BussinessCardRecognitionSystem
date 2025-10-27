import cv2
import numpy as np

def edit_other(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gamma = 1.5
    look_up_table = np.array([((i / 255.0) ** (1 / gamma)) * 255 for i in range(256)]).astype("uint8")
    brightened = cv2.LUT(gray, look_up_table)

    denoised = cv2.bilateralFilter(brightened, d=9, sigmaColor=75, sigmaSpace=75)

    blur = cv2.GaussianBlur(denoised, (0, 0), 3)
    sharpened = cv2.addWeighted(denoised, 1.3, blur, -0.3, 0)
    return sharpened










