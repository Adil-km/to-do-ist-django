from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .forms import SignupForm, LoginForm
# Create your views here.

def signup_page(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        try:
            if form.is_valid():
                success_message= 'User registered successfully'
                messages.success(request,success_message)
                form.save()
                return redirect('login')

        except Exception as e:
            error_message= 'Invalid inputs'
            messages.error(request,error_message)
    else:
        form = SignupForm()

    return render(request,'signup.html', {'form':form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
    else:
        form = LoginForm()

    return render(request,'login.html', {'form': form})


def logout_page(request):
    success_message= "You've been logged out"
    messages.success(request,success_message)
    logout(request)
    return redirect("login")
