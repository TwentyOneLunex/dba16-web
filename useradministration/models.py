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


class SensorStepCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_offset = models.IntegerField()
    count = models.SmallIntegerField()
    distance = models.FloatField()
    calorie = models.FloatField()
    speed = models.FloatField()
    sample_position_type = models.SmallIntegerField()


class SensorSleepStage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_offset = models.IntegerField()
    sleep_id = models.CharField(max_length=36)
    stage = models.SmallIntegerField()


class SensorSleep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_offset = models.IntegerField()


class SensorExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_offset = models.IntegerField()
    calorie = models.FloatField()
    duration = models.SmallIntegerField()
    exercise_type = models.SmallIntegerField()
    exercise_custom_type = models.CharField(max_length=255, null=True, blank=True)
    distance = models.FloatField()
    altitude_gain = models.FloatField()
    altitude_loss = models.FloatField()
    count = models.SmallIntegerField()
    count_type = models.SmallIntegerField()
    max_speed = models.FloatField()
    mean_speed = models.FloatField()
    max_caloricburn_rate = models.FloatField(null=True, blank=True)
    mean_caloricburn_rate = models.FloatField(null=True, blank=True)
    max_cadence = models.FloatField()
    mean_cadence = models.FloatField()
    max_heart_rate = models.FloatField(null=True, blank=True)
    mean_heart_rate = models.FloatField(null=True, blank=True)
    min_heart_rate = models.FloatField(null=True, blank=True)
    max_altitude = models.FloatField()
    mean_altitude = models.FloatField()
    incline_distance = models.FloatField()
    decline_distance = models.FloatField()
    max_power = models.FloatField(null=True, blank=True)
    mean_power = models.FloatField(null=True, blank=True)
    mean_rpm = models.FloatField(null=True, blank=True)
    location_data = models.CharField(max_length=255)


class SensorWaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    amount = models.FloatField()
    unit_amount = models.FloatField()


class SensorFoodIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    calorie = models.FloatField()
    food_info_id = models.CharField(max_length=48)
    amount = models.FloatField()
    unit = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    meal_type = models.IntegerField()


class SensorCaffeineIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    amount = models.FloatField()
    unit_amount = models.FloatField()


class SensorHeartRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_offset = models.IntegerField()
    heart_rate = models.FloatField()
    heart_beat_count = models.SmallIntegerField()


class SensorBodyTemperature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    temperature = models.FloatField()


class SensorBloodPressure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    systolic = models.FloatField()
    diastolic = models.FloatField()
    mean = models.FloatField()
    pulse = models.SmallIntegerField()


class SensorHbA1c(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    hba1c = models.FloatField()


class SensorBloodGlucose(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    glucose = models.FloatField()
    meal_time = models.DateTimeField()
    meal_type = models.SmallIntegerField()
    measurement_type = models.SmallIntegerField()
    sample_source_type = models.SmallIntegerField()


class SensorOxygenSaturation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_offset = models.IntegerField()
    spo2 = models.FloatField()
    heart_rate = models.FloatField()


class SensorAmbientTemperature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)


class SensorUvExposure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    time_offset = models.IntegerField()
    uv_index = models.FloatField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
