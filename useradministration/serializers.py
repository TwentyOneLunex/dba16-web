from rest_framework import serializers
from useradministration.models import User, Question, Choice, UserAnswer, Location


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'age', 'gender')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text')


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('question', 'choice_imagePath')


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ('user', 'choice', 'date')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('pk', 'city', 'country_short')
