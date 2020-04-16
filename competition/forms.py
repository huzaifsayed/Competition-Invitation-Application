from django import forms 
from .models import CompetitionUser

class CompetitionForm(forms.ModelForm): 
    class Meta: 
        model = CompetitionUser 
        fields = ['first_name', 'last_name', 'mobile', 'email'] 