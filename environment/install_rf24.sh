# http://tmrh20.github.io/RF24/Python.html
# Pre-req:
# sudo apt-get install python-dev libboost-python-dev python-setuptools -y
#
# uninstall
# sudo rm -rf /usr/local/lib/librf24*
# sudo rm -rf /usr/local/include/RF24

rf24_dir=".temp.rf24"
git clone https://github.com/nRF24/RF24.git $rf24_dir
cd $rf24_dir
if [ -d /usr/local/include/RF24 ]
then
    make
else
    # ./configure --driver=SPIDEV
    # sudo make install
    sudo make install -B
fi
cd pyRF24
../../../venv/bin/python setup.py build
../../../venv/bin/python setup.py install
cd ../..
rm -rf $rf24_dir