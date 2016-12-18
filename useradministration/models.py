from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
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


class Question(models.Model):
    question_text = models.CharField(max_length=200)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_imagePath = models.CharField(max_length=200)


class UserAnswer(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, blank=True)
