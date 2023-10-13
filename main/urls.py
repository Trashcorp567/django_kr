from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import MainConfig
from .views import MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, \
    ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView, MailingListView, \
    MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, MainView
from main.services import send_mailing

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(MainView.as_view()), name='home'),
    path('message_list', MessageListView.as_view(), name='message_list'),
    path('create', MessageCreateView.as_view(), name='message_create'),
    path('view/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('edit/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('client_view', ClientListView.as_view(), name='client_list'),
    path('client_create', ClientCreateView.as_view(), name='client_create'),
    path('client_detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_edit/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('mailings_view', MailingListView.as_view(), name='mailing_list'),
    path('mailing_create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/send/<int:pk>/', send_mailing, name='send')
]
