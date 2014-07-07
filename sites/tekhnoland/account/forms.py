# coding=utf-8
import re
from django import forms
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from ..catalog.model_choices import EXPORT_STATE_CHANGED
from .models import Registration, CustomerProfile
from .email import send_password_reset_email

attrs_dict = {'class': 'required'}

USERNAME_REGEXP = re.compile(r'[a-zA-Z0-9@\.\+\-_]+')

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict), label=u"Пароль", help_text=u"Обязательное.")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict), label=u"Пароль ещё раз", help_text=u"Обязательное.")

    class Meta:
        model = Registration
        fields = ('username', 'password1', 'password2', 'username1c', 'last_name', 'first_name', 'father_name',
            'email', 'phone', 'city', 'address', 'delivery', 'source', )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(USERNAME_REGEXP, username):
            raise forms.ValidationError(u"В имени пользователя нельзя использовать кириллицу, только латинские буквы.")
        user_count = User.objects.filter(username__iexact=username).count()
        registration_count = Registration.objects.filter(username__iexact=username).count()
        if user_count + registration_count == 0:
            return username
        raise forms.ValidationError(u"Пользователь с таким именем уже существует.")

    def clean_username1c(self):
        username1c = self.cleaned_data['username1c']
        profile_count = CustomerProfile.objects.filter(username1c__iexact=username1c).count()
        registration_count = Registration.objects.filter(username1c__iexact=username1c).count()
        if profile_count + registration_count == 0:
            return username1c
        raise forms.ValidationError(u"Пользователь с таким именем 1С уже существует.")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u"Введённые пароли не совпадают.")
            self.instance.password = make_password(self.cleaned_data['password1'])
        return self.cleaned_data


class PasswordResetFormHtml(PasswordResetForm):

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        for user in self.users_cache:
            send_password_reset_email(request, user, email_template_name, token_generator)


class CustomerProfileForm(forms.ModelForm):
    username = forms.CharField(label=u"Логин", max_length=30)
    email = forms.EmailField(label=u"E-mail")
    #first_name = forms.CharField(label=u"Имя", max_length=30)
    #last_name = forms.CharField(label=u"Фамилия", max_length=30)

    class Meta:
        model = CustomerProfile
        fields = ('username', #'last_name', 'first_name', 'father_name',
                  'email', 'phone', 'city', 'address', 'delivery', )

    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email
        #self.fields['first_name'].initial = self.instance.user.first_name
        #self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        self.instance.export_state = EXPORT_STATE_CHANGED

        super(CustomerProfileForm, self).save(commit=commit)

        self.instance.user.username = self.cleaned_data.get('username')
        self.instance.user.email = self.cleaned_data.get('email')
        #self.instance.user.first_name = self.cleaned_data.get('first_name')
        #self.instance.user.last_name = self.cleaned_data.get('last_name')
        if commit:
            self.instance.user.save()
        return self.instance
