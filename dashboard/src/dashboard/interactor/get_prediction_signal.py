from dashboard.repository.predictions_signal_repository import PredictionSignalRepository


class GetPredictionSignal:
    def __init__(self, prediction_signal_repository: PredictionSignalRepository):
        self.prediction_signal_repository = prediction_signal_repository

    def get_application_signal(self, application: str):
        results = self.prediction_signal_repository.get_application_signal(application)
        return [{"value": item[3], "upper_limit": item[5], "lower_limit": item[6], "is_anomaly": item[8]} for item
                in results]
