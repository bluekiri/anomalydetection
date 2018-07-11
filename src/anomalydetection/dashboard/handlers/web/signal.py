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

import datetime
import sys

import pandas as pd
from tornado.escape import json_encode
from bokeh.plotting import figure
from tornado.web import RequestHandler
from tornado import web

from anomalydetection.backend.stream import FileObservable
from anomalydetection.common.logging import LoggingMixin
from anomalydetection.backend.engine.builder import EngineBuilderFactory
from anomalydetection.backend.entities.handlers.json import InputJsonMessageHandler
from anomalydetection.backend.entities.output_message import OutputMessageHandler
from anomalydetection.backend.interactor.batch_engine import BatchEngineInteractor
from anomalydetection.backend.repository.observable import ObservableRepository
from anomalydetection.dashboard.handlers.base.html import SecureHTMLHandler
from anomalydetection.dashboard.handlers.base.json.secure_json import SecureJSONHandler
from anomalydetection.dashboard.helpers.engine import EngineBuilderForm


class Chart(RequestHandler):

    async def create_figure(self, data):

        to_ts = datetime.datetime.strptime(data["to-date"] + " 23:59:59",
                                           "%d-%m-%Y %H:%M:%S")
        from_ts = datetime.datetime.strptime(data["from-date"] + " 00:00:00",
                                             "%d-%m-%Y %H:%M:%S")

        conf = self.application \
            .settings["config"] \
            .get_as_dict()

        repository = conf[data["name"]][4][0].repository
        observable = ObservableRepository(repository,
                                          data["application"],
                                          from_ts, to_ts)

        min_value = observable.get_min()
        max_value = observable.get_max()
        data["min_value"] = min(min_value, data.get("min_value", sys.maxsize))
        data["max_value"] = max(max_value, data.get("max_value", -sys.maxsize))

        engine_builder = None
        if data["engine"] == "cad":
            engine_builder = EngineBuilderFactory.get_cad()
            if "min_value" in data:
                engine_builder.set_min_value(float(data["min_value"]))
            if "max_value" in data:
                engine_builder.set_max_value(float(data["max_value"]))

        if data["engine"] == "robust":
            engine_builder = EngineBuilderFactory.get_robust()
            if "window" in data:
                engine_builder.set_window(int(data["window"]))

        if data["engine"] == "ema":
            engine_builder = EngineBuilderFactory.get_robust()
            if "window" in data:
                engine_builder.set_window(int(data["window"]))

        if "threshold" in data:
            engine_builder.set_threshold(float(data["threshold"]))

        ticks = []
        reprocess = False
        if reprocess:
            ticks = BatchEngineInteractor(observable,
                                          engine_builder,
                                          OutputMessageHandler()).process()
        else:
            ticks = observable.get_observable().to_blocking()

        predictions = [x.to_plain_dict() for x in ticks]
        df = pd.DataFrame(predictions)
        df["ts"] = pd.to_datetime(df["ts"])

        anomaly = df.loc[df.loc[:, "is_anomaly"] == True]  # noqa: E712

        p = figure(x_axis_type="datetime",
                   plot_height=200,
                   plot_width=450,
                   sizing_mode='scale_width',
                   toolbar_location="left")

        p.line(df["ts"], df["value_lower_limit"], legend="Lower bound",
               line_width=1, color='red', alpha=0.5)
        p.line(df["ts"], df["value_upper_limit"], legend="Upper bound",
               line_width=1, color='blue', alpha=0.5)
        p.line(df["ts"], df["agg_value"], legend=df.iloc[0]["application"],
               line_width=2, color='green')
        p.circle(anomaly["ts"], anomaly["agg_value"], fill_color="red", size=8)

        return p


class SignalData(SecureJSONHandler):

    def get(self, signal):

        input_data = {k: v[0].decode("utf-8")
                      for k, v in self.request.arguments.items()}

        conf = self.application \
            .settings["config"] \
            .get_as_dict()

        repository = conf[signal][4][0].repository
        observable = ObservableRepository(repository,
                                          input_data["application"])
        data = [x.to_plain_dict()
                for x in observable.get_observable().to_blocking()]

        self.response(200, data)


class SignalSandbox(SecureHTMLHandler, LoggingMixin):

    template = "signal_sandbox.html"

    @web.asynchronous
    async def get(self):

        input_data = {k: v[0].decode("utf-8")
                      for k, v in self.request.arguments.items()}

        engines = EngineBuilderFactory.engines
        engine = input_data["engine"] if "engine" in input_data else "robust"
        file_input_value = input_data["file"] if "file" in input_data else ""

        engine_builder = EngineBuilderFactory.get(engine)
        for k in filter(lambda x: x.startswith("set"), input_data):
            try:
                engine_builder = engine_builder.set(k.replace("set_", ""),
                                                    input_data[k])
            except NotImplementedError as ex:
                self.logger.warning(str(ex))

        form = EngineBuilderForm(engine_builder).get_form()

        data = []
        if file_input_value:
            interactor = BatchEngineInteractor(
                FileObservable(file_input_value),
                engine_builder,
                InputJsonMessageHandler())

            data = [x.to_plain_dict()
                    for x in interactor.process()]

        file_input = {
            "label": "Input file (JSON)",
            "name": "file",
            "type": "text",
            "value": file_input_value,
            "placeholder": "Local file to play with",
            "id": "input_file"
        }

        self.response(signal_name="Sandbox", engine_key=engine,
                      engine_name=engine, engines=engines,
                      form=form, file_input=file_input,
                      data=json_encode(data))


class SignalDetail(SecureHTMLHandler):

    template = "signal.html"

    @web.asynchronous
    async def get(self, signal, data=None):

        engines = EngineBuilderFactory.engines
        to_date = datetime.datetime.now()

        conf = self.application \
            .settings["config"] \
            .get_as_dict()

        data = {
            "engine": conf[signal][2].type,
            "window": "30",
            "threshold": "0.99",
            "to-date": to_date.strftime("%d-%m-%Y"),
            "name": signal,
            "from-date": (to_date - datetime.timedelta(days=7)).strftime("%d-%m-%Y")
        }

        input_data = {k: v[0].decode("utf-8")
                      for k, v in self.request.arguments.items()}
        data.update(input_data)

        repository = conf[data["name"]][4][0].repository
        applications = repository.get_applications()
        if 'application' not in data:
            data['application'] = applications[0]

        breadcrumb = [
            ("/signals/", "Signals", ""),
            (self.request.uri, signal, "active")
        ]
        self.response(script=None, div=None, engines=engines,
                      signal_name=signal, breadcrumb=breadcrumb,
                      form_data=data, engine_key=data['engine'],
                      applications=applications,
                      signal_length=100,
                      selected_app=data['application'],
                      engine_name=engines[data['engine']]['name'])


class SignalList(SecureHTMLHandler):

    template = "signal_list.html"

    @web.asynchronous
    async def get(self):
        conf = self.application \
            .settings["config"] \
            .get_as_dict()

        breadcrumb = [("/signals/", "Signals", "")]
        self.response(conf=conf, breadcrumb=breadcrumb)
