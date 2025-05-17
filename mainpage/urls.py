from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_task, name="home"),
    path('add/', views.add_task, name="add"),
]
