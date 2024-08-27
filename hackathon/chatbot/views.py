from django.shortcuts import render
from django.http import JsonResponse
from .facilitator import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Chat
from django.utils import timezone

def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    print(str(chats))
    if request.method == 'POST':
        message = request.POST.get("message")
        response = main_facilitator(message + str(chats))
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, "response": response})
    return render(request, 'chatbot/chatbot.html', {'chats': chats})

@csrf_exempt
def generate_messages(request):
    if request.method == 'POST':
        chats_history = "; ".join([x["message"] for x in Chat.objects.filter(user=request.user).values('message')])
        transformed_messages = [facilitator("Человеческое существо", chats_history)]

        # Формируем данные для ответа
        response_data = []
        for msg in transformed_messages:
            response_data.append({
                'type': 'received',
                'sender': 'ДУСя',
                'content': msg
            })

        chat = Chat(user=request.user, message="Сгенерируй обратную связь", response=transformed_messages[0], created_at=timezone.now())
        chat.save()

        return JsonResponse({'messages': response_data})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def clear_chat(request):
    if request.method == 'POST':
        # Удалите все сообщения для текущего пользователя
        Chat.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

