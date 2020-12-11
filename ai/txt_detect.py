import cv2
from pytesseract import *
from PyDictionary import PyDictionary as pd

TEMP_DIR = 'temp/'
pytesseract.tesseract_cmd = '/bin/tesseract'

def filter_non_words(caption_data):
    caption_list = []
    
    for data in caption_data:
        if pd.meaning(data[0], disable_errors=True) is not None:
            caption_list.append(data)

    return caption_list

def txt_detect(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print('processing...')

    # output image_to_data return value as python dictionary
    detected_text = image_to_data(img, output_type=Output.DICT)

    # set all text to lowercase in "text" list and normalize confidence levels in "conf" list
    # zip both lists together, thus pairing detected text with associated confidence levels
    text_and_confs = [list(x) for x in zip([x.lower() for x in detected_text['text']], [float(x)/100 for x in detected_text['conf']])]

    # filter out all text with confidence levels lower than or equal to .3
    text_and_confs = [x for x in text_and_confs if x[1] >= .3 and len(x[0]) > 0]
    
    return filter_non_words(text_and_confs)
    

if __name__ == '__main__':
    import os
    import sys

    def print_list(l):
        for elem in l:
            print(elem)

    found = []
    # image = cv2.imread(TEMP_DIR + '03fc775d-870c-4665-b4a2-e631799dcc5a.jpg')
    image = cv2.imread('../../Image Repository/u.jpg')
    captions = txt_detect(image)
    print_list(captions)
    # txt_detect('4c7ad56c-8b20-4cdc-a941-65ac828fbd33.jpg')
    # txt_detect('7d0b96ee-ece4-4cb8-af68-0c7d7fe16bbd.jpg')
    # txt_detect('735f8dcd-779a-4c1a-a7a0-8e90a406b31d.jpg')
    # txt_detect('6867136b-f115-4dda-9810-5c95b91525dc.jpg')
    # txt_detect('a1b13ce1-9601-4bfd-b24b-0289b18bca88.jpg')
    # txt_detect('a2cdc487-137b-41ec-8e7f-0765bb4db005.jpg')
    # txt_detect('b0865f5e-cbea-4e55-b33d-3d73f2b89ef7.jpg')