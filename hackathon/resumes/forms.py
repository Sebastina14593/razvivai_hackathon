from .models import UserResume, UserResume2
from django.forms import ModelForm, MultipleChoiceField, TextInput, DateTimeInput, Textarea # здесь импортируем класс TextInput и DateTimeInput

class UserResumeForm(ModelForm):
    class Meta:
        model = UserResume
        fields = ["fio", "sberposition", "skills", "date"]

        widgets = {"fio" : TextInput(attrs={"class": "form-control",
                                            "placeholder" : "ФИО будущего сотрудника"}),

                   "sberposition": TextInput(attrs={"class": "form-control",
                                           "placeholder": "Позиция сотрудника в Сбере"}),

                   "skills": Textarea(attrs={"class": "form-control",
                                           "placeholder": "Навыки"}),

                   "date": DateTimeInput(attrs={"class": "form-control",
                                                "placeholder": "Дата публикации"}),
                   }

class UserResumeForm2(ModelForm):
    widgets = {"sex": MultipleChoiceField(choices={"мужской": 0, "женский": 1}),

               "fio": TextInput(attrs={"class": "form-control",
                                       "placeholder": "ФИО сотрудника"}),

               "work_exprience": TextInput(attrs={"class": "form-control",
                                                  "placeholder": "Стаж на последнем месте работы"}),

               "responsibilities": Textarea(attrs={"class": "form-control",
                                                   "placeholder": "Обязанности на последнем месте работы"}),

               "prof_area": TextInput(attrs={"class": "form-control",
                                             "placeholder": "Проф. Область на последнем месте работы"}),

               "position": TextInput(attrs={"class": "form-control",
                                            "placeholder": "Должность на последнем месте работы"}),

               "achievements": Textarea(attrs={"class": "form-control",
                                               "placeholder": "Достижения на последнем месте работы"}),

               "total_work_exprience": TextInput(attrs={"class": "form-control",
                                                        "placeholder": "Общий стаж"}),

               "prof_tags": TextInput(attrs={"class": "form-control",
                                             "placeholder": "Проф теги"}),

               "skills": TextInput(attrs={"class": "form-control",
                                          "placeholder": "Навыки"}),

               "hobbies": TextInput(attrs={"class": "form-control",
                                           "placeholder": "Интересы"}),

               "key_achievements": Textarea(attrs={"class": "form-control",
                                                   "placeholder": "Ключевые достижения"}),

               "career_status": TextInput(attrs={"class": "form-control",
                                                 "placeholder": "Карьерный статус"}),

               "management_experience": TextInput(attrs={"class": "form-control",
                                                         "placeholder": "Проф теги"}),

               "score": TextInput(attrs={"class": "form-control",
                                         "placeholder": "Оценка 5+"}),

               "language_skills": TextInput(attrs={"class": "form-control",
                                                   "placeholder": "Владение языками"}),

               "degree": Textarea(attrs={"class": "form-control",
                                          "placeholder": "Образование"}),

               "psychotype": TextInput(attrs={"class": "form-control",
                                              "placeholder": "Психологический тип"}),

               "motivations": TextInput(attrs={"class": "form-control",
                                              "placeholder": "Мотивация"})
               }
    class Meta:
        model = UserResume2
        fields = ["sex", "fio", "work_exprience", "responsibilities", "prof_area", "position", "achievements",
                  "total_work_exprience", "prof_tags", "skills", "hobbies", "key_achievements",
                  "career_status", "managment_experience", "score", "language_skills",
                  "degree", "psychotype", "motivations"
                  ]

