# Generated by Django 4.2.5 on 2023-10-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_mailing_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='last_sent_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='отправлено в'),
        ),
    ]
