from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_task, name="home"),
    path('add/', views.add_task, name="add"),
    path('remove/<pk>', views.remove_task, name="remove"),
    path('checkbox/<pk>', views.check_task, name="checkbox"),
    path('active/', views.active_task, name="active"),
    path('completed/', views.completed_task, name="completed"),
    path('edit/<pk>', views.edit_task, name="edit"),
]
