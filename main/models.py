from django.db import models
from users.models import User, NULLABLE


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='ФИО')
    email = models.EmailField(unique=False, verbose_name='Контактный email')
    commentary = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец расслыки', **NULLABLE)

    def __str__(self):
        return f'{self.email}, ({self.name}) - {self.commentary}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец расслыки', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


class Mailing(models.Model):
    STATUS_CHOICES = [('создана', 'created'), ('запущена', 'active'), ('завершена', 'completed')]
    PERIOD_CHOICES = [('единожды', 'one_time'), ('ежедневно', 'daily'), ('еженедельно', 'weekly'),
                      ('ежемесячно', 'monthly')]
    start_time = models.DateTimeField(verbose_name='начало рассылки', **NULLABLE)
    end_time = models.DateTimeField(verbose_name='конец рассылки', **NULLABLE)
    title = models.CharField(max_length=150, verbose_name='название рассылки')
    last_sent_date = models.DateTimeField(verbose_name='отправлено в', **NULLABLE)
    period = models.CharField(max_length=15, choices=PERIOD_CHOICES, default='one', verbose_name='периодичность')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new', verbose_name='состояние')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='текст рассылки', **NULLABLE)
    clients = models.ManyToManyField(Client,  verbose_name='клиенты')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец расслыки', **NULLABLE)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(verbose_name='Дата и время попытки')
    attempt_status = models.CharField(max_length=20, verbose_name='Статус попытки')
    server_response = models.TextField(blank=True, verbose_name='Ответ почтового сервера')

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
