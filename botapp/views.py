from django.shortcuts import render
from django.http import HttpResponse

from rag.engine import ask


def home(request):
    return render(request, 'home.html')


def chat(request):
    return render(request, 'chat.html')


def chat_response(request):
    query = request.GET.get('query', '').strip()

    if not query:
        return HttpResponse("Please enter a question.")

    try:
        result = ask(query)

        answer = result["answer"]
        sources = result["sources"]

        source_text = "\n\nSources:\n"

        for source in sources:
            source_text += f"• {source}\n"

        return HttpResponse(
            answer + source_text
        )

    except Exception as e:
        return HttpResponse(
            f"Sorry, something went wrong: {str(e)}"
        )


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
