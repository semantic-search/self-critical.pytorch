FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-devel

# Dependencies for opencv and wget
RUN apt-get update && apt-get install -y \
  libsm6 \
  libxext6 \
  libxrender-dev \
  libglib2.0-0 \
  wget

# COPY . /app
WORKDIR /models

RUN pip install git+https://github.com/ruotianluo/ImageCaptioning.pytorch.git

RUN pip install gdown

RUN gdown --id 1VmUzgu0qlmCMqM1ajoOZxOXP3hiC_qlL
RUN gdown --id 1zQe00W02veVYq-hdq5WsPOS3OPkNdq79

RUN pip install yacs opencv-python pandas

WORKDIR /content/model_data
 
RUN wget https://dl.fbaipublicfiles.com/vilbert-multi-task/detectron_config.yaml -O /content/model_data/detectron_model.yaml
RUN wget https://dl.fbaipublicfiles.com/vilbert-multi-task/detectron_model.pth -O /content/model_data/detectron_model.pth

WORKDIR /content

RUN git clone https://gitlab.com/vedanuj/vqa-maskrcnn-benchmark.git
WORKDIR /content/vqa-maskrcnn-benchmark

# Compile custom layers and build mask-rcnn backbone
# Run below commands manually after this image is built by running it with gpu : 
#   docker build -t akshay090/self-critical.pytorch .
#   docker run -it --gpus all akshay090/self-critical.pytorch
#   then open new terminal and docker commit [container ID] akshay090/self-critical.pytorch
#   After this its ready to use
# RUN python setup.py build
# RUN python setup.py develop
# RUN python -c 'import sys; sys.path.append("/content/vqa-maskrcnn-benchmark")'
