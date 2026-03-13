from django.urls import path
from .views import say_hello

urlpatterns = [
    path("hello/<string>", say_hello)
]
