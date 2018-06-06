# -*- coding: utf-8 -*-

import os
import sys
import yaml

from anomalydetection.backend.backend import main as backend_main
from anomalydetection.backend.backend import produce_messages
from anomalydetection.common.config import Config
from anomalydetection.dashboard.dashboard import main as dashboard_main

__root__ = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(__root__)


def get_config():
    return yaml.load(open(os.environ["HOME"] + "anomdec/anomdec.yml"))


def get_dev_config():
    return yaml.load(open(__root__ + "anomdec.yml"))


if __name__ == '__main__':

    try:
        if sys.argv[1] == "dashboard":
            dashboard_main(Config())
        elif sys.argv[1] == "backend":
            backend_main(Config())
        elif sys.argv[1] == "devel":
            os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
            os.environ["PUBSUB_PROJECT_ID"] = "testing"
            os.environ["ASYNC_TEST_TIMEOUT"] = "100"
            dashboard_main([backend_main, produce_messages], Config("devel"))

    except IndexError as _:
        dashboard_main([backend_main])
