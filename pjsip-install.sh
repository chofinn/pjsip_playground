#!/bin/bash
yes | sudo apt install git g++ vim make build-essential python3-dev libasound2-dev
git clone https://github.com/pjsip/pjproject.git
cd pjproject
export CFLAGS="$CFLAGS -fPIC"
./configure --enable-shared
make dep
make
sudo make install
sudo apt install python3-dev
cd pjsip-apps/src/
git clone https://github.com/mgwilliams/python3-pjsip.git
cd python3-pjsip
python3 setup.py build
sudo python3 setup.py install
sudo ldconfig /usr/local/lib
