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
            TodoList.objects.create(task=task_unauthorized)

        task_list = get_task_list()
        count = get_task_list(checked=False).count()
    else:
        task = ''
        task_list = []
        count = 0
    return render(request,'index.html',{
        "task_list":task_list,
        "task": task,
        "count":count
    })

def add_task(request):
    if request.method == "POST":
        task = request.POST.get("task", "").strip()
        if not task:
            return redirect("home")
        
        if not request.user.is_authenticated:
            request.session['prefill_task_unauthorized'] = task
            return redirect('login')
        
        list_obj = TodoList(task=task)
        list_obj.save()
    return redirect("home")

@login_required(login_url="login")
def check_task(request,pk):
    list_obj = get_task(pk)
    list_obj.is_checked = not list_obj.is_checked #toggle check box
    list_obj.save()
    return redirect("home")

@login_required(login_url="login")
def edit_task(request,pk):
    list_obj = get_task(pk)
    request.session['prefill_task'] = list_obj.task
    list_obj.delete()
    return redirect('home')

@login_required(login_url="login")
def remove_task(request,pk):
    list_obj = get_task(pk)
    list_obj.delete()
    return redirect("home")

@login_required(login_url="login")
def active_task(request):
    return filter_task(request=request, status=False)

@login_required(login_url="login")
def completed_task(request):
    return filter_task(request, status=True)


def filter_task(request, status):
    task_list = get_task_list(checked=status)
    count = task_list.count()
    return render(request,'index.html',{
        "task_list":task_list,
        "count":count
    })

def get_task(pk):
    """
    Retrieve a tasks from the database based on the primary key value.

    Args:
        pk (primary key value)

    Returns:
        QuerySet: An object of a task by a primary key value.
    """
    return get_object_or_404(TodoList, pk=pk)

def get_task_list(checked=None):
    """
    Retrieve a list of tasks from the database based on their completion status.

    Args:
        checked (bool or None, optional): 
            - True: return completed tasks.
            - False: return active (incomplete) tasks.
            - None: return all tasks.

    Returns:
        QuerySet: A list of tasks filtered by the completion status.
    """
    if checked is True:
        return TodoList.objects.filter(is_checked=True).order_by('-created_at')
    elif checked is False:
        return TodoList.objects.filter(is_checked=False).order_by('-created_at')
    else:
        return TodoList.objects.all().order_by('-created_at')