from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from main.models import Mailing, Client, Message
from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('title', 'start_time', 'end_time', 'message', 'period', 'status', 'clients')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MailingForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['message'].queryset = self.fields['message'].queryset.filter(owner=user)
            self.fields['clients'].queryset = self.fields['clients'].queryset.filter(owner=user)