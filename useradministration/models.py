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


class Questionary(models.Model):
    VERY_HAPPY = 1
    HAPPY = 2
    AVERAGE = 3
    UNHAPPY = 4
    VERY_UNHAPPY = 5
    FEELING_CHOICES = (
        (VERY_HAPPY, 'sehr glücklich'), (HAPPY, 'glücklch'), (AVERAGE, 'durchschnittlich'), (UNHAPPY, 'unglücklich'),
        (VERY_UNHAPPY, 'sehr unglücklich'))
    feeling = models.SmallIntegerField(choices=FEELING_CHOICES, default=AVERAGE)
    LECTURE = 1
    OTHERS = 2
    PRACTICAL_TRAINING = 3
    ACTIVITY_CHOICES = ((LECTURE, 'Vorlesung'), (OTHERS, 'Sonstiges'), (PRACTICAL_TRAINING, 'Praktikum'))
    activity = models.SmallIntegerField(choices=ACTIVITY_CHOICES, default=AVERAGE)
    VERY_LIGHT_CLOTH = 1
    LIGHT_CLOTH = 2
    WARM_CLOTH = 3
    VERY_WARM_CLOTH = 4
    CLOTHING_CHOICES = (
        (VERY_LIGHT_CLOTH, 'sehr leichte Kleidung'), (LIGHT_CLOTH, 'leiche Kleidung'), (WARM_CLOTH, 'warme Kleidung'),
        (VERY_WARM_CLOTH, 'sehr warme Kleidung'))
    clothing = models.SmallIntegerField(choices=CLOTHING_CHOICES, default=WARM_CLOTH)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
