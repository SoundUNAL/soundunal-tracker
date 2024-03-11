from rest_framework import serializers


class InteractionCounterSerializer(serializers.Serializer):
    count = serializers.IntegerField()


class UserReactionSerializer(serializers.Serializer):
    reaction = serializers.BooleanField()


class UserSongsSerializer(serializers.Serializer):
    songs = serializers.ListField(child=serializers.IntegerField())


class CommentsSerializer(serializers.Serializer):
    comments = serializers.ListField(child=serializers.CharField())
