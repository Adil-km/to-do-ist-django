from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .forms import UserCreation
# Create your views here.


def temp(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully!')
            return HttpResponse("<p>hiii</p>")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreation()

    return render(request,'temp.html', {'form':form})



def signup_page(request):
    if request.POST:
        try:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 == password2:
                user = User.objects.create_user(username=username, email=email,password=password1)
                user.save()
                success_message= 'User registered successfully'
                messages.success(request,success_message)
                return redirect("login")
            else:
                error_message= "Password does not match"
                messages.error(request,error_message)
                
        except Exception as e:
            error_message= 'Username already taken or invalid inputs'
            messages.error(request,error_message)

    return render(request, 'signup.html')

def login_page(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request,"Invalid credentials")
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect("login")