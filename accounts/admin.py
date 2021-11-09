from django.contrib import admin
from django.db import models
from accounts.models import Users, Subject, Student, Teacher

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'username', 'is_student']
admin.site.register(Users, UsersAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject']
admin.site.register(Subject, SubjectAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student']
admin.site.register(Student, StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher']
admin.site.register(Teacher, TeacherAdmin)