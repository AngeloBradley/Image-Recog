from os import walk
from os import rename
from uuid import uuid4
import cv2 as cv
import json
import requests
import time
import base64
import sys

database = {}
to_be_processed = []
repo = '../../Image Repository/'
cache = 'cache/'
IMAGE_TYPES = ('.jpeg', '.jpg', '.tiff', '.png')
PROCESS_LIMIT = range(100)


def get_image_list():
    # search for new files
    print('gathering new images')
    for root, dirs, files, in walk(repo):
        for file in files:
            if file[file.rfind('.'):] in IMAGE_TYPES:
                if file not in database:
                    to_be_processed.append(file)
                    


def image_processor():
    print('processing new images')
    # for i in range(len(to_be_processed)):
    for i in PROCESS_LIMIT: #due to space constraints on dev pc, image processing is limited to the first 100 new images
        uuid = str(uuid4())
        orig_name = to_be_processed[i]
        path = repo + to_be_processed[i]
        image = cv.imread(path)
        image_shape = image.shape
        image = image.tolist()

        # gather data, convert to JSON format
        image_data = json.dumps({
            'original_name': orig_name,
            'uuid': uuid,
            'image': image,
            'image_shape': image_shape
        })

        # create image data file
        image_data_file = open(cache + uuid + ".json", 'w')
        image_data_file.write(image_data)
        image_data_file.close()

        # rename and move to cache for future deletion
        rename(path, cache + uuid + '.jpg')

        to_be_processed[i] = image_data
        # chose single int over empty string as key placeholder
        # empty string is 49 bytes, an int is 4 bytes
        database[uuid] = 1
        # print(to_be_processed[i])


def send_to_ai():
    print('sending processed images to ai')
    counter = 0
    # for image_data in to_be_processed:
    for i in PROCESS_LIMIT:
        while True:
            try: 
                if counter == 30: return
                response = requests.post('http://localhost:8080', to_be_processed[i])
                # <Response 200> is the one you want
                print(response)
                counter = counter + 1
                break
            except:
                time.sleep(5)


if __name__ == "__main__":
    while True:
        get_image_list()
        image_processor()
        send_to_ai()
        sys.exit() #for development purposes, loop should sleep after each iteration rather than exit
        time.sleep(20)
