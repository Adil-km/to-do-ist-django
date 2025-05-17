from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_task, name="home"),
    path('add/', views.add_task, name="add"),
    path('remove/<pk>', views.remove_task, name="remove"),
    path('checkbox/<pk>', views.check_task, name="checkbox"),
]
