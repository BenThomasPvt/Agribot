from django.urls import path
from . import views


urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # RAG Chatbot
    path('chat/', views.chat, name='chat'),
    path('get-response/', views.chat_response, name='chat_response'),

    # Project information
    path('about/', views.about, name='about'),

    # Developer / contact information
    path('contact/', views.contact, name='contact'),
]
