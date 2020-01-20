#/bin/bash

# unfortunately, this directory only exists when running the web-based terminal
# so, we will create a directory with the codeocean Dockerfile
DIRECTORY=/codeocean-true

ls
ls /

if [ -d "$DIRECTORY" ]; then
    echo "Assuming CodeOcean execution environment, do not clone NNV, already set up at /code"
else
    echo "Install NNV"
    git clone https://github.com/verivital/nnv.git
    matlab -nodisplay -nodesktop -r "run nnv/code/nnv/install.m; quit"
fi


echo "Install ReluVal"
git clone https://github.com/tcwangshiqi-columbia/ReluVal
mkdir -p ReluVal/OpenBLAS
apt-get install libopenblas-base
wget https://github.com/xianyi/OpenBLAS/archive/v0.3.6.tar.gz
tar -xzf v0.3.6.tar.gz
cd OpenBLAS-0.3.6
make
make PREFIX=$(pwd) install
cd ..
mv $(pwd)/OpenBLAS-0.3.6/* $(pwd)/ReluVal/OpenBLAS
rm -r OpenBLAS-0.3.6
rm -r v0.3.6.tar.gz 

cd ReluVal
make
cd ..

echo "Install Reluplex"
git clone https://github.com/guykatzz/ReluplexCav2017.git
cd ReluplexCav2017
cd glpk-4.60
chmod +x configure_glpk.sh
./configure_glpk.sh
make
make install
cd ..

cd reluplex
make
cd ..

cd check_properties
make
cd ..
cd ..

echo "Install Marabou"
apt install cmake
git clone https://github.com/NeuralNetworkVerification/Marabou.git
cd Marabou
mkdir build
cd build 
cmake ..
cmake --build .
cd ..
cd ..
