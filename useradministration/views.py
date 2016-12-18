from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from useradministration.models import User, Question, Choice, UserAnswer
from useradministration.serializers import UserSerializer
import json


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


def registration_successful(request):
    return HttpResponse("<font color=\"green\">User was successfully registered :)</font>")


def show_user_registration_form(request):
    if request.method == 'GET':
        return render(request, 'useradministration/registrationView.html', {})
    elif request.method == 'POST':
        def reload(errorMsg):
            return render(request, 'useradministration/registrationView.html', {
                'error_message': errorMsg,
                'username': request.POST['username'],
                'password': request.POST['password'],
                'password_rep': request.POST['password_rep'],
                'email': request.POST['email'],
                'age': request.POST['age'],
            })

        try:
            data = request.POST
            newUser = User(username = data['username'],
                           password = data['password'],
                           email = data['email'],
                           age = data['age'],
                           gender = data['gender'])

            if newUser.password != data['password_rep']:
                return reload("password was repeated wrongly")
            else:
                try:
                    newUser.save_forRegView()
                    return HttpResponseRedirect(reverse('useradministration:reg_ok'))
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
    content = "["

    first = 0;
    for q in Question.objects.all():
        if first != 0:
            content += "},"
        content += "{\"question_text\": \"" + q.question_text + "\","
        content += "\"choice_imagePath\": ["

        second = 0
        for c in Choice.objects.all():
            if c.question == q:
                if second != 0:
                    content += ","
                content += "{\"choice\": \"" + str(c.pk) + "\","
                content += "\"imagePath\": \"" + c.choice_imagePath + "\"}"
                second += 1

        content += "]"
        first += 1

    content += "}]"
    return JSONResponse(content)
