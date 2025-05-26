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

# old ccode
# def signup_page(request):
#     if request.POST:
#         try:
#             username = request.POST.get("username")
#             email = request.POST.get("email")
#             password1 = request.POST.get("password1")
#             password2 = request.POST.get("password2")

#             if password1 == password2:
#                 user = User.objects.create_user(username=username, email=email,password=password1)
#                 user.save()
#                 success_message= 'User registered successfully'
#                 messages.success(request,success_message)
#                 return redirect("login")
#             else:
#                 error_message= "Password does not match"
#                 messages.error(request,error_message)
                
#         except Exception as e:
#             error_message= 'Username already taken or invalid inputs'
#             messages.error(request,error_message)

#     return render(request, 'signup.html')

# def login_page(request):
#     if request.POST:
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect("home")
#         else:
#             messages.error(request,"Invalid credentials")
#     return render(request, 'login.html')
