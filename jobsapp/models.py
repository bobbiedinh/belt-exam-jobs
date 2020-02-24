from django.db import models
from datetime import datetime
import re
import bcrypt

# Create your models here.
class Manager(models.Manager):
    def regValidator(self, postDATA):
        errors={}
        EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postDATA['email']):
            errors['email']="Email in incorrect format"
        elif User.objects.filter(email=postDATA['email']):
            errors['email']="Email exists"
        if len(postDATA['first'])<2:
            errors['first']="First name must have more than 2 characters"
        if len(postDATA['last'])<2:
            errors['last']="Last name must have more than 2 characters"
        if len(postDATA['password'])<6:
            errors['password']="Password must be 6+ characters"
        elif (postDATA['password']!=postDATA['confirm']):
            errors['password']="Passwords do not match"
        return errors
    
    def loginValidator(self, postDATA):
        errors={}
        user = User.objects.filter(email=postDATA['email'])
        if not user:
            errors['email']="Email not registered"
            return errors
        logged_user=user[0]
        if not bcrypt.checkpw(postDATA['password'].encode(), logged_user.password.encode()):
            errors['password']="Incorrect Password"
        return errors
    
    def infoValidator(self, postDATA):
        errors={}
        if len(postDATA['title'])<3:
            errors['title']="Title must have more than 2 characters"
        if len(postDATA['desc'])<3:
            errors['desc']="Description must have more than 2 characters"
        if len(postDATA['location'])<3:
            errors['location']="Location must be have more than 2 characters"
        return errors
    
    def editValidator(self, postDATA):
        errors={}
        if len(postDATA['title'])<3:
            errors['title']="Title must have more than 2 characters"
        if len(postDATA['desc'])<3:
            errors['desc']="Description must have more than 2 characters"
        if len(postDATA['location'])<3:
            errors['location']="Location must be have more than 2 characters"
        return errors

class User(models.Model):
     first = models.CharField(max_length=45)
     last = models.CharField(max_length=45)
     email = models.CharField(max_length=45)
     password=models.TextField()
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)
     objects = Manager()

class Job(models.Model):
    title = models.CharField(max_length=45)
    location = models.CharField(max_length=100)
    desc = models.TextField()
    category = models.TextField()
    creator = models.ForeignKey(User, related_name='jobs_created', on_delete=models.CASCADE)
    employee = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)