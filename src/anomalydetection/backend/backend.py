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

from anomalydetection.backend.core.config import Config
from anomalydetection.backend.interactor.stream_engine import StreamEngineInteractor
from anomalydetection.backend.sink.websocket import WebSocketSink
from anomalydetection.common.concurrency import Concurrency


def main(config: Config):

    # Creates stream based on config env vars and a RobustDetector
    def run_live_anomaly_detection(stream, handler, engine_builder,
                                   sinks, warmup, name):

        # Add dashboard websocket as extra sink
        extra_sink = []
        try:
            websocket = WebSocketSink(name, config.get_websocket_url())
            extra_sink.append(websocket)
        except Exception as _:
            pass

        # Instantiate interactor and run
        interactor = StreamEngineInteractor(
            stream,
            engine_builder,
            handler,
            sinks=sinks + extra_sink,
            warm_up=warmup[0] if warmup else None)
        interactor.run()

    pids = []
    for name, item in config.get_as_dict().items():
        item_list = list(item)
        item_list.append(name)
        pid = Concurrency.run_process(target=run_live_anomaly_detection,
                                      args=tuple(item_list),
                                      name="Detector {}".format(name))
        pids.append(pid)

    for pid in pids:
        Concurrency.get_process(pid).join()


if __name__ == "__main__":
    main(Config())
