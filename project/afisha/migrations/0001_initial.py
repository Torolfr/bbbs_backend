# Generated by Django 3.2.3 on 2021-09-26 04:41

import afisha.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.datetime
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0004_activitytype_booktype_city_region_tag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес мероприятия')),
                ('contact', models.CharField(max_length=200, verbose_name='Контактное лицо')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Контактный телефон')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(max_length=1000, verbose_name='Описание мероприятия')),
                ('start_at', models.DateTimeField(verbose_name='Время начала')),
                ('end_at', models.DateTimeField(verbose_name='Время окончания')),
                ('seats', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество мест')),
                ('canceled', models.BooleanField(default=False, help_text='События с этой меткой помечаются как "Отмененные", запись на них становится недоступной.', verbose_name='Отметка об отмене события')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='events', to='common.city', verbose_name='Город мероприятия')),
            ],
            options={
                'verbose_name': 'Календарь',
                'verbose_name_plural': 'Календарь',
                'ordering': ('start_at',),
                'permissions': (('events_in_all_cities', 'Можно смотреть события всех городов'),),
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='afisha.event', validators=[afisha.validators.event_lifetime_validator, afisha.validators.free_seats_validator, afisha.validators.event_canceled_validator])),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Запись на событие',
                'verbose_name_plural': 'Записи на события',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='EventMailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_sending', models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')),
                ('mailing_type', models.CharField(choices=[('cancellation', 'Отмена'), ('reminder', 'Напоминание')], max_length=12, verbose_name='Тип сообщения')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailings', to='afisha.event', verbose_name='Событие')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_mailings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рассылка уведомлений',
                'verbose_name_plural': 'Рассылки уведомлений',
                'ordering': ('-date_sending',),
            },
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events', through='afisha.Participant', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ForeignKey(limit_choices_to={'category': 'Календарь'}, on_delete=django.db.models.deletion.PROTECT, related_name='events', to='common.tag', verbose_name='Тег'),
        ),
        migrations.AddConstraint(
            model_name='participant',
            constraint=models.UniqueConstraint(fields=('event', 'participant'), name='event_participant_uniquetogether'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(django.db.models.functions.datetime.Extract('start_at', 'month'), name='event_start_at_month_index'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(django.db.models.functions.datetime.Extract('start_at', 'year'), name='event_start_at_year_index'),
        ),
    ]
