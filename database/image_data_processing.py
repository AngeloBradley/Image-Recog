import cv2 as cv
import numpy as np
import json

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

def add_image_to_database(data):
    print('add_image_to_database running...')
    caption_list = data.captions
    caption_list = reduce_duplicate_captions(caption_list)

    # caption_list format -> [caption_data1, caption_data2...]
    # caption_data format -> [caption, confidence]

    for caption_data in caption_list:
        print('updating caption pool')
        caption = caption_data[0]
        confidence = caption_data[1]
        print(caption)

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
            print(e.with_traceback)
            caption_dot_text = open(
                caption_pool_location + caption + '.txt', 'w')
            caption_dot_text.write(data.uuid + '.txt ' + str(confidence))

        

        


def data_processor(data):
    try:
        data_dict = data.dict()
    except:
        data_dict = asdict(data)

    #read image in as image file
    image = np.asarray(data.image)
    
    # set paths
    orig_image_path = cache_location + data.uuid + ".jpg"
    thumb_image_path = cache_location + data.uuid + "_t.jpg"
    # write original image to cache
    cv.imwrite(orig_image_path, image)

    # resize to make thumbnail
    image = cv.imread(orig_image_path)

    thumb_height = thumb_width = 300
    image = cv.resize(image, (thumb_height, thumb_width), interpolation=cv.INTER_AREA)
    
    #write thumbnail to cache
    image = cv.imwrite(thumb_image_path, image)
    
    # add metadata file to cache
    url = "http://localhost:8090/"
    url_orig = url + orig_image_path
    url_thumb = url + thumb_image_path
    

    image_data = {
        "src": url_orig,
        "thumbnail": url_thumb,
        "thumbnailWidth": thumb_width,
        "thumbnailHeight": thumb_height
    }

    with open(cache_location + data.uuid + '.txt', 'w') as file:
        file.write(json.dumps(image_data))

    # caption handler
    add_image_to_database(data)


if __name__ == '__main__':
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
    # data_processor(data2)