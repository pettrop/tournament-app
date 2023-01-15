from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.db.transaction import commit
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Input valid email address.', required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField()

    class Meta:
        model = Profile
        fields = ['phone']
