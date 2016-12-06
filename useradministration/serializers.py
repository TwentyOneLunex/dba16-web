from rest_framework import serializers
from useradministration.models import User, Questionary


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'age', 'gender')


class QuestionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionary
        fields = ('id', 'feeling', 'activity', 'clothing', 'user')
