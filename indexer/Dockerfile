FROM nvidia/cuda:10.0-cudnn7-devel

MAINTAINER Davide Desirello <davide.desirello@rai.it>

ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH

RUN apt-get update -y --fix-missing

RUN mkdir -p $CONDA_DIR && \
    echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh && \
    apt-get install -y wget git libhdf5-dev g++ openmpi-bin && \
    apt-get install -y graphviz && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh && \
    echo "c59b3dd3cad550ac7596e0d599b91e75d88826db132e4146030ef471bb434e9a *Miniconda3-4.2.12-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash /Miniconda3-4.2.12-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.2.12-Linux-x86_64.sh

ENV NB_USER keras
ENV NB_UID 1000

RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p $CONDA_DIR && \
    chown keras $CONDA_DIR -R && \
    mkdir -p /src && \
    chown keras /src

USER keras

# Python
ARG python_version=3.5

RUN conda install -y python=${python_version} && \
    pip install --upgrade pip && \
    pip install tensorflow-gpu && \
    pip install pymongo && \
    conda install Pillow scikit-learn notebook pandas matplotlib mkl nose pyyaml six h5py && \
    conda install theano pygpu && \
    git clone git://github.com/fchollet/keras.git /src && pip install -e /src[tests] && \
    pip install git+git://github.com/fchollet/keras.git && \
    conda clean -yt

ADD theanorc /home/keras/.theanorc

ENV PYTHONPATH='/src/:$PYTHONPATH'

ENV CUDA_VISIBLE_DEVICES=0

RUN mkdir -p /home/keras/indexer &&\
    mkdir -p /home/keras/indexer/output &&\
    mkdir -p /home/keras/indexer/input &&\ 
    mkdir -p /home/keras/indexer/bin

COPY ./bin /home/keras/indexer/bin

WORKDIR /home/keras/indexer/bin

EXPOSE 8000 8000

USER root

CMD ["python", "makeIndex.py"]


