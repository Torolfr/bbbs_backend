from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, MyEventsArchive, ParticipantViewSet

v1_router = DefaultRouter()

v1_router.register(r'events', EventViewSet, basename='event')
v1_router.register(r'event-participants/archive', MyEventsArchive, basename='my-events-archive')  # noqa (E501)
v1_router.register(r'event-participants', ParticipantViewSet, basename='event-participant')  # noqa (E501)


app_name = 'afisha'

urlpatterns = [
    path('v1/afisha/', include((v1_router.urls, 'v1'))),
]
