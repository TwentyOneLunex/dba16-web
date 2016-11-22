from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    birth_date = models.DateField()
    gender = models.BooleanField() # True=>male, False=>female

    def __str__(self):
        return '%s %s %s %s %s' % (self.username, self.password, self.email, self.birth_date, self.gender)
