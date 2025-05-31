from django.shortcuts import render,redirect
from django.utils import timezone
from . models import TodoList
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

def crash(request):
    raise Exception("Test 500")

def show_task(request):
    if request.user.is_authenticated:
        task = request.session.pop('prefill_task', '')  

        task_unauthorized = request.session.pop('prefill_task_unauthorized', '')

        if task_unauthorized:
            TodoList.objects.create(task=task_unauthorized, user = request.user)

        task_list = get_task_list(user=request.user)
        count = task_list.filter(is_checked=False).count()
    else:
        task = ''
        task_list = []
        count = 0

    return render(request,'index.html',{
        "task_list":task_list,
        "task": task,
        "count":count,
    })

def add_task(request):
    if request.method == "POST":
        task = request.POST.get("task", "").strip()
        if not task:
            return redirect("home")
        
        if not request.user.is_authenticated:
            request.session['prefill_task_unauthorized'] = task
            return redirect('login')
        
        list_obj = TodoList(user= request.user, task=task)
        list_obj.save()
    return redirect("home")

@login_required(login_url="login")
def check_task(request,pk):
    list_obj = get_task(user=request.user, pk=pk)
    list_obj.is_checked = not list_obj.is_checked #toggle check box
    list_obj.save()
    return redirect("home")

@login_required(login_url="login")
def edit_task(request,pk):
    list_obj = get_task(user=request.user, pk=pk)
    request.session['prefill_task'] = list_obj.task
    list_obj.delete()
    return redirect('home')

@login_required(login_url="login")
def remove_task(request,pk):
    list_obj = get_task( user= request.user,pk=pk)
    list_obj.delete()
    return redirect("home")

@login_required(login_url="login")
def active_task(request):
    return filter_task(request=request, status=False)

@login_required(login_url="login")
def completed_task(request):
    return filter_task(request, status=True)


def filter_task(request, status):
    task_list = get_task_list(user= request.user, checked=status).select_related('user')
    count = task_list.count()
    return render(request,'index.html',{
        "task_list":task_list,
        "count":count
    })

def get_task( user,pk):
    """
    Retrieve a task object from the database based on the primary key and user.

    Args:
        user (User): The user who owns the task.
        pk (int): The primary key of the task.

    Returns:
        TodoList: A single task object.
    """
    return get_object_or_404(TodoList,user = user, pk=pk)

def get_task_list(user,checked=None):
    """
    Retrieve a list of tasks from the database based on their completion status.

    Args:
        user (User): The user whose tasks are being retrieved.
        checked (bool or None, optional): 
            - True: return completed tasks.
            - False: return active (incomplete) tasks.
            - None: return all tasks.

    Returns:
        QuerySet: A list of tasks filtered by the completion status.
    """
    
    queryset = TodoList.objects.filter(user=user).order_by('-created_at')
    if checked is True:
        queryset = queryset.filter(is_checked=True)
    elif checked is False:
        queryset = queryset.filter(is_checked=False)
    return queryset