FROM python:3.5-alpine

ENV application_path /opt/anomaly_detection
WORKDIR ${application_path}

COPY . .

RUN pip3 install .
ENTRYPOINT python -m anomalydetection.app
