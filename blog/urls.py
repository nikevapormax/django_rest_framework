from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('article/', views.ArticleView.as_view()),
]
