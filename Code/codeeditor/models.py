# codeeditor/models.py
from django.db import models
from django.contrib.auth.models import User

class UserCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    code = models.TextField()
    output = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.language}'
from django.db import models

# Create your models here.
