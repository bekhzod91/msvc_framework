from rest_framework import serializers
from .fields import RemoteRelatedField


class RemoteRelatedSerializer(serializers.IntegerField):
    def to_representation(self, value):
        return value.get()


class ModelSerializer(serializers.ModelSerializer):
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        RemoteRelatedField: RemoteRelatedSerializer
    }
