from rest_framework import serializers
from .models import User, Student, Teacher, Class, Recording, ClassResume, Task, Review, Specialization
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

User = get_user_model()

class PasswordResetSerializer(serializers.ModelSerializer):
    """
    Password reset serializer
    """


    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        try:
            user = User.objects.get(email=email).first()
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if password != new_password:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if new_password != confirm_password:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def save(self, **kwargs):
        print("kwargs", kwargs)
        user = self.context['request'].user
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class SignUpSerializer(serializers.ModelSerializer):
    """
    Sign up serializer
    """
    role = serializers.ChoiceField(choices=User.ROLES)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'role']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def send_verification_email(self, user):
        """
        Send verification email to user
        """
        try:
            # Generate verification token
            token = get_random_string(64)
            user.verification_token = token
            user.save()

            # Create verification URL
            verification_url = f"http://localhost:8000/verify-email/{token}/"

            # Email content
            subject = 'Verify your email - Profe Chill'
            message = f'''
            Hi {user.username},

            Welcome to Profe Chill! Please verify your email by clicking the link below:

            {verification_url}

            If you didn't create this account, please ignore this email.

            Best regards,
            Profe Chill Team
            '''
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print("Email sent successfully")
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            print(f"Error type: {type(e)}")
            raise  # Re-raise the exception to see the full traceback

    def create(self, validated_data):
        # 1. Primero creamos el usuario
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        
        # 2. Luego enviamos el email de verificación
        self.send_verification_email(user)  # Necesitamos el usuario creado para enviar el email
        
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class StudentSerializer(serializers.ModelSerializer):
    """
    Student serializer
    """
    user = UserSerializer()


    class Meta:
        model = Student
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Update the student data
        """
        # Update the user data
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():

            setattr(instance.user, attr, value)
        instance.user.save()

        # Update the student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
class TeacherSerializer(serializers.ModelSerializer):
    """
    Teacher serializer
    """
    user = UserSerializer()


    class Meta:
        model = Teacher
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Update the teacher data
        """
        user_data = validated_data.pop('user, {}')
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
