# Generated by Django 3.2.3 on 2021-09-26 04:30

import common.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_alter_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Вид активности')),
            ],
            options={
                'verbose_name': 'Тип отдыха',
                'verbose_name_plural': 'Типы отдыха',
            },
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
                ('color', common.fields.ColorField(default='#FF0000', max_length=7, verbose_name='Цвет')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг (Ссылка)')),
            ],
            options={
                'verbose_name': 'Тип книг',
                'verbose_name_plural': 'Типы книг',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название региона')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('category', models.CharField(choices=[('Фильмы', 'Фильмы'), ('Куда пойти', 'Куда пойти'), ('Вопросы', 'Вопросы'), ('Права', 'Права'), ('Видеоролики', 'Видеоролики'), ('Календарь', 'Календарь')], max_length=50, verbose_name='Категория')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг (Ссылка)')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Теги с меньшим значением выводятся первыми.', verbose_name='Порядок вывода')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('category', 'order'),
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название города')),
                ('is_primary', models.BooleanField(default=False, help_text='Города с этой меткой будут отображаться в начале списка.', verbose_name='Приоритет вывода')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='common.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('-is_primary', 'name'),
            },
        ),
    ]
