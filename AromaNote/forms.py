from django.forms import ModelForm, Textarea
from AromaNote.models import AromaNote

class AromaNoteForm(ModelForm):
    class Meta:
        model = AromaNote
        fields = ('content', 'title')
        widgets = {
            'content': Textarea(attrs={
                "class":"form-control", 
                "id":"inputPanel",
            }),
        }
    
