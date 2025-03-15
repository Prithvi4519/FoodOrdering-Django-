from django import forms
from .models import Queries

class QueryForm(forms.ModelForm):
    class Meta:
        model = Queries
        fields = ['name', 'mobile', 'email', 'message']
