from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    name= models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class Topic(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    room= models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=40)
    description=models.TextField(null=True, blank=True)
    participants=models.ManyToManyField(User,related_name='participants', blank=True)
    updated =models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    #returning the newest ones first
    class Meta:
        #- signifies descending order, i.e, newest values first
        ordering = ['created','updated']
    #returning all the data
    def __str__(self):
        return self.name

class Questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic= models.ForeignKey(Topic, on_delete=models.CASCADE)#Set_NULL for single deletion
    body=models.TextField()
    updated =models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        #- signifies descending order, i.e, newest values first
        ordering = ['created','updated']
    def __str__(self) -> str:
        return self.body[0:50]
