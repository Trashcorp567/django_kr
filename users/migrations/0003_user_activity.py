# Generated by Django 4.2.5 on 2023-10-11 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activity',
            field=models.BooleanField(default=True, verbose_name='статус'),
        ),
    ]
