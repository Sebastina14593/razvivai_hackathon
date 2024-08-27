from django.urls import path
from . import views
urlpatterns = [
    path('', views.chatbot, name="chatbot"),
    path('generate/', views.generate_messages, name='generate_messages'),
    path('clear/', views.clear_chat, name='clear_chat'),
]

