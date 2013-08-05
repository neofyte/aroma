import re

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import AromaUser

class SignInForm(forms.ModelForm):
    class Meta:
        model = AromaUser
        fields = ('email', 'password')
        label = {
            'email' : 'E-mail',
            'password' : 'Mima',
        }
        widgets = {
            'email': forms.TextInput(attrs={
                "class":"form-control", 
                "id":"sign-in-email",
            }),
            'password': forms.PasswordInput(attrs={
                "class":"form-control", 
                "id":"sign-in-password",
            }),
        }
        error_messages = {
            'username' : {
                'invalid': '这不可能是邮箱。',
                'required':'一定要填邮箱哦。',
            },
            'password' : {
                'required':'一定要填密码哦。',
            }
        }

    '''
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^[A-Za-z0-9]+$', username):
            raise forms.ValidationError('用户名只能用字母或数字。')
        return username
    '''


class SignUpForm(forms.ModelForm):
    class Meta:
        model = AromaUser
        fields = ('email', 'nickname', 'password')
        label = {
            'email' : 'E-mail',
            'nickname' : 'Username',
            'password' : 'Mima',
        }
        widgets = {
            'email': forms.TextInput(attrs={
                "class":"form-control", 
                "id":"sign-in-email",
            }),
            'nickname': forms.TextInput(attrs={
                "class":"form-control", 
                "id":"sign-in-nickname",
            }),
            'password': forms.PasswordInput(attrs={
                "class":"form-control", 
                "id":"sign-in-password",
            }),
        }
        error_messages = {
            'username' : {
                'invalid': '这不可能是邮箱。',
                'required': '一定要填邮箱哦。',
                'unique' : '邮箱已存在。',
            },
            'nickname' : {
                'invalid': '用户名。',
                'required':'一定要填。',
            },
            'password' : {
                'required':'一定要填密码哦。',
            }
        }

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if nickname != re.match('[\w\u2E80-\u9FFF]+', nickname).group(0):
            raise forms.ValidationError("Invalid nickname.")
        return nickname


