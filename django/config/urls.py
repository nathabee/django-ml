from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def health(_): return JsonResponse({"status": "ok"})

def hello(_): return JsonResponse({"service": "django", "message": "Hello from Django"})

urlpatterns = [path('admin/', admin.site.urls), path('health', health), path('api/hello', hello)]
