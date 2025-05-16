from django.shortcuts import render

# Create your views here.

def show_mainpage(request):
    return render(request,'index.html')