import datetime

from bokeh.embed import components
from flask import render_template
from flask import request
from flask_admin import expose, BaseView
from bokeh.plotting import figure
import pandas as pd

from anomalydetection.backend.engine.engine_factory import EngineFactory
from anomalydetection.backend.engine.robust_z_engine import RobustDetector
from anomalydetection.backend.entities.output_message import OutputMessageHandler
from anomalydetection.backend.interactor.batch_engine import BatchEngineInteractor
from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository.sqlite import ObservableSQLite


class HomeView(BaseView):
    def __init__(self, model, session, endpoint, repository: BaseRepository):
        super().__init__(model, session, endpoint=endpoint)
        self.repository = repository

    def is_accessible(self):
        if request.cookies.get("auth") == "dummy_auth":
            return True
        return False

    def create_figure(self):

        data = request.args.to_dict()

        days = int(data["days"]) if "days" in data else 7
        to_ts = datetime.datetime.now()
        from_ts = to_ts - datetime.timedelta(days=days)
        observable = ObservableSQLite(self.repository,
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

        p = figure(title="Anomaly", x_axis_type="datetime", plot_width=1600, plot_height=650)
        p.line(df["ts"], df["value_lower_limit"], legend="Lower bound", line_width=1, color='red', alpha=0.5)
        p.line(df["ts"], df["value_upper_limit"], legend="Upper bound", line_width=1, color='blue', alpha=0.5)
        p.line(df["ts"], df["agg_value"], legend=df.ix[0]["application"], line_width=2, color='green')
        p.circle(anomaly["ts"], anomaly["agg_value"], fill_color="red", size=8)

        return p

    @expose('/')
    def index(self):
        plot = self.create_figure()
        script, div = components(plot)
        return render_template("home.html", script=script, div=div)
