from django.contrib import admin
from .models import Message, ChatRoom


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ('author', 'content', 'chatroom')
    list_display = ('content', 'timestamp')

@admin.register(ChatRoom)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')
