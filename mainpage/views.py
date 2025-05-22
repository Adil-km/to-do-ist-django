from django.shortcuts import render,redirect
from django.utils import timezone
from . models import TodoList
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.


def show_task(request):
    if request.user.is_authenticated:
        task = request.session.pop('prefill_task', '')  

        task_unauthorized = request.session.pop('prefill_task_unauthorized', '')
        if task_unauthorized:
            TodoList.objects.create(task=task_unauthorized, created_at=timezone.now())
            request.session.pop('prefill_task_unauthorized', None)

        task_list = TodoList.objects.all().order_by('-created_at')
        count = task_list.filter(is_checked=False).count()
    else:
        task = ''
        task_list = []
        count = 0
    return render(request,'index.html',{"task_list":task_list,'task': task,"count":count})


def add_task(request):
    if request.POST and request.POST.get("task") != "":
        task = request.POST.get("task", "").strip()

        if not request.user.is_authenticated:
            request.session['prefill_task_unauthorized'] = task
            return redirect('login')

        if not task:
            return redirect("home")

        print(task)
        list_obj = TodoList(task=task,  created_at=timezone.now())
        list_obj.save()
    return redirect("home")

@login_required(login_url="login")
def check_task(request,pk):
    list_obj = get_object_or_404(TodoList, pk=pk)
    list_obj.is_checked = not list_obj.is_checked
    list_obj.save()
    return redirect("home")

@login_required(login_url="login")
def edit_task(request,pk):
    list_obj = get_object_or_404(TodoList, pk=pk)
    task_data = list_obj.task
    list_obj.delete()
    request.session['prefill_task'] = task_data
    return redirect('home')

@login_required(login_url="login")
def remove_task(request,pk):
    list_obj = get_object_or_404(TodoList, pk=pk)
    list_obj.delete()
    return redirect("home")

@login_required(login_url="login")
def active_task(request):
    task_list = TodoList.objects.filter(is_checked = False).order_by('-created_at')
    count = task_list.count()
    return render(request,'index.html',{"task_list":task_list,"count":count})

@login_required(login_url="login")
def completed_task(request):
    task_list = TodoList.objects.filter(is_checked = True).order_by('-created_at')
    count = task_list.count()
    return render(request,'index.html',{"task_list":task_list,"count":count})
