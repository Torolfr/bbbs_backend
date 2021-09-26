from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

v1_router.register(r'articles', views.ArticleViewSet, basename='article')
v1_router.register(r'books', views.BookView, basename='book')
v1_router.register(r'catalog', views.CatalogView, basename='catalog')
v1_router.register(r'movies', views.MovieView, basename='movie')
v1_router.register(r'videos', views.VideoView, basename='video')


app_name = 'read_n_watch'

urlpatterns = [
    path('v1/', include((v1_router.urls, 'v1'))),
]
