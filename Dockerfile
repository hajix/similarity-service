FROM illagrenan/faiss-python:latest

RUN apt update && \
    apt upgrade -y && \
    apt install -y libsndfile1

CMD pip3 install -U pip

WORKDIR /

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY app /app

CMD uvicorn app.app:app --host 0.0.0.0
