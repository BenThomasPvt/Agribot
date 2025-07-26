from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('get-response/', views.chat_response, name='chat_response'),
    path('diagnose/', views.diagnose, name='diagnose'),
    path('voice/', views.voice_chat, name='voice_chat'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
