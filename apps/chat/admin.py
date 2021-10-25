from django.contrib import admin

from .models import ChatRoom, ChatMessage


class ChatMessageTabularAdmin(admin.TabularInline):
    model = ChatMessage
    extra = 0
    ordering = ('-created_at',)

    def has_change_permission(self, request, obj=None):
        return False


class ChatRoomAdmin(admin.ModelAdmin):
    inlines = [ChatMessageTabularAdmin]

    class Meta:
        model = ChatRoom


admin.site.register(ChatRoom, ChatRoomAdmin)
