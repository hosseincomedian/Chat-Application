from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(user, related_name='chatrooms')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def mymessages(self, num):
        return self.messages.order_by("-timestamp")[:num]

    @property
    def last_message(self):
        try:
            return self.messages.order_by('-timestamp').first()
        except:
            return None


class Message(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    mode_CHOICES = (
        ("s", "set"),
        ("n", "normal"),
    )
    mode = models.CharField(max_length=1, choices=mode_CHOICES, default='n')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.author.username
