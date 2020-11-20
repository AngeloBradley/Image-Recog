import cv2
import gray as gray
import pytesseract
import numpy as np
from PIL import ImageGrab, Image
import time

def txt_detect(image):
    return []
    #pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_data(Image.open(img)))

    # ##Detect words
    # hImg, wImg,_ = img.shape
    # kernel = np.ones((2, 1), np.uint8)
    # #img = cv2.erode(gray, kernel, iterations=1)
    # img = cv2.dilate(img, kernel, iterations=1)
    # out_below = pytesseract.image_to_string(img)
    # gray = cv2.cvtColor(np.float32(img), cv2.COLOR_RGB2GRAY)
    # print("OUTPUT:", out_below)

if __name__ == '__main__':
    txt_detect("temp/1cb3d439-1f2c-410c-bdd1-0c9b3110cb2d.jpg")