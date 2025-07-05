from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = router.urls
