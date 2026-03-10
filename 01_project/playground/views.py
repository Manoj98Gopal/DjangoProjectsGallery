from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request,string):
    return render(request, 'hello.html', {"name": string})
