# UserCore/views.py
# 
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
 
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import AllowAny



@api_view(["GET"])
@permission_classes([AllowAny])
def hello(_req):
    return JsonResponse({"service":"django", "message":"Hello from Django"})
 
 

@api_view(["GET"])
@authentication_classes([JWTAuthentication])   # <- important
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return JsonResponse({"id": u.id, "username": u.username, "email": u.email})