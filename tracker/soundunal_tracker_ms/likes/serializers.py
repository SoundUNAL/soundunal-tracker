from rest_framework import serializers


class InteractionCounterSerializer(serializers.Serializer):
    count = serializers.IntegerField()
