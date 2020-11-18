from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import cv2 as cv
import numpy as np
import json

app = FastAPI()
cache_location = '/cache/'
offical_captions = set()
dictionary = {}


class Data(BaseModel):
    pass


@app.post("/")
async def post(data: Data):
    data_dict = data.dict()

    # add image file to cache
    image = np.asarray(data.image)
    cv.imwrite(cache_location + data.uuid + ".jpg", image)
    
    # add metadata file to cache
    data_file = open(cache_location + data.uuid + ".json", "w")
    data_file.write(json.dumps(data_dict))
    data_file.close()

    # caption handler
    caption_list = list(data.captions)


    for caption in list(data_dict.captions):
        if caption in offical_captions:
            with open(caption + '.json') as caption_file:
                caption_file

@app.websocket("/ws")
async def forward_to_database(data: str):
    pass


if __name__ == "__main__":
    uvicorn.run(app, port=8090, host="0.0.0.0")
