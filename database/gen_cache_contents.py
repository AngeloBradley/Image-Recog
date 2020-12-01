from labels import COCO_CATEGORIES
import json
from PyDictionary import PyDictionary
import sys

captions = []
dictionary = dict()

dictionary_file = 'cache/dictionary.json'
official_captions_file = 'cache/official_captions.txt'
official_captions_set = set()
cache_location = 'cache/'
caption_pool_location = 'cache/caption_pool/'

def load_coco_captions():
    global captions
    captions = [x["name"] for x in COCO_CATEGORIES]

####################################### Check/Build Dictionary #######################################

def verify_dictionary_json():
    global dictionary
    global captions
    global dictionary_file

    try:
        # open dictionary file
        with open(dictionary_file, 'r') as d:
            dictionary_contents = d.read()

            if len(dictionary_contents) != 0:
                dictionary = json.loads(dictionary_contents)
            else:
                # dictionary file exists but is empty
                return False

        # verify that all known captions are in dictionary
        for caption in captions:
            try:
                dictionary[caption]
            except KeyError:
                # first missing caption triggers dictionary re-creation
                return False

        # dictionary.json exists and contains all known captions
        # assumption is made that synonyms have also been added
        return True
    except IOError:
        # if dictionary.json does not exist, trigger creation
        return False



def add_synonyms(caption):
    global dictionary

    caption_split = caption.split(' ')

    for c_s in caption_split:
        synomyns = PyDictionary.synonym(c_s)
        if synomyns != None:
            synomyns = [x.lower() for x in synomyns]
            for synonym in synomyns:
                if synonym in dictionary:
                    # if the synonym is in the dictionary, attempt to
                    # add caption to the word's caption set
                    # set synonym to lowercase so search is not case sensitive
                    if caption not in set(dictionary[synonym]):
                        # print(dictionary[synonym])
                        dictionary[synonym].append(caption)
                else:
                    # if the synonym is not in the dictionary,
                    # map the synonym to a set containing the caption
                    # set synonym to lowercase so search is not case sensitive
                    dictionary[synonym] = [caption]


def populate_dictionary_in_memory():
    global captions
    global dictionary
    global dictionary_file

    for caption in captions:
        ''' 
        check to see if a coco caption has already been added 
        to the dictionary as a synonym for a caption that was
        processed earlier
        '''
        if caption in dictionary:
            '''
            if so, append caption to the list of captions
            that, that word is mapped to IF it is not already
            on the list
            '''
            if caption not in set(dictionary[caption]):
                dictionary[caption].append(caption)
        else:
            dictionary[caption] = [caption]
            add_synonyms(caption)

def write_dictionary_to_disk():
    with open(dictionary_file, 'r+') as d:
        d.truncate()

    with open(dictionary_file, 'w') as d:
        d.write(json.dumps(dictionary))

def create_dictionary():
    populate_dictionary_in_memory()
    write_dictionary_to_disk()

####################################### Populate Caption Pool #######################################

def check_caption_pool():
    global captions

    for caption in captions:
        try:
            caption_dot_text = open(caption_pool_location + caption + '.txt', 'r')
        except IOError:
            caption_dot_text = open(caption_pool_location + caption + '.txt', 'w')
            caption_dot_text.close()


####################################### Initialize Database #######################################
def init_database():
    load_coco_captions()
    if not verify_dictionary_json():
        create_dictionary()
    check_caption_pool()


if __name__ == "__main__":
    init_database()