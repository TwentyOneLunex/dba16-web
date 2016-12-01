from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.SmallIntegerField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        return '%s %s %s %s %s' % (self.username, self.password, self.email, self.age, self.gender)

    def save(self, *args, **kwargs):
        if self.gender != 'm' and self.gender != 'f':
            raise ValueError("field 'gender' has to be 'm' or 'f'")
        else:
            super(Blog, self).save(*args, **kwargs)
