from django import forms

import re

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
    title = models.CharField(max_length=100)
    identifier = models.CharField(max_length=20, validator=[validate_identifier])
    abstract = models.TextField(max_length=1000)
    author = models.CharField(max_length=100)
    # will establish a separate model for paper subjects
    category = models.CharField(max_length=15)
    submitted = models.DateTimeField()
