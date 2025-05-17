from django.shortcuts import render,redirect
from django.utils import timezone
from . models import TodoList

# Create your views here.

def show_task(request):
    task_list = TodoList.objects.all().order_by('-created_at')
    return render(request,'index.html',{"task_list":task_list})


def add_task(request):
    if request.POST and request.POST.get("task") != "":
        task = request.POST.get("task")
        list_obj = TodoList(task=task,  created_at=timezone.now())
        list_obj.save()
    return redirect("home")

def remove_task(request):
    return render(request,'index.html')

def check_task(request):
    return render(request,'index.html')