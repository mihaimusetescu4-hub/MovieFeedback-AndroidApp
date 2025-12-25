from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudioViewSet,
    RegizorViewSet,
    ActorViewSet,
    GenViewSet,
    UtilizatorViewSet,
    FilmViewSet,
    FeedbackViewSet,
    FilmActorViewSet,
    FilmGenViewSet,
    FeedbackReactieViewSet,
)

router = DefaultRouter()

router.register(r'studio', StudioViewSet, basename='studio')
router.register(r'regizor', RegizorViewSet, basename='regizor')
router.register(r'actori', ActorViewSet, basename='actori')
router.register(r'gen', GenViewSet, basename='gen')
router.register(r'utilizatori', UtilizatorViewSet, basename='utilizator')
router.register(r'filme', FilmViewSet, basename='film')
router.register(r'feedback', FeedbackViewSet, basename='feedback')

router.register(r'film_actor', FilmActorViewSet, basename='film_actor')
router.register(r'film_gen', FilmGenViewSet, basename='film_gen')
router.register(r'feedback_reactie', FeedbackReactieViewSet, basename='feedback_reactie')

urlpatterns = [
    path('', include(router.urls)),
]