# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

from labels import COCO_CATEGORIES

image_location = "../../Image Repository/"
IMAGE_TYPES = ('.jpg', '.jpeg')
images = []

# setup detectron model
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)

def get_object_captions(image):
    # inject image into detectron model
    outputs = predictor(image)

    # obtain captions and confidence levels
    caption_data = []

    for i in range(len(outputs["instances"].pred_classes)):
        data = []
        data.append(COCO_CATEGORIES[outputs["instances"].pred_classes[i].item()]["name"]) # grab label
        data.append(outputs["instances"].scores[i].item()) # grab confidence level

        caption_data.append(data)

    return caption_data

    # v = Visualizer(image[:,:,::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    # out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    # cv2.imshow('processed image', out.get_image()[:,:,::-1])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    image = cv2.imread(image_location + 'image.jpg')
    captions = get_object_captions(image)
    print(captions)