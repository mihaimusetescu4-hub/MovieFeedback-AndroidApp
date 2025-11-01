from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'studio', StudioViewSet)
router.register(r'regizor', RegizorViewSet)
router.register(r'actori', ActorViewSet)
router.register(r'gen', GenViewSet)
router.register(r'utilizator', UtilizatorViewSet)
router.register(r'filme', FilmViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'film_actor', FilmActorViewSet)
router.register(r'film_gen', FilmGenViewSet)
router.register(r'feedback_reactie', FeedbackReactieViewSet)

urlpatterns = router.urls
