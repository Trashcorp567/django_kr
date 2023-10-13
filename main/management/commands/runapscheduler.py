import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from main.models import Mailing, MailingLog

logger = logging.getLogger(__name__)


def sendmails():
    # Получить все активные рассылки, подходящие по времени
    current_time = timezone.now()
    active_mailings = Mailing.objects.filter(status='запущена')

    # Перебрать активные рассылки и выполнить рассылку для каждой из них
    for mailing in active_mailings:
        if mailing.period == 'единожды':
            mail_recipients = mailing.clients.all()
            for recipient in mail_recipients:
                subject = mailing.message.title
                message = mailing.message.body
                from_email = settings.EMAIL_HOST_USER
                recipient_email = recipient.email

                try:
                    if current_time == last_sent_date:
                        send_mail(subject, message, from_email, [recipient_email])
                        MailingLog.objects.create(mailing=mailing, attempt_time=current_time,
                                                attempt_status='completed')
                    else:
                        send_mail(subject, message, from_email, [recipient_email])
                        MailingLog.objects.create(mailing=mailing, attempt_time=current_time,
                                                  attempt_status='active')


                except Exception as e:

                    error_message = str(e)
                    MailingLog.objects.create(
                        mailing=mailing, attempt_time=current_time, attempt_status='error',
                        server_response=error_message
                    )

        # Обновляем статус рассылки
            mailing.status = 'выполнено'
            mailing.save()

        elif mailing.start_time <= current_time <= mailing.end_time:
            if mailing.period == 'ежедневно':
                last_sent_date = mailing.last_sent_date
                current_date = current_time.date()
                # Проверяем, была ли уже отправка сегодня
                if last_sent_date == mailing.end_time:
                    mailing.status = 'выполнено'
                    mailing.save()

                elif last_sent_date is None or last_sent_date != current_date:
                    mail_recipients = mailing.clients.all()
                    for recipient in mail_recipients:
                        subject = mailing.message.title
                        message = mailing.message.body
                        from_email = settings.EMAIL_HOST_USER
                        recipient_email = recipient.email

                        try:
                            if current_time == last_sent_date:
                                send_mail(subject, message, from_email, [recipient_email])
                                MailingLog.objects.create(mailing=mailing, attempt_time=current_time,
                                                          attempt_status='completed')
                            else:
                                send_mail(subject, message, from_email, [recipient_email])
                                MailingLog.objects.create(mailing=mailing, attempt_time=current_time,
                                                          attempt_status='active')
                        except Exception as e:
                            # Обработка ошибок при отправке
                            error_message = str(e)
                            MailingLog.objects.create(
                                mailing=mailing, attempt_time=current_time, attempt_status='ошибка',
                                server_response=error_message
                            )

            elif mailing.period == 'еженедельно':
                # Проверяем, была ли уже отправка на этой неделе
                if mailing.last_sent_date is None or mailing.last_sent_date.isocalendar()[1] != current_time.isocalendar()[1]:
                    mail_recipients = mailing.clients.all()
                    for recipient in mail_recipients:
                        subject = mailing.message.title
                        message = mailing.message.body
                        from_email = settings.EMAIL_HOST_USER
                        recipient_email = recipient.email

                        try:
                            send_mail(subject, message, from_email, [recipient_email])
                            MailingLog.objects.create(mailing=mailing, attempt_time=current_time,
                                                      attempt_status='выполнено')
                            mailing.last_sent_date = current_time
                            mailing.save()
                        except Exception as e:
                            error_message = str(e)
                            MailingLog.objects.create(
                                mailing=mailing, attempt_time=current_time, attempt_status='ошибка',
                                server_response=error_message
                            )
                elif last_sent_date == mailing.end_time:
                    mailing.status = 'выполнено'
                    mailing.save()

            elif mailing.period == 'ежемесячно':
                if mailing.last_sent_date is None or mailing.last_sent_date.month != current_time.month:
                    mail_recipients = mailing.clients.all()
                    for recipient in mail_recipients:
                        subject = mailing.message.title
                        message = mailing.message.body
                        from_email = settings.EMAIL_HOST_USER
                        recipient_email = recipient.email

                        try:
                            # Отправляем письмо
                            send_mail(subject, message, from_email, [recipient_email])
                            # Создаем запись в логе рассылки
                            MailingLog.objects.create(mailing=mailing, attempt_time=current_time,
                                                      attempt_status='выполнено')
                            # Обновляем последнюю дату отправки в этом месяце
                            mailing.last_sent_date = current_time
                            mailing.save()
                        except Exception as e:
                            # Обработка ошибок при отправке
                            error_message = str(e)
                            MailingLog.objects.create(
                                mailing=mailing, attempt_time=current_time, attempt_status='ошибка',
                                server_response=error_message
                            )
                elif last_sent_date == mailing.end_time:
                    mailing.status = 'выполнено'
                    mailing.save()

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            sendmails,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="sendmails",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
