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


class Location(models.Model):
    city = models.CharField(max_length=200)
    country_short = models.CharField(max_length=2)


class Room(models.Model):
    location = models.ForeignKey(Location, related_name='rooms', on_delete=models.CASCADE)
    identifier = models.CharField(max_length=200)


class Question(models.Model):
    question_text = models.CharField(max_length=200)


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_imagePath = models.CharField(max_length=200)


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, blank=True)


class Weather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    pressure = models.SmallIntegerField()
    humidity = models.SmallIntegerField()
    windspeed = models.DecimalField(max_digits=5, decimal_places=2)
    winddegree = models.SmallIntegerField()
    date = models.DateTimeField(auto_now=True, blank=True)


class Sensortype(models.Model):
    sensor = models.CharField(max_length=32)


class Sensordata(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensortype, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField() #0-32000
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()

