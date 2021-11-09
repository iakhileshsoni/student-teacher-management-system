from django.urls import path
from rest_framework import routers
from accounts import views


urlpatterns = [
    path('students/', views.Students.as_view(), name='Student'),
    path('teachers/', views.Teachers.as_view(), name='Teacher'),
    path('reports/', views.Report.as_view(), name='Report'),
    path('update/<str:pk>/', views.UpdateUser.as_view(), name='update'),
]
