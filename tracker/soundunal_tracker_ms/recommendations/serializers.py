from rest_framework import serializers
from .response import Recommendation 


class RecommendationSerializer(serializers.Serializer):
    songs = serializers.ListField(child=serializers.IntegerField())



