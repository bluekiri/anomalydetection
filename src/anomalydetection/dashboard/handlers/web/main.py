# -*- coding: utf-8 -*-
import datetime

from bokeh.embed import components
from bokeh.plotting import figure
import pandas as pd
from tornado.web import RequestHandler
from tornado import web

from anomalydetection.backend.engine.engine_factory import EngineFactory
from anomalydetection.backend.entities.output_message import OutputMessageHandler
from anomalydetection.backend.interactor.batch_engine import BatchEngineInteractor
from anomalydetection.backend.repository.sqlite import ObservableSQLite
from anomalydetection.backend.repository.sqlite import SQLiteRepository
from anomalydetection.dashboard.handlers.base.html \
    import BaseHTMLHandler
from anomalydetection.dashboard.handlers.base.html \
    import SecureHTMLHandler


class Chart(RequestHandler):

    async def create_figure(self, data):

        to_ts = datetime.datetime.strptime(data["to-date"] + " 23:59:59",
                                           "%d-%m-%Y %H:%M:%S")
        from_ts = datetime.datetime.strptime(data["from-date"] + " 00:00:00",
                                             "%d-%m-%Y %H:%M:%S")
        file_db = self.application.settings['conf']['DATA_DB_FILE']
        observable = ObservableSQLite(SQLiteRepository(file_db),
                                      from_ts, to_ts)

        ticks = BatchEngineInteractor(observable,
                                      EngineFactory(**data).get(),
                                      OutputMessageHandler()).process()

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


class Home(SecureHTMLHandler, Chart):
    template = "home.html"

    @web.asynchronous
    async def get(self):

        engines = EngineFactory.engines
        to_date = datetime.datetime.now()
        default_engine = next(iter(engines.items()))
        data = {
            "engine": default_engine[1]['key'],
            "window": "30",
            "threshold": "0.99",
            "to-date": to_date.strftime("%d-%m-%Y"),
            "from-date": (to_date - datetime.timedelta(days=7)).strftime("%d-%m-%Y")
        }

        input_data = {k: v[0].decode("utf-8")
                      for k, v in self.request.arguments.items()}
        data.update(input_data)

        plot = await self.create_figure(data)
        script, div = components(plot)

        self.response(script=script, div=div, engines=engines,
                      form_data=data, engine=engines[data['engine']]['name'])


class Maintenance(BaseHTMLHandler):
    template = "maintenance.html"

    async def get(self):
        self.response(h_title="Maintenance")


class MaintenanceSwitch(SecureHTMLHandler):
    template = "maintenance.html"

    async def get(self):
        raise NotImplemented

    async def switch_maintenance(self, status):
        return status


class MaintenanceEnable(MaintenanceSwitch):

    async def get(self):
        res = await self.switch_maintenance(True)
        if res:
            self.response(h_title="Maintenance enabled")


class MaintenanceDisable(MaintenanceSwitch):

    async def get(self):
        res = await self.switch_maintenance(False)
        if res:
            self.response(h_title="Maintenance enabled")
