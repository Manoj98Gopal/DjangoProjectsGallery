from django.shortcuts import render
from store.models import Product

# Create your views here.

def say_hello(request):

    qs = Product.objects.all()[:5]
    
    
    return render(request,'hello.html',{'qs':qs})