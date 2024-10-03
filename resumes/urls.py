# resumes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('resumes/', views.resume_list, name='resume_list'),
]
