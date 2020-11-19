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
official_captions_set = set(['dog', 'fire hydrant', 'bird', 'giraffe'])
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

def add_synonyms_to_dictionary(caption, orignal_caption=None):
    if type(caption) == type([]):
        for caption_term in caption:
            synomyns = PyDictionary().synonym(caption_term)
            if synomyns is not None:
                for synonym in synomyns:
                    if synonym in dictionary:
                        # if the synonym is in the dictionary, attempt to
                        # add caption to the word's caption set
                        dictionary[synonym].add(orignal_caption)
                    else:
                        # if the synonym is not in the dictionary,
                        # map the synonym to a set containing the caption
                        dictionary[synonym] = set(orignal_caption)
    else:
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
            # check caption for spaces or hyphens
            # code expects there to be only dashes OR spaces, not both
            caption_char_set = set(caption)
            if ('-' in caption_char_set) or (' ' in caption_char_set):
                caption_terms = None

                if ('-') in caption_char_set:
                    caption_terms = caption.split('-')
                else:
                    caption_terms = caption.split(' ')

                add_synonyms_to_dictionary(caption_terms, original_caption=caption)
            else:
                add_synonyms_to_dictionary(caption)

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
            caption_dot_text_data.append([data.uuid, confidence])

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
            caption_dot_text.write(data.uuid + ' ' + str(confidence))
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

    for term in search_terms:
        # attempt to pass term to dictionary
        # if the dictionary throws a keyerror, return nothing
        # if the dictionary returns a value, store as valid_term

        try:
            valid_term = dictionary[term]

            with open(caption_pool_location + valid_term + '.txt') as caption_dot_text:
                images = caption_dot_text.readlines()

                # image format -> "uuid confidence"
                for image in images:
                    # split image data into uuid and confidence
                    i = image.split(' ')
                    # only store uuid
                    search_results.append(i[0])
            print(search_results)
        except:
            continue


if __name__ == "__main__":
    # image = cv.imread('../Image Repository/image.jpg')
    # with open('cache/5ad38c9f-1dcf-47b8-b21b-97c171205cac.json') as file:
    #     data = json.load(file)
    #     data['captions'] = [['fire hydrant', .645645745], [
    #         'bird', .45734953], ['giraffe', .23425325], ['dog', .45757456]]
    #     data = Data(data['original_name'], data['uuid'],
    #                 data['image'], data['image_shape'], data['captions'])
    #     post(data)

    search("dog ")