from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Case, When
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ..models import Diary
from ..permissions import IsOwner
from ..serializers import DiarySerializer


class DiaryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = DiarySerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Diary.objects.filter(
            mentor=self.request.user
        ).annotate(
            has_curator=Case(
                When(mentor__curator_id=None, then=False),
                default=True
            )
        ).order_by(
            '-date'
        )

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)

    @action(methods=['post'], detail=True)
    def send(self, request, pk=None):
        mentor = request.user
        diary = get_object_or_404(Diary, pk=pk, mentor=mentor)
        if not mentor.curator:
            message = {'diary': _('У вас нет куратора.')}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if diary.sent_to_curator:
            message = {
                'diary': _(
                    'Запись дневника уже была отправлена куратору ранее.'
                )
            }
            return Response(message, status=status.HTTP_200_OK)
        email = mentor.curator.email
        try:
            send_mail(
                subject=settings.SEND_DIARY_TO_CURATOR_SUBJECT % (
                    mentor,
                    diary.date.isoformat()
                ),
                message=diary.description,
                from_email=None,
                recipient_list=[email],
            )
        except SMTPException:
            message = {'diary': _('Проблемы с отправкой, попробуйте позднее.')}
            return Response(
                message,
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        diary.sent_to_curator = True
        diary.save()
        message = {'diary': _('Запись дневника отправлена куратору.')}
        return Response(message, status=status.HTTP_200_OK)
