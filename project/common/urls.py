from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CityViewSet, TagViewSet

v1_router = DefaultRouter()

v1_router.register(r'tags', TagViewSet, basename='tag')
v1_router.register(r'cities', CityViewSet, basename='city')


app_name = 'common'

urlpatterns = [
    path('v1/', include((v1_router.urls, 'v1'))),
]
