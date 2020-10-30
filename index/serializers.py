from rest_framework import serializers

from . import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('nickname', 'sex')


class ConfessionSerializer(serializers.ModelSerializer):
    sender = PersonSerializer(read_only=True)
    receiver = PersonSerializer(read_only=True)

    class Meta:
        model = models.Confession
        fields = ('id', 'sender', 'receiver', 'creation_time', 'text', 'like')
