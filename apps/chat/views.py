from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import ComposeForm
from .models import ChatRoom, ChatMessage


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'

    def get_queryset(self):
        return ChatRoom.objects.by_user(self.request.user)


class ChatRoomView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/chat_room.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return ChatRoom.objects.by_user(self.request.user)

    def get_object(self, **kwargs):
        target_user = get_object_or_404(User, username=self.kwargs.get("username"))
        chat_room, created = ChatRoom.objects.get_or_create(self.request.user, target_user)
        if not chat_room:
            raise Http404

        return chat_room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.get_form()
        if not form.is_valid():
            self.form_invalid(form)

        chat_room = self.get_object()
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=request.user, chat_room=chat_room, message=message)
        return super().form_valid(form)

    def form_valid(self, form):
        chat_room = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, chat_room=chat_room, message=message)

        return super().form_valid(form)
