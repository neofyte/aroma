from django import forms
from django.core.exceptions import ObjectDoesNotExist

import re

from .models import AromaUser

email_errors = {
    'invalid': '这不可能是邮箱。',
    'required':'一定要填邮箱哦。',
}
nickname_errors = {
    'invalid': 'username length',
    'required':'一定要填username哦。',
}
password_errors = {
    'required':'一定要填密码哦。',
}


class SignInForm(forms.Form):

    email = forms.EmailField(
        label='E-mail',
        max_length=60,
        widget=forms.TextInput(attrs={
                "class":"form-control", 
                "id":"sign-in-email",
            }),
        error_messages=email_errors,
    )
    password = forms.CharField(
        label='Mima',
        widget=forms.PasswordInput(attrs={
                "class":"form-control", 
                "id":"sign-in-password",
            }),
        error_messages=password_errors,
    )


class SignUpForm(forms.Form):

    email = forms.EmailField(
        label='E-mail',
        max_length=60,
        widget=forms.TextInput(attrs={
                "class":"form-control", 
                "id":"sign-in-email",
            }),
        error_messages=email_errors,
    )
    nickname = forms.CharField(
        label='username',
        max_length=20,
        widget=forms.TextInput(attrs={
                "class":"form-control", 
                "id":"sign-in-nickname",
            }),
        error_messages=nickname_errors,
    )
    password = forms.CharField(
        label='Mima',
        widget=forms.PasswordInput(attrs={
                "class":"form-control", 
                "id":"sign-in-password",
            }),
        error_messages=password_errors,
    )

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if nickname != re.match('[\w\u2E80-\u9FFF]+', nickname).group(0):
            raise forms.ValidationError("Invalid nickname.")
        return nickname

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            AromaUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('邮箱已存在。')


