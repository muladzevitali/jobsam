from django.conf import settings
from django.db import models
from django.db.models import Q


class ChatRoomManager(models.Manager):
    def by_user(self, user):
        filter_user_room = Q(first_user=user) | Q(second_user=user)
        filter_non_self_room = Q(first_user=user) & Q(second_user=user)

        return self.get_queryset().filter(filter_user_room).exclude(filter_non_self_room).distinct()

    def get_or_create(self, first_user, second_user):
        if first_user == second_user:
            return None

        filter_first = Q(first_user=first_user) & Q(second_user=second_user)
        filter_second = Q(first_user=second_user) & Q(second_user=first_user)

        queryset = self.get_queryset().filter(filter_first | filter_second).distinct()
        if queryset.count():
            return queryset.order_by('updated_at').first(), False

        room = self.model(first_user=first_user, second_user=second_user, )
        room.save()

        return room, True


class ChatRoom(models.Model):
    first_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='chat_room_first_user')
    second_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='chat_room_second_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChatRoomManager()

    @property
    def room_name(self):
        return f'chat-{self.id}'

    # def broadcast(self, message=None):
    #     if message:
    #         broadcast_message_to_chat(message, group_name=self.room_name, user='admin')
    #         return True
    #     return False


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
