from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthForm(forms.Form):
    email_errors = {
        'invalid': '这不可能是邮箱。',
        'required':'一定要填邮箱哦。',
    }
    password_errors = {
        'required':'一定要填密码哦。',
    }
    username = forms.EmailField(
        label='',
        max_length=60,
        widget=forms.TextInput(attrs={'placeholder': '邮箱', }),
        error_messages=email_errors,
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': '密码', }),
        error_messages=password_errors,
    )
    '''
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^[A-Za-z0-9]+$', username):
            raise forms.ValidationError('用户名只能用字母或数字。')
        return username
    '''
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('邮箱已存在。')