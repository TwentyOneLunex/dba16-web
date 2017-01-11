**Project from the FH-Bielefeld in Germany**

For this you have to install Django on your enviroment.


First install a Postgresql-Database on your own Computer.
```
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```
Change to the User who was created by the commands before (postgres):
```
sudo su - postgres
```
Log into Postgres :
```
psql
```
Now you can create your Database (!dont forget the semikolon after each operation!):
```
CREATE DATABASE project;
```
Create a User:
```
CREATE USER myUser WITH PASSWORD 'MyPassword';
```
Make some Setups for speeding up operations:
```
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
```
Now the User needs access to your database:
```
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```
Back to the user's shell:
```
\q
exit
```
For the REST SERVICE DJANGO-RESTFRAMEWORK you need to install:
```
sudo pip install djangorestframework markdown django-filter
```
The django REST framework, markdown support for browsable API and filtering support

Add 'rest_framework' to your INSTALLED_APPS setting in settings.py.
```
INSTALLED_APPS = (
    ...
    'rest_framework',
)
```
If you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views. Add the following to your root urls.py file.
```
urlpatterns = [
    ...
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```
More Information on Django REST Framework:
http://www.django-rest-framework.org/

To avoid Crossiteskripting Conflicts install Django CORS Headers
```
pip install django-cors-headers
```
make some changest in settings.py:

add to intalled apps
```
INSTALLED_APPS = (
    ...
    'corsheaders',
    ...
)
```
add to middleware
```
MIDDLEWARE = [  # Or MIDDLEWARE_CLASSES on Django < 1.10
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
```
for now we allow all crossitescriptings
```
CORS_ORIGIN_ALLOW_ALL = True
```

After that, you can start coding with **Django**.

The Setup for the server you can see in YourProject/YourProject/settings.py.
In our case: dba16-web/wohlfuehlprojekt/settings.py.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project',
        'USER': 'myUser',
        'PASSWORD': 'myPassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

To start your server. Open another terminal and navigate to /etc/init.d/ and start your database with "./postgresql start".
With the command "psql -l" you can see your running databases.

Apply the migrations to your database.
Go into your Project (the "dba16-web" folder).
And set up the initial databse structure:
```
python manage.py makemigrations
python manage.py migrate
```
Create an administrative account:
```
python manage.py createsuperuser
```
Select a username,emailadress and password.
Test youre Server:
```
python manage.py runserver 127.0.0.1:8000
```
Visit your server in your web browser:
```
http://server_domain_or_IP:8000
```
Maybe : localhost:8000
