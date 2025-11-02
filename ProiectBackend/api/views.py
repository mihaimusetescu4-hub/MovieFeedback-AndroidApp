from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import *
from .serializers import *

class StudioViewSet(ReadOnlyModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

class RegizorViewSet(ReadOnlyModelViewSet):
    queryset = Regizor.objects.all()
    serializer_class = RegizorSerializer

class ActorViewSet(ReadOnlyModelViewSet):
    queryset = Actori.objects.all()
    serializer_class = ActorSerializer

class GenViewSet(ReadOnlyModelViewSet):
    queryset = Gen.objects.all()
    serializer_class = GenSerializer

class UtilizatorViewSet(ReadOnlyModelViewSet):
    queryset = Utilizator.objects.all()
    serializer_class = UtilizatorSerializer

class FilmViewSet(ReadOnlyModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmSerializer

class FeedbackViewSet(ReadOnlyModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class FilmActorViewSet(ReadOnlyModelViewSet):
    queryset = FilmActor.objects.all()
    serializer_class = FilmActorSerializer

class FilmGenViewSet(ReadOnlyModelViewSet):
    queryset = FilmGen.objects.all()
    serializer_class = FilmGenSerializer

class FeedbackReactieViewSet(ReadOnlyModelViewSet):
    queryset = FeedbackReactie.objects.all()
    serializer_class = FeedbackReactieSerializer
