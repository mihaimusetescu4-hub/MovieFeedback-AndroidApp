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
        exclude = ['parola_hash']

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

class FeedbackSerializer(serializers.ModelSerializer):
    utilizator = UtilizatorSerializer(source='id_utilizator', read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'


class FilmDetailSerializer(serializers.ModelSerializer):
    studio = StudioSerializer(source='id_studio', read_only=True)
    regizor = RegizorSerializer(source='id_regizor', read_only=True)
    actori = serializers.SerializerMethodField()
    genuri = serializers.SerializerMethodField()
    feedbackuri = serializers.SerializerMethodField()

    class Meta:
        model = Filme
        fields = '__all__'
        depth = 1  # opțional, pentru a include FK-urile simple

    def get_actori(self, obj):
        legaturi = FilmActor.objects.filter(id_film=obj.id_film)
        actori = [leg.id_actor for leg in legaturi]
        return ActorSerializer(actori, many=True).data

    def get_genuri(self, obj):
        legaturi = FilmGen.objects.filter(id_film=obj.id_film)
        genuri = [leg.id_gen for leg in legaturi]
        return GenSerializer(genuri, many=True).data

    def get_feedbackuri(self, obj):
        feedbackuri = Feedback.objects.filter(id_film=obj.id_film)
        return FeedbackSerializer(feedbackuri, many=True).data