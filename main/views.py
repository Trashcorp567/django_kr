from random import sample

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView

from blog.models import BlogPost
from main.models import Message, Client, Mailing, MailingLog
from users.forms import MailingForm
from users.models import User


class MainView(TemplateView):
    template_name = 'main/include/inc_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        unique_clients = User.objects.filter(is_staff=False).count()
        context['unique_clients'] = unique_clients

        active_mailings = Mailing.objects.filter(status='запущена').count()
        context['active_mailings'] = active_mailings

        all_mailing = Mailing.objects.all().count()
        context['all_mailing'] = all_mailing

        total_mailings = Mailing.objects.count()
        context['total_mailings'] = total_mailings

        if BlogPost.objects.count() >= 3:
            random_blog_posts = sample(list(BlogPost.objects.all()), 3)
        else:
            random_blog_posts = BlogPost.objects.all()
        context['random_blog_posts'] = random_blog_posts
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)

        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('title', 'body')
    success_url = reverse_lazy('main:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('title', 'body')
    success_url = reverse_lazy('main:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)

        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('name', 'email', 'commentary')
    success_url = reverse_lazy('main:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('name', 'email', 'commentary')
    success_url = reverse_lazy('main:client_list')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)

        return queryset

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailing_list')
