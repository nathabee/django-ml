from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return JsonResponse({"id": user.id, "username": user.username})
 


def health(_): return JsonResponse({"status": "ok"})
def hello(_): return JsonResponse({"service": "django", "message": "Hello from Django"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", health),
    path("api/hello", hello),

    # JWT auth
    path("api/auth/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/me", me),
]
