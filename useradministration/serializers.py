from rest_framework import serializers
from useradministration.models import User, Question, Choice, UserAnswer, Location, Room


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'age', 'gender')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('pk', 'question_text')


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('pk', 'choice_imagePath')


class QuestionChoiceSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('pk', 'question_text', 'choices')


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ('user', 'choice', 'date')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('pk', 'city', 'country_short')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('pk', 'identifier')


class LocationRoomSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)

    class Meta:
        model = Location
        fields = ('pk', 'city', 'country_short', 'rooms')



