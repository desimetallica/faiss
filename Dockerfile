FROM nvidia/cuda:10.0-cudnn7-devel

MAINTAINER Davide Desirello <davide.desirello@rai.it>

#Install Keras

WORKDIR /

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

RUN mkdir -p $CONDA_DIR && \
    mkdir -p /src

# Python
ARG python_version=2.7

RUN conda install -y python=${python_version} && \
    pip install --upgrade pip && \
    pip install tensorflow-gpu && \
    conda install Pillow scikit-learn notebook pandas matplotlib mkl nose pyyaml six h5py && \
    conda install theano pygpu && \
    git clone git://github.com/fchollet/keras.git /src && pip install -e /src[tests] && \
    pip install git+git://github.com/fchollet/keras.git && \
    conda clean -yt

RUN wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
RUN apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
RUN wget https://apt.repos.intel.com/setup/intelproducts.list -O /etc/apt/sources.list.d/intelproducts.list
RUN sh -c 'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list'
RUN apt-get update
RUN apt-get install -y intel-mkl-2019.3-062
ENV LD_LIBRARY_PATH /opt/intel/mkl/lib/intel64:$LD_LIBRARY_PATH
ENV LIBRARY_PATH /opt/intel/mkl/lib/intel64:$LIBRARY_PATH
ENV LD_PRELOAD /usr/lib/x86_64-linux-gnu/libgomp.so.1:/opt/intel/mkl/lib/intel64/libmkl_def.so:\
/opt/intel/mkl/lib/intel64/libmkl_avx2.so:/opt/intel/mkl/lib/intel64/libmkl_core.so:\
/opt/intel/mkl/lib/intel64/libmkl_intel_lp64.so:/opt/intel/mkl/lib/intel64/libmkl_gnu_thread.so

# Install necessary build tools
RUN apt-get install -y libopenblas-dev python-numpy python-dev swig git python-pip wget make swig build-essential g++ gcc


# Install necesary headers/libs
RUN apt-get install -y curl

COPY . /opt/faiss

WORKDIR /opt/faiss

# --with-cuda=/usr/local/cuda-8.0 
RUN ./configure --prefix=/usr --libdir=/usr/lib64 --with-cuda=/usr/local/cuda-10.0 --with-cuda-arch="-gencode=arch=compute_61,code=sm_61"
RUN make -j $(nproc)
RUN make -C python
RUN make test
RUN make install
#RUN make gpu/test/demo_ivfpq_indexing_gpu
#RUN make -C demos demo_ivfpq_indexing && ./demos/demo_ivfpq_indexing

EXPOSE 8000 8000

#ADD theanorc /home/keras/.theanorc

ENV PYTHONPATH='/src/:$PYTHONPATH'

ENV CUDA_VISIBLE_DEVICES=1

ENV PYTHONPATH='/usr/local/lib/python2.7/dist-packages/:$PYTHONPATH'

WORKDIR /opt/faiss/webapp

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]

# RUN ./tests/test_blas && \
#     tests/demo_ivfpq_indexing


# RUN wget ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz && \
#     tar xf sift.tar.gz && \
#     mv sift sift1M

# RUN tests/demo_sift1M
