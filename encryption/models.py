from django.db import models
from datetime import datetime


# Creating user model here
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    photo = models.CharField(max_length=1000)
    createdAt = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

# creating encrypted data model here


class Encrypted_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret_message = models.CharField(max_length=500)
    public_key = models.CharField(max_length=5000)
    private_key = models.CharField(max_length=5000)
    encrypted_file = models.CharField(max_length=2000)
    createdAt = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user
