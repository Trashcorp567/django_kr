import random
import secrets

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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

    def form_valid(self, form):
        new_user = form.save()
        new_user.verification_key = secrets.randbelow(1_000_000)
        new_user.save()

        token = urlsafe_base64_encode(force_bytes(new_user.verification_key))
        verification_url = reverse('users:verify', kwargs={'token': token})
        send_mail(
            subject='Перейдите по ссылки которая придет к вам на почту.',
            message=f'Для подтвердения регистрации, пройдите по ссылке ниже в письме. \n {self.request.build_absolute_uri(verification_url)}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)

def verify_email(request, token):
    try:
        user_verification_key = urlsafe_base64_decode(token).decode()
        user = User.objects.get(verification_key=user_verification_key)
        if int(user_verification_key) == int(user.verification_key):
            user.is_active = True
            user.save()
            return redirect('users:login')
        else:
            return HttpResponse("Ошибка верификации аккаунта.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Ошибка верификации аккаунта.")


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

