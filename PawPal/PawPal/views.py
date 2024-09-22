# from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    # return HttpResponse("Hi Homepage")
    return render(request, 'home.html')

def about(request):
    # return HttpResponse("Hi About")
    return render(request, 'about.html')