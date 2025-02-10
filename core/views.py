from django.shortcuts import render
from .models import Student, Teacher
from .serializer import StudentSerializer, TeacherSerializer

# rest framework imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.

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
