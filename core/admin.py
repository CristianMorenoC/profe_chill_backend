from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Student, Teacher, Class, Recording, ClassResume, Task, Review, Specialization

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Recording)
admin.site.register(ClassResume)
admin.site.register(Task)
admin.site.register(Review)
admin.site.register(Specialization)