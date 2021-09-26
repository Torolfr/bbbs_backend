from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    HistoryViewSet,
    MainViewSet,
    PlacesViewSet,
    RightViewSet,
    QuestionViewSet,
    SearchView,
)
from common.views import ActivityTypeView

v1_router = DefaultRouter()

v1_router.register(r'history', HistoryViewSet, basename='history')
v1_router.register(r'places/activity-types', ActivityTypeView, basename='activitytype')  # noqa (E501)
v1_router.register(r'places', PlacesViewSet, basename='place')
v1_router.register(r'rights', RightViewSet, basename='right')
v1_router.register(r'questions', QuestionViewSet, basename='question')
v1_router.register(r'search', SearchView, basename='global-search')


app_name = 'main'

urlpatterns = [
    path('v1/main/', MainViewSet.as_view(), name='main'),
    path('v1/', include((v1_router.urls, 'v1'))),
]
