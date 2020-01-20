from django.db.models import PositiveIntegerField

from .utils import call, is_success
from .broker.exceptions import BrokerStatusFail


def map_data(data):
    try:
        return data[0]
    except IndexError:
        pass


class Value(object):
    def __init__(self, value, get):
        self.value = value
        self.get = get

    def __int__(self):
        return self.value


class RemoteRelatedField(PositiveIntegerField):
    def __init__(self, path=None, key='ids', map=map_data, **kwargs):
        kwargs.setdefault('db_index', True)
        self.path = path
        self.key = key
        self.map = map
        super().__init__(**kwargs)

    def call(self, value):
        params = {self.key: [value]}
        response = call(self.path, params)

        if is_success(response):
            return self.map(response['data'])

        raise BrokerStatusFail

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return Value(value, lambda: self.call(int(value)))

    def get_column_name(self):
        return '%s_id' % self.name

    def get_attname_column(self):
        attname = self.get_attname()
        column = self.get_column_name()
        return attname, column
