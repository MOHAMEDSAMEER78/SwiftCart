# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# User registration view
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import group
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for the new user'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the new user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the new user'),
                'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role of the user (Customer, Sales Manager, Admin)'),
            },
        ),
        responses={201: openapi.Response('User created successfully!')}
    )
    def post(self, request):
        data = request.data

        # Validate and retrieve the role group
        role_name = data.get('role', 'Customer')
    
        # Create the user
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=role_name
        )

        # Associate the user with the role group (if applicable)
        user.save()

        return Response({'message': 'User created successfully!'}, status=201)

# User login view
class LoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
            },
        ),
        responses={200: openapi.Response('Tokens returned successfully')}
    )
    def post(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# Example of Admin-only view
class AdminView(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        responses={200: openapi.Response('Only Admin can access this.')}
    )
    def get(self, request):
        return Response({"message": "Only Admin can access this."})
