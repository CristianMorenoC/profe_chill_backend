from rest_framework import serializers
from .models import User, Student, Teacher, Class, Recording, ClassResume, Task, Review, Specialization

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'name', 'surname', 'patronymic', 'birth_date', 'phone', 'photo']

    def update(self, instance, validated_data):
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
