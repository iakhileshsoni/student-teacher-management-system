from .models import *
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "first_name", "username", "subjects"]


class StudentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Student
        fields = ["id", "student"]
        # depth = 1
        
    def to_representation(self, instance):
        # import ipdb; ipdb.set_trace()
        response = super().to_representation(instance)
        response["username"] = instance.student.username
        # Teacher Response
        data = instance.teacher.__dict__
        print("data: ", data)
        data.pop('_state')
        data['teacher_id']
        data['teacher_id'] = Teacher.objects.filter(id= data['teacher_id']).values()
        print("Teacher: ", data['teacher_id'])
        return response


class TeacherSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Teacher
        fields = ["id", "teacher", "subject"]
        depth = 1

