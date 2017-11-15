rf24_dir=".temp.rf24"
git clone https://github.com/nRF24/RF24.git $rf24_dir
cd $rf24_dir/pyRF24
../../venv/bin/python setup.py install
cd ../..
rm -rf $rf24_dir