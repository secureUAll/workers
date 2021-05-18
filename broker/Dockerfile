FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

RUN curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz \
  && tar xzvf docker-17.04.0-ce.tgz \
  && mv docker/docker /usr/local/bin \
  && rm -r docker docker-17.04.0-ce.tgz

WORKDIR /var/temp

COPY . /var/temp 

CMD ["python3", "worker.py"]
