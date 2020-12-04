from fastapi import FastAPI, WebSocket
import uvicorn
from pydantic import BaseModel
from os import error

import cv2 as cv
import base64
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware
from image_data_processing import data_processor

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


caption_pool_location = 'cache/caption_pool/'
cache_location = 'cache/'

class Data(BaseModel):
    original_name: str
    uuid: str
    image: list
    image_shape: tuple
    captions: list

class Query(BaseModel):
    query: str






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

@app.post("/search")
async def get(query: Query):
    query = query.dict()
    query = query["query"]
    return search(query)

@app.post("/")
async def post(data: Data):
    data_processor(data)


def search(query):
    '''
        this code assumes that the query has gone through some sort of security check and 
        that the query is made up only of words separated by spaces. Will add validation 
        features if necessary.
    '''
    # -------------------------------------------------------------------------------------
    '''
        an "and" or "&" function could be implemented. It could work something like this:
        
        left_term and right_term

        -- grab the lists from both caption.txt files (left_term.txt and right_term.txt)
        -- iterate over one list, image by image, storing the image in some variable like
        and_list if the image is also present in the other list. The tricky part would be 
        sorting the list. By default, the method above would give confidence level
        preference to the left term. What this means is:

        the query "dog and fire hydrant" would result in a list where the images are more
        likely to actually contain a dog. The possibility of any image actually containing a 
        fire hydrant would be hit or miss.

        you could sort by both but that probably wouldn't improve the results much because the 
        confidence levels vary so wildly.
    '''
    # -------------------------------------------------------------------------------------

    search_terms = query.split(' ')
    search_results = []
    seen = set()

    for term in search_terms:
        # attempt to pass term to dictionary
        # if the dictionary throws a keyerror, return nothing
        # if the dictionary returns a value, store as valid_term

        try:
            valid_terms = dictionary[term]
            # print(valid_terms)

            for v_term in valid_terms:

                with open(caption_pool_location + v_term + '.txt') as caption_dot_text:
                    images = caption_dot_text.readlines()
                    # image format -> "uuid.txt confidence"
                    for image in images:
                        # split image data into uuid and confidence
                        i = image.split(' ')
                        if i[0] in seen:
                            pass
                        else:
                            seen.add(i[0])
                            search_results.append(i[0])

        except KeyError:
            # search term was not in dictionary, continue with the for loop
            continue
    # print(search_results)
    return gather_images_for_gui(search_results)


def load_dictionary_from_disk():
    global dictionary

    with open(dictionary_file, 'r') as df:
        dictionary = json.load(df)


def gather_images_for_gui(search_results):
    image_data_b64 = []
    # iterate over search_results and load images
    for result in search_results:
        # print(result)
        with open(cache_location + result) as r:
            image_data_b64.append(r.read())

    # print(image_data_b64)
    return image_data_b64

    


if __name__ == "__main__":
    # load_dictionary_from_disk()
    uvicorn.run(app, port=8090, host="0.0.0.0")
