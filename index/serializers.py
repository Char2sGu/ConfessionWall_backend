from rest_framework import serializers
from . import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('id', 'display_name', 'sex')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ('confession', 'creation_time')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('id', 'confession', 'text', 'creation_time')


class ConfessionSerializer(serializers.ModelSerializer):
    likes = serializers.ReadOnlyField()
    comments = serializers.ReadOnlyField()

    class Meta:
        model = models.Confession
        fields = ('id', 'sender', 'receiver', 'creation_time',
                  'text', 'likes', 'comments')
