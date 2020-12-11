Setup

Once installations have completed:

cd into each folder (ai, database, new_file_detection) and run: $ python main.py
cd into the gui folder and run: $ npm start

-- this will start each application and if there are new images in the image 
repository, image processing will begin immediately and automatically.

-- Note: in new_file_detection's main.py, there is a process limit of 100 images
at a time due to space constraints in the development environment

-- Note: if the database dictionary does not exist at run-time, there will be a
noticeable delay in the database server starting. This is caused by the 
automatic creation (or re-creation) and population of the dictinoary.json file.
All subsequent runs will be faster than the ai server boot time.

-- Note: the complete list of coco categories that detectron2 is using can be
found here -> https://github.com/facebookresearch/detectron2/blob/60d7a1fd33cc48e58968659cd3301f3300b2786b/detectron2/data/datasets/builtin_meta.py


