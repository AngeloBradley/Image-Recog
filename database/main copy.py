from fastapi import FastAPI, WebSocket
import uvicorn
from pydantic import BaseModel
from os import error

import cv2 as cv
import base64
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware

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
    data_dict = data.dict()

    # add b64 version of image file to cache
    image = np.asarray(data.image)
    _, buffer = cv.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    with open(cache_location + data.uuid + ".txt", 'w') as image_file:
        image_file.write(str(jpg_as_text))

    # cv.imwrite(cache_location + data.uuid + ".jpg", image)

    # add metadata file to cache
    data_file = open(cache_location + data.uuid + ".json", "w")
    data_file.write(json.dumps(data_dict))
    data_file.close()

    # caption handler
    caption_list = data.captions
    caption_list = reduce_duplicate_captions(caption_list)
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
            if caption not in set(dictionary[caption]):
                dictionary[caption].append(caption)

        except KeyError:
            # add caption to dictionary and map to set containing itself
            dictionary[caption] = [caption]
            # check caption for spaces or hyphens
            # code expects there to be only dashes OR spaces, not both
            caption_char_set = set(caption)
            if ('-' in caption_char_set) or (' ' in caption_char_set):
                caption_terms = None

                if ('-') in caption_char_set:
                    caption_terms = caption.split('-')
                else:
                    caption_terms = caption.split(' ')

                add_words_to_dictionary(
                    caption_terms, original_caption=caption)
            else:
                add_words_to_dictionary(caption)

        write_dictionary_to_disk()

        # Update official_captions file and caption pool
        if caption in official_captions_set:
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
                caption_pool_location + caption + '.txt', 'a')
            for item in caption_dot_text_data:
                caption_dot_text.write(' '.join(item) + '\n')
            # close file
            caption_dot_text.close()
        else:
            # update official_captions file and set
            with open(official_captions_file, 'a') as ocf:
                ocf.write(caption + '\n')

            official_captions_set.add(caption)

            # create new caption.txt file
            caption_dot_text = open(
                caption_pool_location + caption + '.txt', 'w')
            # write caption info in the form -> "image_name confidence\n"
            caption_dot_text.write(
                data.uuid + '.txt' + ' ' + str(confidence))
            # close file
            caption_dot_text.close()


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
