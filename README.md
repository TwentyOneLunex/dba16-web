**Project from the FH-Bielefeld in Germany**

First install a Postgresql-Database on your own Computer.
After that, you can start coding with Django.

The Setup for the server you can see in YourProject/polls/YourProject/settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangodb',
        'USER': 'djangouser',
        'PASSWORD': 'yourepw',
        'HOST': 'yourehost',
        'PORT': 'youreport',

    }
}
```
