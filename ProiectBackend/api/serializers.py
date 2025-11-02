from rest_framework import serializers
from .models import *

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = "__all__"

class RegizorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regizor
        fields = "__all__"

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actori
        fields = "__all__"

class GenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gen
        fields = "__all__"

class UtilizatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizator
        fields = "__all__"

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filme
        fields = "__all__"

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

class FilmActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmActor
        fields = "__all__"

class FilmGenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmGen
        fields = "__all__"

class FeedbackReactieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackReactie
        fields = "__all__"
