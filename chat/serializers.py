from rest_framework import serializers
from .models import Message, ChatRoom


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['__str__', 'content', 'timestamp', 'author', 'mode']

    def get_author(self, object):
        return object.author.photo.url


class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['name', 'created_time', 'last_message']

    def get_last_message(self, object):
        return MessageSerializer(object.last_message).data
