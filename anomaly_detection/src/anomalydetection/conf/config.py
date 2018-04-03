import os

bootstrap_server = os.environ["BOOTSTRAP_SERVER"].split(',')
broker_server = os.environ["BROKER_SERVER"].split(',')
input_topic = os.environ["INPUT_TOPIC"]
output_topic = os.environ["OUTPUT_TOPIC"]
period_in_seconds = os.environ["PERIOD_IN_SECONDS"]
