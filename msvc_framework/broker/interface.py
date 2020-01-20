SUCCESS = 'success'
FAIL = 'fail'


class BrokerProducer:
    timout = 60
    producer = None

    def __init__(self):
        self.producer = self.instance()

    def instance(self) -> object:
        raise NotImplementedError

    def call(self, path: str, data: object) -> object:
        raise NotImplementedError


class BrokerConsumer:
    consumer = None

    def __init__(self):
        self.consumer = self.instance()

    def instance(self):
        raise NotImplementedError

    def subscribe(self):
        raise NotImplementedError
