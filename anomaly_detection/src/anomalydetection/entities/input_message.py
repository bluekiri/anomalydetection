import dateutil.parser


class InputMessage:

    def __init__(self, application: str, value: float, ts_str: str):
        """
        This is the parser format of a kafka message.

        :param application: Sender application
        :param value: Value
        :param ts_str: current time stamp 2018-03-16T07:10:15+00:00 in ISO 8601
        """
        self.ts = dateutil.parser.parse(ts_str)
        self.value = value
        self.application = application
