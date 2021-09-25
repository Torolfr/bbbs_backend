import time
from datetime import timedelta
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now
from django_cron import CronJobBase, Schedule

from afisha.models import EventMailing  # noqa (I001)
from .models import Participant


class EventCanceled(CronJobBase):
    RUN_EVERY_MINS = 10
    ALLOW_PARALLEL_RUNS = True
    MIN_NUM_FAILURES = 3
    FAILED_RUNS_CRONJOB_EMAIL_PREFIX = '[BBBS ошибка отправки]:'

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.event_canceled'

    def do(self):
        participants = Participant.objects.select_related(
            'event',
            'participant',
        ).filter(
            event__canceled=True,
            event__end_at__gt=now(),
        )
        for participant in participants:
            if not EventMailing.objects.filter(
                event=participant.event,
                user=participant.participant,
                mailing_type='cancellation',
            ).exists():
                try:
                    message = render_to_string(
                        'api/email_event_canceled.html',
                        {'event': participant.event},
                    )
                    send_mail(
                        subject=f'Уведомление об отмене события "{participant.event.title}"', # noqa (E501)
                        message=message,
                        from_email=None,
                        recipient_list=[participant.participant.email],
                        html_message=message,
                    )
                except SMTPException:
                    pass
                else:
                    EventMailing.objects.create(
                        event=participant.event,
                        user=participant.participant,
                        mailing_type='cancellation',
                    )
                    time.sleep(settings.EMAIL_SEND_TIMEOUT)


class EventReminder(CronJobBase):
    RUN_EVERY_MINS = 60
    ALLOW_PARALLEL_RUNS = True
    MIN_NUM_FAILURES = 3
    FAILED_RUNS_CRONJOB_EMAIL_PREFIX = '[BBBS ошибка отправки]:'

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.event_reminder'

    def do(self):
        participants = Participant.objects.select_related(
            'event',
            'participant',
        ).filter(
            event__start_at__gt=now(),
            event__start_at__lt=now() + timedelta(hours=24),
            event__canceled=False,
        )
        for participant in participants:
            if not EventMailing.objects.filter(
                event=participant.event,
                user=participant.participant,
                mailing_type='reminder',
            ).exists():
                try:
                    message = render_to_string(
                        'api/email_event_reminder.html',
                        {'event': participant.event},
                    )
                    send_mail(
                        subject='Напоминание о предстоящем событии',
                        message=message,
                        from_email=None,
                        recipient_list=[participant.participant.email],
                        html_message=message,
                    )
                except SMTPException:
                    pass
                else:
                    EventMailing.objects.create(
                        event=participant.event,
                        user=participant.participant,
                        mailing_type='reminder',
                    )
                    time.sleep(settings.EMAIL_SEND_TIMEOUT)
