from django import forms

import re

from .validator import validate_identifier

arxiv_link_errors = {
    'invalid': '请填写arXiv地址。',
    'required':'一定要填。',
}

class ArXivLinkForm(forms.Form):

    arxiv_link = forms.CharField(
        label='arXiv link',
        max_length=60,
        widget=forms.TextInput(attrs={
                "class":"form-control", 
                "id":"arXiv-link",
            }),
        error_messages=arxiv_link_errors,
    )


class ArXivPaperForm(forms.Form):
    '''to do'''
    
    arxiv_link = forms.CharField(
        label='arXiv link',
        max_length=60,
        widget=forms.TextInput(attrs={
                "class":"form-control", 
                "id":"arXiv-link",
            }),
        error_messages=arxiv_link_errors,
    )
    title = forms.CharField(max_length=100)
    identifier = forms.CharField(max_length=20, validators=[validate_identifier])
    abstract = forms.CharField(max_length=1000)
    author = forms.CharField(max_length=100)
    # will establish a separate model for paper subjects
    category = forms.CharField(max_length=15)
    submitted = forms.DateTimeField()
