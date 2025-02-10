from rest_framework import serializers
from .models import User, Student, Teacher, Class, Recording, ClassResume, Task, Review, Specialization

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
    
    # def create(self, validated_data):
    #     user_data = validated_data.pop('user', {})
    #     user = User.objects.create(**user_data)
    #     student = Student.objects.create(user=user, **validated_data)
    #     return student
    
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
    
