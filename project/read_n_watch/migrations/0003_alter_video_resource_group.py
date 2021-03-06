# Generated by Django 3.2.3 on 2021-10-03 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_n_watch', '0002_auto_20211003_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='resource_group',
            field=models.BooleanField(default=False, help_text='Видео с этой меткой не будут показаны не авторизованным пользователям.', verbose_name='Ресурсная группа'),
        ),
    ]
