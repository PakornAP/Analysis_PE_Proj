FROM python:3.9.5
# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
#FROM nvcr.io/nvidia/pytorch:21.05-py3
#install linux pack
#RUN apt update && apt install -y zip htop screen libgl1-mesa-glx
#install dependencies
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --no-cache torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
WORKDIR /Analysis_PE
COPY . .
CMD ["python", "app.py"]