from __future__ import unicode_literals
import bcrypt
import re
from django.db import models
from datetime import datetime

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def validate_reg(self, post_data):
        errors = {}
        if len(post_data['name']) < 3:
            errors['name'] = "Name must be at least 3 characters"
        if len(post_data['alias']) < 3:
            errors['alias'] = "Alias must be at least 3 characters"
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "Please enter a valid Email"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if post_data['password'] != post_data['password_confirm']:
            errors['password_conf'] = "Please confirm your password correctly"
        if post_data['birthdate'] > datetime.now().strftime("%Y-%m-%d"):
            errors['birthday'] = "Your birthday must be in the past"
        if User.objects.filter(email=post_data['email']):
            errors['email_exists'] = "Sorry but that email address is already in use"
        return errors
    
    def validate_login(self, post_data):
        user_to_check = User.objects.get(email=post_data['email'])
        if user_to_check:
            if bcrypt.checkpw(post_data['password'].encode(), user_to_check.password.encode()):
                user = {
                    "user": user_to_check
                }
                return user
            else:
                errors = {
                    "error": "Login Invalid"
                }
                return errors
        else:
            errors = {
                "error": "Login Invalid"
            }
            return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="quotes")
    favorites = models.ManyToManyField(User, related_name="fav_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

