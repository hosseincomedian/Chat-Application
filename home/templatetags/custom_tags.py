from django import template
import json
from rest_framework import serializers

register = template.Library()
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from chat.serializers import ChatRoomSerializer


@register.simple_tag
def delete_chat(value):
    return value[5:]


@register.simple_tag
def mylist(value):
    serialized = ChatRoomSerializer(value, many=True)
    data = eval(JSONRenderer().render(serialized.data))
    content = {
        'message': data,
        'command': 'fetch_message',
    }
    data = json.dumps(data)
    print("data: ", data)
    return data


register.filter('delete_chat', delete_chat)
register.filter('mylist', mylist)
