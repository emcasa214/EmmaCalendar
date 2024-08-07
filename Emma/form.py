from django import forms
from .models import Task, User, Timers
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"myinput", "placeholder":"Enter Todo"}))
    class Meta:
        model = Task
        fields = ['title']

class Update(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completed']

class Setting(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email'] 

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm New Password"
    )

class PomodoroForm(forms.ModelForm):
    class Meta:
        model = Timers
        fields = ['title', 'hours', 'minutes', 'seconds', 'category', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'required': 'required'}),
            'hours': forms.NumberInput(attrs={'required': 'required'}),
            'minutes': forms.NumberInput(attrs={'required': 'required'}),
            'seconds': forms.NumberInput(attrs={'required': 'required'}),
            'category': forms.TextInput(attrs={'required': 'required'}),
            'priority': forms.NumberInput(attrs={'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('hours', 0)
        minutes = cleaned_data.get('minutes', 0)
        seconds = cleaned_data.get('seconds', 0)

        if hours < 0 or minutes < 0 or seconds < 0:
            raise forms.ValidationError("Hours, minutes, and seconds must be non-negative.")

        return cleaned_data