# -*- coding:utf-8 -*- #
#
# Anomaly Detection Framework
# Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from anomalydetection.backend.sink.websocket import \
    WebSocketSink
from anomalydetection.common.concurrency import Concurrency
from anomalydetection.common.config import Config
from anomalydetection.backend.entities.json_input_message_handler import \
    InputJsonMessageHandler
from anomalydetection.backend.interactor.stream_engine import \
    StreamEngineInteractor


def main(config: Config):

    # Creates stream based on config env vars and a RobustDetector
    def run_live_anomaly_detection(stream, engine_builder,
                                   sinks, warmup, name):

        # Send to broker or similar
        extra_middleware = [
            WebSocketSink(name, config.get_websocket_url())
        ]

        # Instantiate interactor and run
        interactor = StreamEngineInteractor(
            stream,
            engine_builder,
            InputJsonMessageHandler(),
            sinks=sinks + extra_middleware,
            warm_up=warmup[0])
        interactor.run()

    for name, item in config.get_as_dict().items():
        item_list = list(item)
        item_list.append(name)
        Concurrency.run_thread(target=run_live_anomaly_detection,
                               args=tuple(item_list),
                               name="Detector {}".format(name))


if __name__ == "__main__":
    main(Config())
