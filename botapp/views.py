from django.shortcuts import render
from django.http import HttpResponse
from botapp.ml.chatbot_utils import get_response

def home(request):
    return render(request, 'home.html')

def chat(request):
    return render(request, 'chat.html')

def chat_response(request):
    query = request.GET.get('query')
    response = get_response(query)
    return HttpResponse(response)

# placeholder views
def diagnose(request):
    return HttpResponse("🧪 Image diagnosis coming soon...")

def voice_chat(request):
    return HttpResponse("🎙 Voice-based chatbot coming soon...")

def about(request):
    return HttpResponse("ℹ️ AgriBot is a smart agriculture assistant project.")

def contact(request):
    return HttpResponse("📧 Contact us at agri@bot.com")
