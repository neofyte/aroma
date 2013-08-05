from django import forms
from AromaNote.models import AromaNote

class AromaNoteForm(forms.ModelForm):
    class Meta:
        model = AromaNote
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={
                "class":"form-control", 
                "id":"title-panel",
            }),
            'content': forms.Textarea(attrs={
                "class":"form-control", 
                "id":"inputPanel",
                "resize":"none",
            }),
        }
    
