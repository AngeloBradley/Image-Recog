from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import requests
import cv2 as cv
import numpy as np
import obj_detect
from typing import Optional
import time
import json

app = FastAPI()
repo = "temp/"


class Data(BaseModel):
    original_name: str
    uuid: str
    image: list
    image_shape: tuple


@app.post("/")
async def post(data: Data):
    data_dict = data.dict()

    # save image to local repo
    image = np.asarray(data.image)
    image_path = repo + data.uuid + ".jpg"
    cv.imwrite(image_path, image)

    # send image to data analysis models

    # object detection
    captions = []
    image = cv.imread(image_path)
    captions.append(obj_detect.get_object_captions(image))
    print(data.uuid + ' ' + str(captions))

    # text detection
    # TODO
    # add captions to data_dict
    data_dict["captions"] = captions
    final_data_dict_as_string = json.dumps(data_dict)

    # create local copy of data file
    data_file = open(repo + data.uuid + ".txt", "w")
    data_file.write(final_data_dict_as_string)
    data_file.close()

    # forward image data to database with captions
    # final_data_dict_as_string = json.dumps(final_data_dict_as_string)
    send_to_database(data_dict)


def send_to_database(image_data):
    while True:
        try:
            # response = requests.post(
            #     'http://localhost:8090/', json.dumps({
            #         'original_name': 'hello world',
            #         'uuid': '123456',
            #         'image': [[1, 2, 3], [4, 5, 6]],
            #         'image_shape': (12, 15),
            #         'captions': ['dog', 'cat']
            #     }))
            response = requests.post(
                'http://0.0.0.0:8090/', json.dumps(image_data))
            print(response)
            break
        except Exception as e:
            # wait and try again
            print(str(e))
            time.sleep(5)


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
