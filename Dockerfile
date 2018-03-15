FROM ubuntu:16.04
ARG DATABASE_NAME

ENV application_path /opt/anomaly_detection
WORKDIR ${application_path}

RUN apt-get update -y --allow-unauthenticated && apt-get install -y python3-pip

COPY . .

RUN pip3 install .
ENTRYPOINT python -m poc-anomaly-detection
