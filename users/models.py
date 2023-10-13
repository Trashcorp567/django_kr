import hashlib
import datetime
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from config.settings import EMAIL_HOST_USER

NULLABLE = {'blank': True, 'null': True}

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='адрес')
    avatar = models.ImageField(upload_to='media/', verbose_name='аватар', **NULLABLE)
    activity = models.BooleanField(default=True, verbose_name='статус')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    verification_key = models.CharField(max_length=255, blank=True, null=True, verbose_name='ключ верификации')


    def send_registration_email(self):
        subject = 'Подтверждение регистрации'
        message = f'Регистрация пользователя {self.email} прошла успешно.'
        from_email = EMAIL_HOST_USER
        confirm_send = [self.email]

        send_mail(subject, message, from_email, confirm_send)

    def save(self, *args, **kwargs):

        is_new_user = not self.pk

        super().save(*args, **kwargs)

        if is_new_user:
            self.send_registration_email()
