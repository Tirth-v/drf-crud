from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id','teacher_name','teacher_language','teacher_description','teacher_contact','teacher_email','teacher_residence','teacher_city']
