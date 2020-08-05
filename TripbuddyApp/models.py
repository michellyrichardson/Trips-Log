from django.db import models
import re, bcrypt

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name needs to be at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name needs to be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):               
            errors['email'] = "Invalid email address!"
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "Passwords do not match. Try again!"
        return errors
    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['login_email']):               
            errors['login_email'] = "That email is not registered in our system. Please try again!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return f'{self.id} - {self.first_name} {self.last_name}'

class TripsManager(models.Manager):
    def trips_validator(self, post_data):
        errors = {}
        if len(post_data['destination']) < 3:
            errors['destination'] = "Destination must be at least 3 characters long"
        if len(post_data['plan']) < 3:
            errors['plan'] = "Plan must be at least 3 characters long"
        
        return errors

class Tripsnew(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripsManager()

class Alltrips(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripsManager()