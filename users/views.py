import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class UserListView(ListView):
    model = User

    def get_queryset(self):
        return User.objects.filter(is_superuser=False, is_staff=False)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

@login_required
def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for i in range(12)])
    send_mail(
        subject='Смена пароля',
        message=f'Новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )

    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))


@login_required
def mailing_list_view(request):
    user = request.user
    is_manager = Group.objects.get(name='Менеджер') in user.groups.all()
    return render(request, 'main.base.html', {'is_manager': is_manager})


class DeactivateUserView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if user.is_active == True:
            user.is_active = False
            user.activity = False
            user.save()
        else:
            user.is_active = True
            user.activity = True
            user.save()

        return redirect('users:user_list')