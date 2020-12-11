Installation Instructions 
(linux only -- Pop OS preferred -- Detectron2 not supported on Windows)
(VM recommended but not required, GPU is required)


1. install Python if not already installed
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.8

--> to protect the rest of your system, we recommend setting up a 
virtual environment and activating it before continuing
https://virtualenvwrapper.readthedocs.io/en/latest/

virtualenvwrapper cheat sheet:
Creating a virtual environment

to create and activate your env immediately use:
mkvirtualenv name_of_your_env

to deactivate env use:
deactivate

to list all available virtual envs use:
workon 
OR
lsvirtualenv

to activate one specific env:
workon name_of_your_env

to remove specific env:
rmvirtualenv name_of_your_env

create copy of env and activate new copy:
cpvirtualenv old_env new_env

!!!BE SURE TO ACTIVATE YOUR VIRTUAL ENVIRONMENT BEFORE CONTINUING!!!

2. install detectron
$ pip3 install -U torch
$ pip3 install -U torchvision
$ pip3 install git+https://github.com/facebookresearch/fvcore.git
$ python3 -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

cuda install for pop os
https://support.system76.com/articles/cuda/

3. install tesseract-ocr and pytesseract
$ sudo apt-get install tesseract-ocr
$ pip3 install pytesseract

4. install global_requirements.txt from project root folder
$ pip3 install -r global_requirements.txt

5. install react and axios
$ npm install react
$ npm install axios


