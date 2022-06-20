from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserView.as_view()),
    path('login/', views.UserAPIView.as_view()),
    path('logout/', views.UserAPIView.as_view()),
]
