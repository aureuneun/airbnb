from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from users import models as user_models
from . import models


def go_conversation_view(request, host, guest):
    host = user_models.User.objects.get_or_none(pk=host)
    guest = user_models.User.objects.get_or_none(pk=guest)
    if host is not None and guest is not None:
        try:
            conversation = models.Conversation.objects.filter(participants=host).get(
                participants=guest
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(host, guest)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):

    """ ConversationDetail View Definition """

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if conversation is None:
            raise Http404
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message")
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if conversation is None:
            raise Http404
        if message is not None:
            models.Message.objects.create(
                message=message,
                user=self.request.user,
                conversation=conversation,
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))