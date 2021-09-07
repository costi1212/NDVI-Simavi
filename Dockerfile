FROM python:3.8.10
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY src/ .
CMD [ "python", "./NdviClassificationService.py" ]