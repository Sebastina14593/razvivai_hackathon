from django.shortcuts import render, redirect # (удобно)
# Для регистрации
from django.contrib import auth
from django.contrib.auth.models import User
# from django.http import HttpResponse # для вывода текста (неудобно)
# Create your views here.
# def index(request): # обязательный параметр request в каждом из используемых методов
#     return HttpResponse("<h4>Проверка работы</h4>")

# def about(request):
#     return HttpResponse("<h4>Страница про нас</h4>")

def index(request):
    # сделаем передачу данных с помощью словаря
    data = {
        'title' : 'помощник',
        'values' : ['Вика', 'Даня', 'Никита', 'Орхан', 'Рома'],
        'obj': {'Вика' : 22, 'Даня' : 23, 'Никита' : 23, 'Орхан' : 23, 'Рома' : 23}
    }
    # return render(request, 'main/index.html') # нужно сздать html шаблон, который должен находится в templates (в каждом приложении)
    return render(request,'main/index.html', data)  # здесь будут данные передаваевые внутрь шаблона в формаате словаря

def about(request):
    return render(request, 'main/about.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            error_message = 'Некорректное имя пользователя или пароль'
            return render(request, 'main/login.html', {'error_message': error_message})

    else:
        return render(request, 'main/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('home')
            except:
                error_message = 'Ошибка при создании аккаунта'
                return render(request, 'main/register.html', {'error_message': error_message})
        else:
            error_message = 'Пароли не совпали'
            return render(request, 'main/register.html', {'error_message': error_message})
    return render(request, 'main/register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')