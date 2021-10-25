from django.contrib import admin

from .models import ChatRoom, ChatMessage


class ChatMessageTabularAdmin(admin.TabularInline):
    model = ChatMessage


class ChatRoomAdmin(admin.ModelAdmin):
    inlines = [ChatMessageTabularAdmin]

    class Meta:
        model = ChatRoom


admin.site.register(ChatRoom, ChatRoomAdmin)
