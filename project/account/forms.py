from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm, UsernameField
from django.core.mail import send_mail
from django.forms import EmailField

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True # noqa E501

    def save(self, commit=True):
        """Save the new user and send mail to user with login and password"""
        user = super().save(commit=False)
        password = User.objects.make_random_password()
        email = self.cleaned_data['email']
        login = self.cleaned_data['username']
        user.set_password(password)
        send_mail(
            subject=settings.USER_CREATION_SUBJECT,
            message=settings.USER_CREATION_MESSAGE % (login, password),
            from_email=None,
            recipient_list=[email],
            fail_silently=True
        )
        if commit:
            user.save()
        return user


class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):

    def save(self, commit=True):
        """Save the new password and send mail to user with the new password"""
        password = self.cleaned_data['password1']
        self.user.set_password(password)
        User.email_user(
            self.user,
            subject=settings.USER_PASSWORD_CHANGE_SUBJECT,
            message=settings.USER_PASSWORD_CHANGE_MESSAGE % password,
            fail_silently=True
        )
        if commit:
            self.user.save()
        return self.user
