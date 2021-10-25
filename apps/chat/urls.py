from django.urls import path

from .views import ChatRoomView, InboxView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view()),
    path(r"<username>/", ChatRoomView.as_view()),
]
