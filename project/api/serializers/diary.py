from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import Diary


class DiarySerializer(serializers.ModelSerializer):
    mentor = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    date = serializers.DateField(default=now().date())
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )
    has_curator = serializers.BooleanField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Diary
        validators = [
            UniqueTogetherValidator(
                queryset=Diary.objects.all(),
                fields=['place', 'date', 'mentor'],
                message=_('Вы уже добавили дневник с такими данными'),
            )
        ]
