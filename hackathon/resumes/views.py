from django.shortcuts import render, redirect # redirect - для переадресации
# Здесь проипишем методы, вызывающие вывод резюме на сайт
from .models import UserResume, UserResume2
from .forms import UserResumeForm, UserResumeForm2# импортируем новый объект класса
from django.views.generic import DetailView, UpdateView, DeleteView # на основе класса DetailView можно создать динамическую страницу
# а на основе класса UpdateView будет происходить обновление
# на основе DeleteView - удаление
# Create your views here.
# Первый способ создания каждой из статьи
def resumes_home(request):
    resumes = UserResume.objects.order_by('-date')
    resumes2 = UserResume2.objects.order_by('-created_at')
    return render(request, 'resumes/resumes_home.html', {"resumes": resumes2})

# Второй способ - с помощью готовых классов django (предпочтительнеее)
class ResumesDetailView(DetailView): # главное указать, что он все наследует от класса DetailView
    # model = UserResume
    model = UserResume2
    template_name = 'resumes/details_view.html'
    context_object_name = 'resume' # название ключа, по которому передается объект внутрь шаблона

class ResumesUpdateView(UpdateView): # наследует от класса UpdateView
    # model = UserResume
    model = UserResume2
    template_name = 'resumes/create.html' # можно для страницы редактирования прописать шаблон создания резюме

    # form_class = UserResumeForm
    form_class = UserResumeForm2
    # fields = ["fio", "sberposition", "skills", "date"]

class ResumesDeleteView(DeleteView): # наследует от класса DeleteView
    # model = UserResume
    model = UserResume2
    success_url = '/resumes'
    template_name = 'resumes/resumes_delete.html' # другой шаблон
def create(request):
    error = ''
    if request.method == 'POST': # данные отпарвляются из формы
        form = UserResumeForm2(request.POST) # в этом объекте находятся все те данные, полученные пользователем от формы
        if form.is_valid():
            form.save()
            return redirect('home')# для переадресации
        else:
            error = 'Форма была неверной'


    form = UserResumeForm2()

    data = {'form': form,
            'error': error
            }

    return render(request, 'resumes/create.html', data)

