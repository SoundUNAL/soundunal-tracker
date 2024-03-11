from rest_framework import serializers


class RecommendationSerializer(serializers.Serializer):
    """
    Serializer class for handling recommendation data.

    Attributes:
        songs (List[int]): A list of song IDs recommended to the user.
    """
    songs = serializers.ListField(child=serializers.IntegerField())
