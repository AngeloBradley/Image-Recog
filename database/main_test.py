from dataclasses import dataclass, asdict
import cv2 as cv
import numpy as np
import json


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
    
    for caption in caption_list:
        try:
            with open(caption + '.txt') as caption_file:
                caption_file_data = json.load(caption_file)
                caption_file_data[data.uuid]


    # for caption in list(data_dict.captions):
    #     if caption in offical_captions:
    #         with open(caption + '.json') as caption_file:
    #             caption_file




if __name__ == "__main__":
    image = cv.imread('../Image Repository/image.jpg')
    with open('5ad38c9f-1dcf-47b8-b21b-97c171205cac.txt') as file:
        data = json.load(file)
        data['captions'] = ['cat','dog']
        data = Data(data['original_name'], data['uuid'], data['image'], data['image_shape'], data['captions'])
        post(data)



    
    # cv.imshow('image', image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()