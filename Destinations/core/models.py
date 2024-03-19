from django.db import models

# Create your models here.

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.TextField()

class Session(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField(unique=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE)

class Destination(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    review = models.TextField()
    rating = models.IntegerField()
    share_publicly = models.BooleanField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)