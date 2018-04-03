FROM ubuntu:16.04

ENV application_path /opt/anomaly_detection
WORKDIR ${application_path}

COPY . .
RUN apt-get update -y --allow-unauthenticated && apt-get install -y python3-numpy python3-scipy python3-pip
RUN pip3 install .

ENTRYPOINT python3 -m anomalydetection.app
