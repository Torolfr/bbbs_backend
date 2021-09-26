from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DiaryViewSet, ProfileViewSet

v1_router = DefaultRouter()

v1_router.register(r'profile/diaries', DiaryViewSet, basename='diary')


app_name = 'profile'

urlpatterns = [
    path('v1/', include((v1_router.urls, 'v1'))),
    path('v1/profile/', ProfileViewSet.as_view(), name='profile'),
]
