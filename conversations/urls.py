from django.urls import path
from . import views

app_name = "conversations"

urlpatterns = [
    path("go/<int:host>/<int:guest>/", views.go_conversation_view, name="go"),
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="detail"),
]
