from django import forms
from django.forms import ModelForm
from .models import * 

class StudentForms(ModelForm):
    class Meta: 
        model = CollageForm
        exclude = ('collage',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
        }