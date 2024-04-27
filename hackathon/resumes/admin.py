from django.contrib import admin
# from .models import UserResume, UserResume2
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(UserResume, UserResume2)
class ViewAdmin(ImportExportModelAdmin):
    pass
# class RecordAdmin(ImportExportModelAdmin):
#     list_display = ('sex'
# ,'fio'
# ,'work_exprience'
# ,'responsibilities'
# ,'prof_area'
# ,'position'
# ,'achievements'
# ,'total_work_exprience'
# ,'prof_tags'
# , 'skills'
# ,'hobbies'
# ,'key_achievements'
# ,'career_status'
# ,'managment_experience'
# ,'score'
# ,'language_skills'
# ,'degree'
# ,'psychotype'
# ,'motivations')
# # Register your models here.
# admin.site.register(UserResume)
# admin.site.register(UserResume2)
