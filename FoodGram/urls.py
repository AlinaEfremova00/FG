from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Привет, Алинка! Фудграм работает 🍲</h1>")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
    path('', index),
]
