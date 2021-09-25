from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

v1_router.register(r'articles', views.ArticleViewSet, basename='article')
v1_router.register(r'books', views.BookView, basename='book')
v1_router.register(r'catalog', views.CatalogView, basename='catalog')
v1_router.register(r'history', views.HistoryViewSet, basename='history')
v1_router.register(r'places/activity-types', views.ActivityTypeView, basename='activitytype')  # noqa (E501)
v1_router.register(r'places', views.PlacesViewSet, basename='place')
v1_router.register(r'tags', views.TagViewSet, basename='tag')
v1_router.register(r'rights', views.RightViewSet, basename='right')
v1_router.register(r'movies', views.MovieView, basename='movie')
v1_router.register(r'videos', views.VideoView, basename='video')
v1_router.register(r'questions', views.QuestionViewSet, basename='question')
v1_router.register(r'cities', views.CityViewSet, basename='city')
v1_router.register(r'profile/diaries', views.DiaryViewSet, basename='diary')
v1_router.register(r'afisha/events', views.EventViewSet, basename='event')
v1_router.register(r'afisha/event-participants/archive', views.MyEventsArchive, basename='my-events-archive')  # noqa (E501)
v1_router.register(r'afisha/event-participants', views.ParticipantViewSet, basename='event-participant')  # noqa (E501)
v1_router.register(r'search', views.SearchView, basename='global-search')


app_name = 'api'

urlpatterns = [
    path(
        'v1/main/',
        views.MainViewSet.as_view(), name='main'
    ),
    path(
        'v1/profile/',
        views.ProfileViewSet.as_view(), name='profile'
    ),
    path('v1/', include((v1_router.urls, 'v1'), namespace='v1')),
]
