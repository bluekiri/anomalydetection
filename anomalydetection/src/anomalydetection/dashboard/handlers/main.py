# -*- coding: utf-8 -*-
import datetime

from bokeh.embed import components
from bokeh.plotting import figure
import pandas as pd
from tornado.web import RequestHandler

from anomalydetection.backend.engine.engine_factory import EngineFactory
from anomalydetection.backend.entities.output_message import OutputMessageHandler
from anomalydetection.backend.interactor.batch_engine import BatchEngineInteractor
from anomalydetection.backend.repository.sqlite import ObservableSQLite, SQLiteRepository
from anomalydetection.dashboard.conf import DATA_DB_FILE
from anomalydetection.dashboard.lib.handlers.html.base_html import BaseHTMLHandler
from anomalydetection.dashboard.lib.handlers.html.secure_html import SecureHTMLHandler


class Chart(RequestHandler):

    async def create_figure(self):

        data = {k: v[0].decode("utf-8") for k, v in self.request.arguments.items()}

        days = int(data["days"]) if "days" in data else 7
        to_ts = datetime.datetime.now()
        from_ts = to_ts - datetime.timedelta(days=days)
        observable = ObservableSQLite(SQLiteRepository(DATA_DB_FILE),
                                      from_ts, to_ts)

        ticks = observable.get_observable().to_blocking()
        if "engine" in data:
            ticks = BatchEngineInteractor(observable,
                                          EngineFactory(**data).get(),
                                          OutputMessageHandler()).process()

        predictions = [x.to_plain_dict() for x in ticks]
        df = pd.DataFrame(predictions)
        df["ts"] = pd.to_datetime(df["ts"])

        anomaly = df.loc[df.loc[:,"is_anomaly"] == True]

        p = figure(x_axis_type="datetime",
                   plot_height=200,
                   plot_width=450,
                   sizing_mode='scale_width',
                   toolbar_location="left")

        p.line(df["ts"], df["value_lower_limit"], legend="Lower bound",
               line_width=1, color='red', alpha=0.5)
        p.line(df["ts"], df["value_upper_limit"], legend="Upper bound",
               line_width=1, color='blue', alpha=0.5)
        p.line(df["ts"], df["agg_value"], legend=df.ix[0]["application"],
               line_width=2, color='green')
        p.circle(anomaly["ts"], anomaly["agg_value"], fill_color="red", size=8)

        return p


class Home(SecureHTMLHandler, Chart):

    template = "home.html"

    async def get(self):
        plot = await self.create_figure()
        script, div = components(plot)
        self.response(script=script, div=div)


class Documentation(SecureHTMLHandler):

    template = "docs.html"

    async def get(self):
        self.response()


class CategoriesSettings(SecureHTMLHandler):

    template = "categories_settings.html"

    async def get(self):
        self.response()


class HotelFile(SecureHTMLHandler):

    template = "hotel_file.html"

    async def get(self):
        hotel = self.get_argument("hotel", "")
        aws_s3_url = self.application.settings['conf']['aws']['s3']['url']
        self.response(hotel=hotel, aws_s3_url=aws_s3_url)


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
