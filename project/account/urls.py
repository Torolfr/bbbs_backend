from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenObtainPairView

app_name = 'account'

urlpatterns = [
    path(
        'v1/token/',
        CustomTokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(), name='token_refresh'
    ),
]
