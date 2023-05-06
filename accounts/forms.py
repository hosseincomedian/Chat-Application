from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='', min_length=2, max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'User name'}))
    password1 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    photo = forms.ImageField(label='', required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'photo']

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = CustomUser.objects.filter(username=username)
        if new.count():
            raise ValidationError("Username Already Exist")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match!!")
        return password2

    def save(self, commit=True):
        print(self.cleaned_data)
        if self.cleaned_data['photo']:
            user = CustomUser.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password1'],
                photo=self.cleaned_data['photo']
            )
        else:
            user = CustomUser.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password1']
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='', min_length=2, max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'User name'}))
    password = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
