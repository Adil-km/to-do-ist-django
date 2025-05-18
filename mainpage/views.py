from django.shortcuts import render,redirect
from django.utils import timezone
from . models import TodoList

# Create your views here.

def show_task(request):
    task = request.session.pop('prefill_task', '')

    task_list = TodoList.objects.all().order_by('-created_at')
    count = TodoList.objects.filter(is_checked = False).count()

    return render(request,'index.html',{"task_list":task_list,'task': task,"count":count})


def add_task(request):
    if request.POST and request.POST.get("task") != "":
        task = request.POST.get("task")
        list_obj = TodoList(task=task,  created_at=timezone.now())
        list_obj.save()
    return redirect("home")

def remove_task(request,pk):
    list_obj = TodoList.objects.get(pk=pk)
    if list_obj:
        list_obj.delete()
        return redirect("home")

def check_task(request,pk):
    list_obj = TodoList.objects.get(pk=pk)
    if list_obj:
        list_obj.is_checked = not list_obj.is_checked
        list_obj.save()
        return redirect("home")
    
def active_task(request):
    task_list = TodoList.objects.all().order_by('-created_at').filter(is_checked = False)
    count = TodoList.objects.filter(is_checked = False).count()
    return render(request,'index.html',{"task_list":task_list,"count":count})

def completed_task(request):
    task_list = TodoList.objects.all().order_by('-created_at').filter(is_checked = True)
    count = TodoList.objects.filter(is_checked = True).count()
    return render(request,'index.html',{"task_list":task_list,"count":count})


def edit_task(request,pk):
    list_obj = TodoList.objects.get(pk=pk)
    task_data = list_obj.task
    list_obj.delete()
    request.session['prefill_task'] = task_data
    return redirect('home')