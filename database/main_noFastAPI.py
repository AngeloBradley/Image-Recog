from dataclasses import dataclass, asdict
from os import error
from PyDictionary import PyDictionary
import cv2 as cv
import numpy as np
import json
import heapq
import sys

cache_location = 'cache/'
caption_pool_location = 'cache/caption_pool/'
dictionary_file = 'cache/dictionary.json'
official_captions_file = 'cache/official_captions.txt'
official_captions_set = set(['dog'])
dictionary = {}


@dataclass
class Data:
    original_name: str
    uuid: str
    image: list
    image_shape: tuple
    captions: list

    # def __init__(self, data):
    #     self.original_name = data['original_name']
    #     self.uuid = data['uuid']
    #     self.image = data['image']
    #     self.image_shape = data['image_shape']
    #     self.captions = data['captions']


def post(data: Data):
    # data_dict = data.dict()

    # add image file to cache
    image = np.asarray(data.image)
    cv.imwrite(cache_location + data.uuid + ".jpg", image)

    # add metadata file to cache
    data_file = open(cache_location + data.uuid + ".json", "w")
    data_file.write(json.dumps(asdict(data)))
    data_file.close()

    # caption handler
    caption_list = data.captions

    # caption_list format -> [caption_data1, caption_data2...]
    # caption_data format -> [caption, confidence]

    for caption_data in caption_list:

        # Update the dictionary
        caption = caption_data[0]
        confidence = caption_data[1]
        try:
            '''
                Try to map the caption to itself. If the caption is not in 
                the dictionary, a KeyError will be thrown. The attempt to map
                the caption to itself here is for a situation where a caption
                landed in the library as a synonym and is mapped only to other
                captions.
            '''
            dictionary[caption].add(caption)

        except KeyError:
            # add caption to dictionary and map to set containing itself
            dictionary[caption] = set(caption)
            # generate synonyms for the caption and add to dictionary
            synomyns = PyDictionary().synonym(caption)
            if synomyns is not None:
                for synonym in synomyns:
                    if synonym in dictionary:
                        # if the synonym is in the dictionary, attempt to
                        # add caption to the word's caption set
                        dictionary[synonym].add(caption)
                    else:
                        # if the synonym is not in the dictionary,
                        # map the synonym to a set containing the caption
                        dictionary[synonym] = set(caption)

        # Update official_captions file and caption pool
        if caption in official_captions_set:
            # read caption.json file line by line into a list, split each line into list by ' '
            caption_dot_json = open(caption_pool_location + caption + '.txt', 'r')
            lines = caption_dot_json.readlines()
            caption_dot_json.close()

            caption_dot_json_data = []
            for line in lines:
                l = line.split(' ')
                caption_dot_json_data.append(l)
            
            # add new data to list
            caption_dot_json_data.append([data.uuid, confidence])

            # sort using confidence
            caption_dot_json_data = [[x, str(y)] for x,y in sorted(caption_dot_json_data, key= lambda x:x[1])]

            # print back to file line by line ' '.join(caption_data) -> "image_name confidence\n"
            caption_dot_json = open(caption_pool_location + caption + '.txt', 'w')
            caption_dot_json.write('')
            caption_dot_json.close()

            caption_dot_json = open(caption_pool_location + caption + '.txt', 'a')
            for item in caption_dot_json_data:
                print(item)
                caption_dot_json.write(' '.join(item))
            # close file
            caption_dot_json.close()
            pass
        else:
            # create new caption.json file
            
            # write caption info in the form -> "image_name confidence\n"
            # close file
            pass


if __name__ == "__main__":
    image = cv.imread('../Image Repository/image.jpg')
    with open('cache/5ad38c9f-1dcf-47b8-b21b-97c171205cac.json') as file:
        data = json.load(file)
        data['captions'] = [['fire hydrant', .345234], [
            'bird', .2586234], ['giraffe', .23532424], ['dog', .2848659]]
        data = Data(data['original_name'], data['uuid'],
                    data['image'], data['image_shape'], data['captions'])
        post(data)
