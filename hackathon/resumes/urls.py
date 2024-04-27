from django.urls import path
from . import views

urlpatterns = [
    path('', views.resumes_home, name="resumes_home"),
    path('create', views.create, name="create"),
    path('<int:pk>', views.ResumesDetailView.as_view(), name = 'resumes_detail'), # pk - primery key
    path('<int:pk>/update', views.ResumesUpdateView.as_view(), name = 'resumes_update'), # для обновления резюме
    path('<int:pk>/delete', views.ResumesDeleteView.as_view(), name = 'resumes_delete') # для обновления резюме
]