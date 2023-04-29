FROM anibali/pytorch:2.0.0-cuda11.8-ubuntu22.04

ENV TZ=UTC
RUN sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

RUN sudo apt-get update \
 && sudo apt-get install -y curl libgl1-mesa-glx libgtk2.0-0 libsm6 libxext6 \
 && sudo rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false

COPY . /code/

RUN poetry install --only main

CMD ["python","image_segmentation/main.py"]
