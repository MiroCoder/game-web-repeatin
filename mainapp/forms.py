from collections import Counter
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ProfileModel
from django.contrib.auth.models import User
from django.db.models import Case, When

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=255, label='ФИО')
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)), label='Дата рождения', required=False)
    location = forms.CharField(max_length=30, label='Адрес', required=False)
    gender = forms.ChoiceField(choices=ProfileModel.GENDER_CHOICES, label='Пол', required=False)
    contact_number = forms.CharField(max_length=20, label='Контактный номер', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'full_name', 'birth_date', 'location', 'gender', 'contact_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        profile = ProfileModel.objects.create(
            user=user,
            full_name=self.cleaned_data['full_name'],
            birth_date=self.cleaned_data['birth_date'],
            location=self.cleaned_data['location'],
            gender=self.cleaned_data['gender'],
            contact_number=self.cleaned_data['contact_number']
        )
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField(label='User name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

