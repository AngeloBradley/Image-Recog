######### build open-cv
# install tools needed for build
yes " " | sudo apt update && sudo apt install -y cmake g++ wget unzip

# grab opencv source
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip
unzip opencv.zip
unzip opencv_contrib.zip

# create and cd into build directory
mkdir -p build && cd build

# configure
cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.x/modules ../opencv-4.x

# build (note: this process takes a while)
cmake --build .