# В данном файле отслеживаются url адреса
# from django.contrib import admin # не понадобиться панель администратора
from django.urls import path # include # не понадобится метод include
from . import views

urlpatterns = [
    path('', views.index, name="home"), # не надо указывать круглых скобок (т.к. нужно лишь обратиться к нему без его выполнения)
    path('about', views.about, name="about"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout")
]