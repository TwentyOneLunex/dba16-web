from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.SmallIntegerField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        return '%s %s %s %s %s' % (self.username, self.password, self.email, self.age, self.gender)

    def save_forRegView(self, *args, **kwargs):
        self.username = self.username.strip()
        self.password = self.password.strip()
        self.email = self.email.strip()
        self.age = self.age.strip()

        if self.username == '':
            raise ValueError("username must not be blank!")
        elif self.password == '':
            raise ValueError("password must not be blank!")
        elif self.email == '':
            raise ValueError("email must not be blank!")
        
        ageAsInt = 0
        try:
            ageAsInt = int(self.age)
        except:
            raise ValueError("age must be an integer value")

        if ageAsInt < 1 or ageAsInt > 110:
                raise ValueError("age has an unrealistic value!")
        elif self.gender != 'm' and self.gender != 'f':
            raise ValueError("field 'gender' has to be 'm' or 'f'")
        else:
            super(User, self).save(*args, **kwargs)
