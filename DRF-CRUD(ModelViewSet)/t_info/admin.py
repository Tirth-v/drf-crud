from django.contrib import admin
from .models import Teacher
# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_name','teacher_language','teacher_description','teacher_contact','teacher_email','teacher_residence','teacher_city']