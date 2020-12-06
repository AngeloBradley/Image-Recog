from os import error

import cv2 as cv
import base64
import numpy as np
import json
import sys

caption_pool_location = 'cache/caption_pool/'
cache_location = 'cache/'

def reduce_duplicate_captions(captions):
    seen = {}

    for caption_data in captions:
        caption = caption_data[0]
        confidence = caption_data[1]

        '''
            for simplicity's sake, instances of duplicate captions (ie. an 
            image was detected to have multiple instances of the same type of object
            like an image with 3 people would have 3 "person" captions) are reduced
            to a single caption with it's confidence assigned to the highest
            confidence among the duplicates
        '''

        if caption in seen:
            if seen[caption] < confidence:
                seen[caption] = confidence
        else:
            seen[caption] = confidence

    return [[x, y] for x, y in seen.items()]


def write_image_as_b64_to_file(image, uuid):
    image = np.array(image)
    _, buffer = cv.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    with open(cache_location + uuid + '.txt', 'w') as image_file:
        image_file.write(str(jpg_as_text))

def write_metadata_to_file(data_dict, uuid):
    data_file = open(cache_location + uuid + ".json", "w")
    data_file.write(json.dumps(data_dict))
    data_file.close()

def add_image_to_database(data):
    caption_list = data.captions
    caption_list = reduce_duplicate_captions(caption_list)

    # caption_list format -> [caption_data1, caption_data2...]
    # caption_data format -> [caption, confidence]

    for caption_data in caption_list:
        caption = caption_data[0]
        confidence = caption_data[1]

        try:
            # read caption.text file line by line into a list, split each line into list by ' '
            caption_dot_text = open(
                caption_pool_location + caption + '.txt', 'r')
            lines = caption_dot_text.readlines()
            caption_dot_text.close()

            caption_dot_text_data = []
            for line in lines:
                l = line.split(' ')
                l[1] = float(l[1])
                caption_dot_text_data.append(l)

            # add new data to list
            caption_dot_text_data.append([data.uuid + '.txt', confidence])

            # sort images from highest to lowest using their confidence level as the point of comparison
            caption_dot_text_data = [[x, str(y)] for x, y in sorted(
                caption_dot_text_data, key=lambda x:x[1], reverse=True)]

            # ditch original file contents
            caption_dot_text = open(
                caption_pool_location + caption + '.txt', 'r+')
            caption_dot_text.truncate()
            caption_dot_text.close()

            # print back to file line by line ' '.join(caption_data) -> "image_name confidence\n"
            caption_dot_text = open(
                caption_pool_location + caption + '.txt', 'w')
            for item in caption_dot_text_data:
                caption_dot_text.write(' '.join(item) + '\n')
            # close file
            caption_dot_text.close()

        except Exception as e:
            print(e)

def data_processor(data):
    try:
        data_dict = data.dict()
    except:
        data_dict = asdict(data)

    # add b64 version of image file to cach
    write_image_as_b64_to_file(data.image, data.uuid)

    # add metadata file to cache
    write_metadata_to_file(data_dict, data.uuid)

    # caption handler
    add_image_to_database(data)

    caption_list = data.captions
    caption_list = reduce_duplicate_captions(caption_list)
    # caption_list format -> [caption_data1, caption_data2...]
    # caption_data format -> [caption, confidence]

    for caption_data in caption_list:

        caption = caption_data[0]
        confidence = caption_data[1]

        # update caption.txt file
        # read caption.txt file line by line into a list, split each line into list by ' '
        caption_dot_text = open(
            caption_pool_location + caption + '.txt', 'r')
        lines = caption_dot_text.readlines()
        caption_dot_text.close()
        # convert caption.txt file data into list, converting confidences to floats for later sorting
        caption_dot_text_data = []
        for line in lines:
            l = line.split(' ')
            l[1] = float(l[1])
            caption_dot_text_data.append(l)

        # add new data to list
        caption_dot_text_data.append([data.uuid + '.txt', confidence])

        # sort images from highest to lowest using their confidence level as the point of comparison
        # convert confidence levels back to strings after sorting is complete
        # final list is the caption.txt data sorted from highest to lowest confidence levels
        caption_dot_text_data = [[x, str(y)] for x, y in sorted(
            caption_dot_text_data, key=lambda x:x[1], reverse=True)]

        # ditch original file contents
        caption_dot_text = open(
            caption_pool_location + caption + '.txt', 'r+')
        caption_dot_text.truncate()
        caption_dot_text.close()

        # print back to file line by line ' '.join(caption_data) -> "image_name confidence\n"
        caption_dot_text = open(
            caption_pool_location + caption + '.txt', 'a')
        for item in caption_dot_text_data:
            caption_dot_text.write(' '.join(item) + '\n')
        # close file
        caption_dot_text.close()


if __name__ == '__main__':
    from pydantic import BaseModel
    from dataclasses import dataclass, asdict

    @dataclass
    class Data:
        original_name: str
        uuid: str
        image: list
        image_shape: tuple
        captions: list

    image = cv.imread("test_data/image.jpg")
    image = image.tolist()
    
    data1 = {
        "original_name": "image.jpg",
        "uuid": "image1",
        "image": image,
        "image_shape": (2000, 4000),
        "captions": [["fire hydrant", 98], ["person", 89], ["person", 100], ["stop sign", 55]]
    }

    data2 = {
        "original_name": "image.jpg",
        "uuid": "image2",
        "image": image,
        "image_shape": (2000, 4000),
        "captions": [["fire hydrant", 60], ["person", 70], ["person", 30], ["stop sign", 90]]
    }

    data1 = Data(data1['original_name'], data1['uuid'], data1['image'], data1['image_shape'], data1['captions'])
    data2 = Data(data2['original_name'], data2['uuid'], data2['image'], data2['image_shape'], data2['captions'])

    data_processor(data1)
    data_processor(data2)