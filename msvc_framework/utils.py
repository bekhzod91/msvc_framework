import importlib
import json
from django.conf import settings
from .broker.interface import SUCCESS, FAIL


def get_broker():
    engine = settings.MSVC_FRAMEWORK["ENGINE"]
    module_name, class_name = engine.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def call(path: str, data: object) -> dict:
    broker = get_broker()
    producer = broker.producer()
    response = producer.call(path, data)
    return json.loads(response)


def async_call(path: str, data: object) -> None:
    broker = get_broker()
    producer = broker.producer()
    producer.async_call(path, data)


def is_fail(response):
    return response['status'] == FAIL


def is_success(response):
    return response['status'] == SUCCESS
