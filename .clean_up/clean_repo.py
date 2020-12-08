import os

def clean_image_repository():
    image_repo = '../Image Repository/'
    IMAGE_TYPES = ('.jpg', '.jpeg', '.tiff', '.png')

    for root, dirs, files in os.walk(image_repo):
        for file in files:
            if file[file.rfind('.'):] not in IMAGE_TYPES:
                os.remove(image_repo + file)