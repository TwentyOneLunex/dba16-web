from django.db import models

# Create your models here.
from django.db import models



class User(models.Model):
    email = models.EmailField(label ='New E-Mail', max_length = 50)
    username = models.charField(max_length=20)
    password = models.charField(widget=models.PasswordInput)



