import os
from clean_repo import clean_image_repository

AI_TEMP = 'ai/temp/'

CAPTION_POOL = 'database/cache/caption_pool/'

DATABASE_CACHE = 'database/cache/'
DATABASE_CACHE_SAFE = ('dictionary.json', 'official_captions.txt')

NFD_CACHE = 'new_file_detection/cache/'

IMAGE_REPOSITORY = '../Image Repository/'

# clear ai's temp folder
for root, dirs, files in os.walk(AI_TEMP):
    for file in files:
        os.remove(AI_TEMP + file)

# clear database cache files (image and metadata files)
for root, dirs, files in os.walk(DATABASE_CACHE):
    for file in files:
        try:
            if file not in DATABASE_CACHE_SAFE:
                os.remove(DATABASE_CACHE + file)
        except:
            pass
        # let the next loop clear the caption pool

# clear caption.txt files
for root, dirs, files in os.walk(CAPTION_POOL):
    for file in files:
        os.remove(CAPTION_POOL + file)

# move files in new_file_detection back to image repository
for root, dirs, files in os.walk(NFD_CACHE):
    for file in files:
        os.rename(NFD_CACHE + file, IMAGE_REPOSITORY + file)

# remove json metadata files from image repository
clean_image_repository()

# # purge dictionary.json file
# with open(DATABASE_CACHE + 'dictionary.json', 'r+') as d:
#     d.truncate()

# # purge official_captions file
# with open(DATABASE_CACHE + 'official_captions.txt', 'r+') as d:
#     d.truncate()
