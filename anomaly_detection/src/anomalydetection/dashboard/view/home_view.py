from bokeh.embed import components
from flask import render_template
from flask_admin import expose, BaseView
from bokeh.plotting import figure

from anomalydetection.dashboard.interactor.get_prediction_signal import GetPredictionSignal


class HomeView(BaseView):
    def __init__(self, model, session, login_auth, endpoint, get_prediction_signal: GetPredictionSignal):
        super().__init__(model, session, endpoint=endpoint)
        self.get_prediction_signal = get_prediction_signal
        self.login_auth = login_auth

    def is_accessible(self):
        return self.login_auth.is_authenticated()

    def create_figure(self):
        predictions = self.get_prediction_signal.get_application_signal("")

        x = range(len(predictions))
        y = [prediction.get("value") for prediction in predictions]
        anomalies_x = [i for i in range(len(predictions)) if predictions[i].get("is_anomaly") == 1]
        anomalies_y = [predictions[i].get("value") for i in range(len(predictions)) if
                       predictions[i].get("is_anomaly") == 1]
        p = figure(title="Anomaly", x_axis_label='x', y_axis_label='y')
        p.line(x, y, legend="Temp.", line_width=2)
        p.circle(anomalies_x, anomalies_y, fill_color="red", size=8)
        # Set the y axis label
        return p

    @expose('/')
    def index(self):
        plot = self.create_figure()
        script, div = components(plot)
        return render_template("home.html", script=script, div=div)
