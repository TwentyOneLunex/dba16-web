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
After that, you can start coding with **Django**.

The Setup for the server you can see in YourProject/YourProject/settings.py.
In our case: dba16-web/wohlfühlprojekt/settings.py.

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
Apply the migrations to your database.
Go into your Project (the "dba16-web" folder).
Setting up the initial databse structure:
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
python manage.py runserver 0.0.0.0:8000
```
Visit your server in your web browser:
```
http://server_domain_or_IP:8000
```
Maybe : localhost:8000
