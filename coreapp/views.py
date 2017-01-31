from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from coreapp.models import *
from coreapp.serializers import *
import datetime


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def user_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete userdata.
    """
    try:
        users = User.objects.get(username=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(users)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(users, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        users.delete()
        return HttpResponse(status=204)


@csrf_exempt
def auth_check(request):
    try:
        data = JSONParser().parse(request)
        users = User.objects.get(username=data['username'])
    except User.DoesNotExist:
        content = {
            'authenticated': 'false'
        }
        return JSONResponse(content)

    if request.method == 'POST':

        if data['password'] == users.password:
            content = {
                'authenticated': 'true'
            }
            return JSONResponse(content)
        else:
            content = {
                'authenticated': 'false'
            }
        return JSONResponse(content)
    return HttpResponse(status=404)


#Die Funktion user_login prueft als erstes, ob es sich um einen reinen Aufruf
#der Webseite des Datenbankenanwendungen-Projektes handelt, oder ob auch Daten
#uebergeben werden. Ist Ersteres der Fall, wird zur Loginseite verwiesen, bzw.
#sofort zum Inhalt, sofern bereits eine Session-ID vorhanden ist.
#Bei Letzterem wird geprueft, ob der in der Loginseite uebergebene Nutzername
#in der Datenbank vorhanden ist und das Passwort mit dem gespeicherten Passwort
#uebereinstimmt.
#Ist dies der Fall, wird eine Session-ID gesetzt und zum Inhalt verwiesen.
def user_login(request):
    def reload(errorMsg):
        return render(request, 'coreapp/loginView.html', {
            'error_message': errorMsg,
            'username': request.POST['username'],
            'password': request.POST['password'],
        })
    if request.method == 'GET':
        if request.session.has_key('username'):
            return show_profile(request, request.session['username'])
        else:
            return render(request, 'coreapp/loginView.html')
    else:
        try:
            user_request_name = request.POST['username']
            user_request_password = request.POST['password']
            user_datensatz = User.objects.get(username=user_request_name)
        except:
            return reload('Username oder Passwort falsch.')
        if check_password(user_request_password, user_datensatz.password):
            request.session['username'] = user_datensatz.username
            return show_profile(request, user_datensatz.username)
        else:
            return reload('Username oder Passwort falsch.')


#Leitet den Nutzer zum Login weiter und löscht die aktuelle Session-ID.
def user_logout(request):
    def reload(errorMsg):
        return render(request, 'coreapp/loginView.html')
    try:
        if request.session.has_key('username'):
            del request.session['username']
            return reload('Sie wurden erfolgreich ausgeloggt.')
    except:
        pass


def show_profile(request, username):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    data = {
        'username': user.username,
        'email': user.email,
        'age': user.age,
        'gender': 'male' if user.gender == 'm' else 'female',
    }

    #if request.method == 'POST':
        #if request.POST['newpassword']:
     #       if request.POST['newpassword'] != request.POST['reppassword']:
       #         data['error_message'] = "wrong password repitition"
      #      else:
        #        user.password = request.POST['newpassword']
         #       try:
          #          user.save_forRegView()
           #         data['info_message'] = "password successfully changed :)"
           #     except ValueError as e:
           #         data['error_message'] = e
           #     except:
           #         data['error_message'] = "something went terribly wrong"

    if request.method == 'POST' and 'logout' in request.POST:
        return user_logout(request)

    return render(request, 'coreapp/myprofileView.html', data)

def registration_successful(request):
    return HttpResponse("<font color=\"green\">User was successfully registered :)</font>")


def show_user_registration_form(request):
    if request.method == 'GET':
        return render(request, 'coreapp/registrationView.html', {})
    elif request.method == 'POST':
        def reload(errorMsg):
            return render(request, 'coreapp/registrationView.html', {
                'error_message': errorMsg,
                'username': request.POST['username'],
                'password': request.POST['password'],
                'password_rep': request.POST['password_rep'],
                'email': request.POST['email'],
                'age': request.POST['age'],
            })

        try:
            data = request.POST
            newUser = User(username=data['username'],
                           password=data['password'],
                           email=data['email'],
                           age=data['age'],
                           gender=data['gender'])

            if newUser.password != data['password_rep']:
                return reload("password repetition incorrect")
            else:
                try:
                    newUser.password = make_password(newUser.password)
                    newUser.save_forRegView()
                    return HttpResponseRedirect(reverse('coreapp:reg_ok'))
                except ValueError as e:
                    return reload(e)
                except:
                    raise
        except:
            return reload("something went terribly wrong")


@csrf_exempt
def question_add(request):
    try:
        data = JSONParser().parse(request)
    except ValueError:
        content = {
            'successfull': 'false'
        }
        return JSONResponse(content)
    if request.method == 'POST':
        json_question_text = data['question_text']
        q = Question(question_text=json_question_text)
        q.save()

        json_question_text = data['choice_imagePath']
        for e in json_question_text:
            Choice(question=q, choice_imagePath=e).save()

        content = {
            'successfull': 'true'
        }
        return JSONResponse(content)
    return HttpResponse(status=404)


@csrf_exempt
def question_answer(request):
    try:
        data = JSONParser().parse(request)
    except ValueError:
        content = {
            'successfull': 'false'
        }
        return JSONResponse(content)
    if request.method == 'POST':
        user = User.objects.get(pk=data['user'])
        choice = Choice.objects.get(pk=data['choice'])
        UserAnswer(user=user, choice=choice).save()
        content = {
            'successfull': 'true'
        }
        return JSONResponse(content)
    return HttpResponse(status=404)


@csrf_exempt
def question_get(request):
    if request.method == 'GET':
        question = Question.objects.all()
        serializer = QuestionChoiceSerializer(question, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def location_add(request):
    try:
        data = JSONParser().parse(request)
    except ValueError:
        content = {
            'successfull': 'false'
        }
        return JSONResponse(content)
    if request.method == 'POST':
        Location(city=data['city'], country_short=data['country_short']).save()
        content = {
            'successfull': 'true'
        }
        return JSONResponse(content)
    return HttpResponse(status=404)


@csrf_exempt
def location_get(request):
    if request.method == 'GET':
        location = Location.objects.all()
        serializer = LocationSerializer(location, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def room_add(request, pk):
    try:
        data = JSONParser().parse(request)
    except ValueError:
        content = {
            'successful': 'false'
        }
        return JSONResponse(content)
    if request.method == 'POST':
        Room(location=Location.objects.get(pk=pk),
             identifier=data['identifier']).save()
        content = {
            'successful': 'true'
        }
        return JSONResponse(content)
    return HttpResponse(status=404)


@csrf_exempt
def location_room_get(request):
    if request.method == 'GET':
        location = Location.objects.all()
        serializer = LocationRoomSerializer(location, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def weather_add(request, pk):
    try:
        data = JSONParser().parse(request)
    except ValueError:
        content = {
            'successfull': 'false'
        }
        return JSONResponse(content)
    if request.method == 'POST':
        Weather(location=Location.objects.get(pk=pk),
                temperature=data['main']['temp'],
                pressure=data['main']['pressure'],
                humidity=data['main']['humidity'],
                windspeed=data['wind']['speed'],
                winddegree=data['wind']['deg']).save()
        content = {
            'successfull': 'true'
        }
        return JSONResponse(content)
    return HttpResponse(status=404)

  
@csrf_exempt
def sensordata_add(request, user):
    try:
        data = JSONParser().parse(request)
    except ValueError:
        content = {
            'successfull': 'false'
        }
        return JSONResponse(content)
    if request.method == 'POST':
        for e in data:
            starttime = datetime.datetime.fromtimestamp(int(e['START_TIME'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
            time_offset = e['TIME_OFFSET'] / 1000 / 60 / 60

            if e['TYPE'] == "StepCount":
                endtime = datetime.datetime.fromtimestamp(int(e['END_TIME'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
                SensorStepCount(user=User.objects.get(pk=user), end_time=endtime, start_time=starttime,
                                time_offset=time_offset, count=e['COUNT'], distance=e['DISTANCE'], calorie=e['CALORIE'],
                                speed=e['SPEED'], sample_position_type=e['SAMPLE_POSITION_TYPE']).save()
            elif e['TYPE'] == "SleepStage":
                endtime = datetime.datetime.fromtimestamp(int(e['END_TIME'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
                SensorSleepStage(user=User.objects.get(pk=user), start_time=starttime, end_time=endtime,
                                 time_offset=time_offset, sleep_id=e['SLEEP_ID'], stage=e['STAGE']).save()
            elif e['TYPE'] == "Sleep":
                endtime = datetime.datetime.fromtimestamp(int(e['END_TIME'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
                SensorSleep(user=User.objects.get(pk=user), start_time=starttime, end_time=endtime,
                            time_offset=time_offset).save()
            elif e['TYPE'] == "Exercise":
                endtime = datetime.datetime.fromtimestamp(int(e['END_TIME'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
                SensorExercise(user=User.objects.get(pk=user), start_time=starttime, end_time=endtime,
                               time_offset=time_offset, calorie=e['CALORIE'], duration=e['DURATION'],
                               exercise_type=e['EXERCISE_TYPE'], exercise_custom_type=e['EXERCISE_CUSTOM_TYPE'],
                               distance=e['DISTANCE'], altitude_gain=e['ALTITUDE_GAIN'],
                               altitude_loss=e['ALTITUDE_LOSS'], count=e['COUNT'],
                               count_type=e['COUNT_TYPE'], max_speed=e['MAX_SPEED'],
                               mean_speed=e['MEAN_SPEED'], max_caloricburn_rate=e['MAX_CALORICBURN_RATE'],
                               mean_caloricburn_rate=e['MEAN_CALORICBURN_RATE'], max_cadence=e['MAX_CADENCE'],
                               mean_cadence=e['MEAN_CADENCE'], max_heart_rate=e['MAX_HEART_RATE'],
                               mean_heart_rate=e['MEAN_HEART_RATE'], min_heart_rate=e['MIN_HEART_RATE'],
                               max_altitude=e['MAX_ALTITUDE'], mean_altitude=e['MEAN_ALTITUDE'],
                               incline_distance=e['INCLINE_DISTANCE'], decline_distance=e['DECLINE_DISTANCE'],
                               max_power=e['MAX_POWER'], mean_power=e['MEAN_POWER'], mean_rpm=e['MEAN_RPM'],
                               location_data=e['LOCATION_DATA']).save()
            elif e['TYPE'] == "WaterIntake":
                SensorWaterIntake(user=User.objects.get(pk=user), start_time=starttime, time_offset=time_offset,
                                  amount=e['AMOUNT'], unit_amount=
                                  e['UNIT_AMOUNT']).save()
            elif e['TYPE'] == "FoodIntake":
                SensorFoodIntake(user=User.objects.get(pk=user), start_time=starttime, time_offset=time_offset,
                                 calorie=e['CALORIE'], food_info_id=e['FOOD_INFO_ID'], amount=e['AMOUNT'],
                                 unit=e['UNIT'], name=e['NAME'], meal_type=e['MEAL_TYPE']).save()
            elif e['TYPE'] == "CaffeineIntake":
                SensorCaffeineIntake(user=User.objects.get(pk=user), start_time=starttime,
                                     time_offset=time_offset, amount=e['AMOUNT'], unit_amount=e['UNIT_AMOUNT']).save()
            elif e['TYPE'] == "HeartRate":
                endtime = datetime.datetime.fromtimestamp(int(e['END_TIME'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
                SensorHeartRate(user=User.objects.get(pk=user), start_time=starttime, end_time=endtime,
                                time_offset=time_offset, heart_rate=e['HEART_RATE'],
                                heart_beat_count=e['HEART_BEAT_COUNT']).save()
            elif e['TYPE'] == "BodyTemperature":
                SensorBodyTemperature(user=User.objects.get(pk=user), start_time=starttime,
                                      time_offset=time_offset, temperature=e['TEMPERATURE']).save()
            elif e['TYPE'] == "BloodPressure":
                SensorBloodPressure(user=User.objects.get(pk=user), start_time=starttime,
                                    time_offset=time_offset, systolic=e['SYSTOLIC'], diastolic=e['DIASTOLIC'],
                                    mean=e['MEAN'], pulse=e['PULSE']).save()
            elif e['TYPE'] == "BloodGlucose":
                mealtime = datetime.datetime.fromtimestamp(int(e['MEAL_TIME'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
                SensorBloodGlucose(user=User.objects.get(pk=user), start_time=starttime, time_offset=time_offset,
                                   glucose=e['GLUCOSE'], meal_time=mealtime, meal_type=e['MEAL_TYPE'],
                                   measurement_type=e['MEASUREMENT_TYPE'],
                                   sample_source_type=e['SAMPLE_SOURCE_TYPE']).save()
            elif e['TYPE'] == "OxygenSaturation":
                endtime = datetime.datetime.fromtimestamp(int(e['END_TIME'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')

                SensorOxygenSaturation(user=User.objects.get(pk=user), start_time=starttime, end_time=endtime,
                                       time_offset=time_offset, spo2=e['SPO2'], heart_rate=e['HEART_RATE']).save()
            elif e['TYPE'] == "HbA1c":
                SensorHbA1c(user=User.objects.get(pk=user), start_time=starttime, time_offset=time_offset,
                            hba1c=e['HBA1C']).save()
            elif e['TYPE'] == "AmbientTemperature":
                SensorAmbientTemperature(user=User.objects.get(pk=user), start_time=starttime,
                                         time_offset=time_offset, temperature=e['TEMPERATURE'], humidity=e['HUMIDITY'],
                                         latitude=e['LATITUDE'], longitude=e['LONGITUDE'], altitude=e['ALTITUDE'],
                                         accuracy=e['ACCURACY']).save()
            elif e['TYPE'] == "UvExposure":
                SensorUvExposure(user=User.objects.get(pk=user), start_time=starttime, time_offset=time_offset,
                                 uv_index=e['UV_INDEX'], latitude=e['LATITUDE'], longitude=e['LONGITUDE'],
                                 altitude=e['ALTITUDE'], accuracy=e['ACCURACY']).save()
        content = {
            'successfull': 'true'
        }
        return JSONResponse(content)
    return HttpResponse(status=404)


class TestPageView(TemplateView):

    template_name = "coreapp/bootstrap.html"

class ChartsPageView(TemplateView):

    template_name = "coreapp/charts.html"

class IndexPageView(TemplateView):

    template_name = "coreapp/index.html"

class HomePageView(TemplateView):

    template_name = "coreapp/home.html"

class MyprofilePageView(TemplateView):

    template_name = "coreapp/myprofileView.html"

class TablesPageView(TemplateView):

    template_name = "coreapp/tables.html"

