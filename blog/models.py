from django.db import models

from users.models import NULLABLE


# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='media/', verbose_name='Превью', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'