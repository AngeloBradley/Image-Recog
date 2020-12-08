from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from os import error

from gen_cache_contents import init_database
from image_data_processing import data_processor
from search import search

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/cache", StaticFiles(directory="cache"), name="cache")


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


@app.post("/search")
async def get(query: Query):
    return search(query)

@app.post("/")
async def post(data: Data):
    data_processor(data)
    


if __name__ == "__main__":
    init_database()
    uvicorn.run(app, port=8090, host="0.0.0.0")
