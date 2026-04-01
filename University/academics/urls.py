from django.urls import path
from . import views


app_name = 'academics'

urlpatterns = [
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/', views.department_detail,name='department_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
]