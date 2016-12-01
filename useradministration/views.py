from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from useradministration.models import User
from useradministration.serializers import UserSerializer


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
    return HttpResponse("Benutzer wurde angelegt :)")


def show_user_registration_form(request):
    context = {}
    return render(request, 'useradministration/registrationView.html', context)


def create_user(request):
    try:
        newUser = User()
        newUser.username = request.POST['username']
        newUser.password = request.POST['password']
        newUser.email = request.POST['email']
        newUser.age = request.POST['age']
        newUser.gender = request.POST['gender']

        entry = Entry.objects.get(username=newUser.username)
        if not entry.exists():
            return render(request, 'useradministration/registrationView.html', {
                'error_message': "Dieser Benutzername existiert bereits!",
            })
        elif newUser.password != request.POST['password_rep']:
            return render(request, 'useradministration/registrationView.html', {
                'error_message': "Das Passwort wurde falsch wiederholt!",
            })
        else:
            newUser.save()
    except:
        return render(request, 'useradministration/registrationView.html', {
            'error_message': "Es wurden nicht alle Felder korrekt ausgefüllt!",
        })
    else:
        return HttpResponseRedirect(reverse('useradministration:reg_ok'))
