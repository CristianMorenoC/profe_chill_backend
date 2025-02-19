from django.shortcuts import render, get_object_or_404
from .models import Student, Teacher, User
from .serializer import StudentSerializer, TeacherSerializer, UserSerializer, PasswordResetSerializer

# rest framework imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import SignUpSerializer


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def reset_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
@api_view(['POST'])
def create_user(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "user": {
                "id": serializer.instance.id,
                "email": serializer.instance.email,
                "username": serializer.instance.username,
                "role": serializer.instance.role
            },
            "message": "User created successfully",
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verify_email(request, token):
    user = get_object_or_404(User, verification_token=token)
    user.is_email_verified = True
    user.verification_token = None  # Clear token after use
    user.save()
    
    return Response({
        'message': 'Email verified successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user

    if user.role == 'student':
        student = Student.objects.get(user=user)
        serializer = StudentSerializer(student, data=request.data)

    elif user.role == 'teacher':
        teacher = Teacher.objects.get(user=user)
        serializer = TeacherSerializer(teacher, data=request.data)
    else:
        return Response({'error': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)


    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_profiles(request):
    profiles = Student.objects.all()
    serializer = StudentSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)






