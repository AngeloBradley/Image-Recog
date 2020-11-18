from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import cv2 as cv
import numpy as np
import json
import obj_detect

app = FastAPI()
repo = "./Processing Repo/"


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
    cv.imwrite(repo + data.uuid + ".jpg", image)

    # send image to data analysis models

    # object detection
    captions = []
    image = cv.imread(image)
    captions.append(obj_detect.get_object_captions(image))

    # text detection
    

    # add captions to data_dict
    data_dict["captions"] = captions
    final_data_dict_as_string = str(data_dict)

    # create local copy of data file
    data_file = open(repo + data.uuid + ".txt", "w")
    data_file.write(final_data_dict_as_string)
    data_file.close()

    # forward image data to database with captions


@app.websocket("/ws")
async def forward_to_database(data: str):
    pass


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
