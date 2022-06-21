from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductView.as_view()),
    path('product/<obj_id>/', views.ProductView.as_view()),
]
