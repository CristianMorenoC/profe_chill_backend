from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default='student'
    )

# ----------------------
# Student Model
# ----------------------
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    personal_goal = models.TextField(blank=True, null=True)
    goal_date = models.DateTimeField(blank=True, null=True)
    sex = models.CharField(max_length=10, default='not specified')
    time_zone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Student: {self.user.username}"

# ----------------------
# Teacher Model
# ----------------------
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    short_about_me = models.CharField(max_length=255, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    languages = models.JSONField(default=list)  # Stores an array of languages
    calendar_available = models.JSONField(default=dict)  # Available time slots
    number_classes = models.IntegerField(default=0)
    link_photo = models.TextField(blank=True, null=True)
    link_video = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Teacher: {self.user.username}"

# ----------------------
# Language Level Model
# ----------------------
class LanguageLevel(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]
    
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, unique=True)
    skill = models.CharField(max_length=50)  # e.g., Reading, Writing, Speaking

    def __str__(self):
        return f"{self.level} - {self.skill}"

# ----------------------
# Class Model
# ----------------------
class Class(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
        ('rescheduled', 'Rescheduled'),
        ('no_show', 'No Show'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meeting_date_time = models.DateTimeField()
    zoom_link = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return f"Class with {self.teacher.user.username} and {self.student.user.username} on {self.meeting_date_time}"

# ----------------------
# Recording Model
# ----------------------
class Recording(models.Model):
    class_session = models.OneToOneField(Class, on_delete=models.CASCADE)
    recording_link = models.TextField()
    expired_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Recording for {self.class_session}"

# ----------------------
# Class Resume Model
# ----------------------
class ClassResume(models.Model):
    class_session = models.OneToOneField(Class, on_delete=models.CASCADE)
    resume_link = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Class Resume for {self.class_session}"

# ----------------------
# Task Model
# ----------------------
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    class_session = models.ForeignKey(Class, on_delete=models.CASCADE)
    content_name = models.CharField(max_length=255)
    content_url = models.TextField()
    presented_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Task: {self.content_name} for {self.class_session}"

# ----------------------
# Review Model
# ----------------------
class Review(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.student.user.username} for {self.teacher.user.username}"

# ----------------------
# Specialization Model
# ----------------------
class Specialization(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    specialization_name = models.CharField(max_length=100)
    goal_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.specialization_name} for {self.student.user.username}"