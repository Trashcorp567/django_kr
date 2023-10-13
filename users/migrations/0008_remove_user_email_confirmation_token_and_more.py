# Generated by Django 4.2.5 on 2023-10-13 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_email_confirmation_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_confirmation_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email_confirmed',
        ),
        migrations.AddField(
            model_name='user',
            name='verification_key',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ключ верификации'),
        ),
    ]
