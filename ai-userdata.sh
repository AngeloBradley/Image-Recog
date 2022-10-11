######### install pip
# yes " " -> should handle the 'press ENTER' prompt
yes " " | sudo add-apt-repository universe
yes Y | sudo apt install python3-pip

######### set-up virtual environment
python3 -m pip install --user virtualenv
python3 -m virtualenv venv
source venv/bin/activate

######### install pytorch and torchvision
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

######### install opencv-python
pip install opencv-python

######### install detectron2
yes " " | sudo apt update && sudo apt install -y cmake g++ wget unzip
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'