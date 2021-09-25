from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import City
from ..serializers import CitySerializer


class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all().order_by('-is_primary', 'name')
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    pagination_class = None
