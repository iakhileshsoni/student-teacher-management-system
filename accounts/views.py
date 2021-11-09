from re import sub
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework import viewsets, mixins

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, viewsets
from rest_framework.authtoken.models import *
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions

from django.http import JsonResponse
from django.http import Http404

from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication



class Students(generics.ListCreateAPIView):
    # authentication_classes = (JWTAuthentication)
    # permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer

    def list(self, request):
        queryset = Student.objects.all().order_by('-id')
        serializer = self.serializer_class(queryset, many=True)
        return Response({"data": serializer.data,  "code": "HTTP_200_OK"})


class Teachers(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TeacherSerializer

    def list(self, request):
        queryset = Teacher.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"data": serializer.data,  "code": "HTTP_200_OK"})


class Report(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self,request):
        student_list = Student.objects.all()
        teacher_list = Teacher.objects.all()
        student = StudentSerializer(student_list, many=True)
        teacher = TeacherSerializer(teacher_list, many=True)

        # dict1 = {"student": student, "teacher": teacher}
        # return render(request, 'accounts/report.html', context=dict1 )
        
        return Response({"student":student.data, "teacher":teacher.data})


class UpdateUser(APIView):
    # permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Users.objects.get(id=pk)
        except Users.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        users = self.get_object(pk)
        serializer = TeacherSerializer(users)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        users = self.get_object(pk)
        serializer = TeacherSerializer(users, data=request.data)

        data_dict = self.request.data
        first_name = data_dict['first_name']
        subjects = data_dict['subjects']
    
        if serializer.is_valid():
            serializer.save()
            userData = TeacherSerializer(serializer.data)
            return Response({"message": "Record is Updated Successfully !!!",  "code": "HTTP_200_OK", "user": userData.data})
        return Response({"message": "Record is not Updated !!!",  "code": "HTTP_400_BAD_REQUEST"})


