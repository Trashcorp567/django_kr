from django.contrib import admin

from main.models import Client, Message, Mailing, MailingLog


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'title', 'status', 'message', 'owner', 'get_client_names')

    def get_client_names(self, obj):
        return ", ".join([client.name for client in obj.clients.all()])

    get_client_names.short_description = 'Клиенты'


@admin.register(MailingLog)
class MailingLog(admin.ModelAdmin):
    list_display = ('attempt_time', 'attempt_status', 'server_response', 'mailing')
