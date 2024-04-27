"""
URL configuration for hackathon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Когда пользователь заходит на главную страницу вызывается главный метод urls.py (В файле settings: ROOT_URLCONF = 'hackathon.urls')
# В данном файле отслеживаются url адреса
from django.contrib import admin
from django.urls import path, include # дополнил методом include

# Ниже представлены библиотеки, которые позволят обратиться к файлику settings,
# а также к ключевому слову static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # при переходе в url в admin происходит переход в панель администратора
    path('', include('main.urls')), # т.е. при переходе на главну страниуц мы делегирауем все полномочия приложению main
    # для этого необходимо прописать также метод include, который включает другой модуль
    # конфигурации (main)
    path('resumes/', include('resumes.urls')), # если пользователь переходит на адрес resumes, то обработка через файл resumes
    path('chatbot/', include('chatbot.urls')) # если пользователь переходит к чатботу
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
