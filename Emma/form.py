from django import forms
from .models import Task, User

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
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['name', 'email', 'password'] 
