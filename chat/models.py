from django.db import models
from shortuuidfield import ShortUUIDField
from user.models import User

# Create your models here.

class ChatRoom(models.Model):
    roomId = ShortUUIDField()
    type = models.CharField(
        max_length=10,
        default='dm'
    )
    member = models.ManyToManyField(
        User
    )
    name = models.CharField(
        max_length=40,
        blank=False
    )

    def __str__(self):
        return self.roomId + str(self.nome)


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        ChatRoom,
        on_delete=models.SET_NULL,
        null=True
    )

    user = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True

        )
    
    message = models.CharField(
        max_length=225
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.message
    

