from django import forms
from .models import Disease, Folder

class DiseaseForm(forms.ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(), required=False)
    
    class Meta:
        model = Disease
        fields = '__all__'

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']
