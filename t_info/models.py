from django.db import models

# Create your models here.


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=100)
    teacher_language = models.CharField(max_length=50)
    teacher_description = models.CharField(max_length=500)
    teacher_contact = models.CharField(max_length=15)
    teacher_email = models.EmailField()
    teacher_residence = models.CharField(max_length=500)
    teacher_city = models.CharField(max_length=50)

    class Meta:
        ordering = ['teacher_city','teacher_name']