from django import forms
from django.forms import ModelForm
from .models import * 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

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

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Passowrd'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']



# class UserForm(ModelForm):
#     class Meta: 
#         model = User
#         exclude = ('username',)
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
            
#         }