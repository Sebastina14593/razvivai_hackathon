from django.db import models

# Create your models here.
# Здесь создаем таблицу
class UserResume(models.Model):

    fio = models.CharField('ФИО кандидата', max_length=100)
    sberposition = models.CharField('Позиция в структуре Сбера', max_length=250)
    skills = models.TextField('Навыки')
    date = models.DateTimeField('Дата публикации')

    def __str__(self): # чтобы возвращалось именно ФИО сотрудника, а не ссылка на объект
        return f'Кандидат: {self.fio}'

    def get_absolute_url(self): # здесь храниться функция, которая отвевчает за, куда направлять пользователя после обновления резюме
        return f'/resumes/{self.id}'

    class Meta:
        verbose_name = 'Резюме кандидата'
        verbose_name_plural = 'Резюме кандидатов'

class UserResume2(models.Model):

    sex = models.PositiveIntegerField('Пол')
    fio = models.CharField('ФИО', max_length=250)
    work_exprience = models.PositiveIntegerField('Стаж на последнем месте работы')
    responsibilities = models.TextField('Обязанности на последнем месте работы')
    prof_area = models.CharField('Проф. Область на последнем месте работы', max_length=250)
    position = models.CharField('Должность на последнем месте работы', max_length=250)
    achievements = models.TextField('Достижения на последнем месте работы')
    total_work_exprience = models.PositiveIntegerField('Общий стаж')
    prof_tags = models.CharField('Проф теги', max_length=250)
    skills = models.CharField('Навыки', max_length=250)
    hobbies = models.CharField('Интересы', max_length=250)
    key_achievements = models.TextField('Ключевые достижения')
    career_status = models.PositiveIntegerField('Карьерный статус')
    managment_experience = models.PositiveIntegerField('Опыт управления')
    score = models.CharField('Оценка 5+', max_length=2)
    language_skills = models.CharField('Владение языками', max_length=250)
    degree = models.TextField('Образование')
    psychotype = models.CharField('Психологический тип', max_length=250)
    motivations = models.CharField('Мотивация', max_length=250)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self): # чтобы возвращалось именно ФИО сотрудника, а не ссылка на объект
        return f'Кандидат: {self.fio}'

    def get_absolute_url(self): # здесь храниться функция, которая отвевчает за, куда направлять пользователя после обновления резюме
        return f'/resumes/{self.id}'

    class Meta:
        verbose_name = 'Резюме кандидата (версия 2)'
        verbose_name_plural = 'Резюме кандидатов (версия 2)'