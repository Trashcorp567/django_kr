from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from main.models import Mailing, MailingLog
from django.core.mail import send_mail
from config import settings

app_name = 'main'


def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mail_recipients = mailing.clients.all()

    for recipient in mail_recipients:
        current_time = timezone.now()
        subject = mailing.message.title
        message = mailing.message.body
        from_email = settings.EMAIL_HOST_USER
        recipient_email = recipient.email

        send_mail(subject, message, from_email, [recipient_email])
        MailingLog.objects.create(mailing=mailing, attempt_time=current_time, attempt_status='completed')
        mailing.status = 'завершена'
        mailing.save()
    return HttpResponse("Рассылка успешно завершена.")
