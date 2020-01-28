FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip && \
    apt-get clean

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        gcc \
        libboost-all-dev \
        libopenblas-base \
        make \
        pkg-config \
        python3 \
        python3-dev \
        wget \
        python-pip \
        python3-pip \
        software-properties-common \
        git

RUN pkg-config --cflags python

RUN pip3 install numpy

RUN pip3 install pybind11

RUN git clone https://github.com/verivital/run_nnv_comparison

# cmake cmake-data libarchive13 libcurl4 libjsoncpp1 liblzo2-2 librhash0 libuv1

RUN ls

WORKDIR run_nnv_comparison

RUN chmod +x setup_tools.sh
RUN ./setup_tools.sh

#RUN chmod +x run_tools.sh
#RUN ./run_tools.sh

RUN apt-get install nano

RUN ls
RUN ls
RUN ls
RUN ls
RUN ls
RUN ls
RUN git pull
