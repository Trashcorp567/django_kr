# Generated by Django 4.2.5 on 2023-10-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='period',
            field=models.CharField(choices=[('единожды', 'one_time'), ('ежедневно', 'daily'), ('еженедельно', 'weekly'), ('ежемесячно', 'monthly')], default='one', max_length=15, verbose_name='периодичность'),
        ),
    ]
