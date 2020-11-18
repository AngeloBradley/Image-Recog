from dataclasses import dataclass, asdict
from PyDictionary import PyDictionary
import cv2 as cv
import numpy as np
import json
import heapq
import sys

cache_location = 'cache/'
offical_captions = set()
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

    # sys.exit()
    # captions_data -> [caption, confidence]

    for caption_data in caption_list:
        # Update the dictionary
        caption = caption_data[0]
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
            
            for synonym in synomyns:
                if synonym in dictionary:
                    # if the synonym is in the dictionary, attempt to
                    # add caption to the word's caption set
                    dictionary[synonym].add(caption)
                else:
                    # if the synonym is not in the dictionary,
                    # map the synonym to a set containing the caption
                    dictionary[synonym] = set(caption)




if __name__ == "__main__":
    image = cv.imread('../Image Repository/image.jpg')
    with open('cache/5ad38c9f-1dcf-47b8-b21b-97c171205cac.json') as file:
        data = json.load(file)
        data['captions'] = [['cat', .345234],['dog', .2586234]]
        data = Data(data['original_name'], data['uuid'], data['image'], data['image_shape'], data['captions'])
        post(data)



    
    # cv.imshow('image', image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()