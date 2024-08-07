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
    
class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Old Password", required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="New Password", required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm New Password", required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # Check if the username exists and the old password is correct
        try:
            user = User.objects.get(username=username)
            if not user.check_password(old_password):
                raise forms.ValidationError("Old password is incorrect")
        except User.DoesNotExist:
            raise forms.ValidationError("Username does not exist")

        # Check if the new passwords match
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("The new passwords do not match")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        user = User.objects.get(username=cleaned_data["username"])
        user.set_password(cleaned_data["new_password1"])
        user.save()

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