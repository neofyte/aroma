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
