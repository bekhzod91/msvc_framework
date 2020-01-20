import json
import uuid
import logging
from django.conf import settings
from kafka import KafkaProducer
from kafka import KafkaConsumer
from .interface import BrokerProducer
from .interface import BrokerConsumer
from ..tasks import tasks_methods

logger = logging.getLogger('kafka')
config = settings.MSVC_FRAMEWORK

kafka_host = config.get('HOST', 'localhost')
kafka_topic = config.get('TOPIC', 'default_topic')
producer_kwargs = config.get('PRODUCER_KWARGS', {})
consumer_kwargs = config.get('CONSUMER_KWARGS', {})


def get_consumer(topic, **kwargs):
    kwargs = {**consumer_kwargs, **kwargs}
    return KafkaConsumer(topic, bootstrap_servers=kafka_host, **kwargs)


def get_producer(**kwargs):
    kwargs = {**producer_kwargs, **kwargs}
    return KafkaProducer(bootstrap_servers=kafka_host, **kwargs)


class KafkaBrokerProducer(BrokerProducer):
    """
    from apps.msvc.broker.kafka import KafkaBrokerProducer
    k = KafkaBrokerProducer()
    k.call('user.user.get', {'data': 'hello'})
    """
    def instance(self):
        return get_producer()

    def response(self, topic):
        consumer = get_consumer(topic, auto_offset_reset='earliest')
        results = next(consumer)
        consumer.close()

        return results.value

    def send(self, data):
        send_data = json.dumps(data).encode('utf-8')
        self.producer.send(kafka_topic, send_data)

    def call(self, path: str, data: dict):
        reply_to = str(uuid.uuid4())

        self.send({
            'path': path,
            'reply_to': reply_to,
            'body': json.dumps(data)
        })

        return self.response(reply_to)

    def async_call(self, path: str, data: dict):
        self.send({
            'path': path,
            'reply_to': None,
            'body': json.dumps(data)
        })


class KafkaBrokerConsumer(BrokerConsumer):
    """
    from apps.msvc.broker.kafka import KafkaBrokerConsumer
    k = KafkaBrokerConsumer()
    k.subscribe()
    """
    def instance(self):
        return get_consumer(kafka_topic)

    def reply(self, topic, data):
        producer = get_producer()
        send_data = json.dumps(data).encode('utf-8')
        future = producer.send(topic, send_data)
        future.get()

    def subscribe(self):
        for msg in self.consumer:
            protocol = json.loads(msg.value)
            body = json.loads(protocol['body'])
            method = tasks_methods.get(protocol['path'])

            if method:
                func = method['func']
                results = func(body)

                if protocol['reply_to']:
                    self.reply(protocol['reply_to'], results)
            else:
                message = 'Method %s not found' % protocol['path']
                logger.log(logging.WARNING, message)


class KafkaBroker(object):
    @staticmethod
    def consumer():
        return KafkaBrokerConsumer()

    @staticmethod
    def producer():
        return KafkaBrokerProducer()
