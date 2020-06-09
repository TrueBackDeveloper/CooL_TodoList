from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=250, help_text='Username:')
    username = forms.EmailField(max_length=250, help_text='Email:')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2',)


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=250, help_text='Email:')

    class Meta:
        model = User
        fields = ('username', 'password',)


class ColorCheckForm(forms.Form):
    hex_color = forms.CharField(max_length=25)

    def clean_hex_color(self):
        color = str(self.cleaned_data['hex_color'])
        if len(color) < 7 or len(color) > 7:
            raise ValidationError('Invalid value')
        if color[0] != '#':
            raise ValidationError('Invalid value')
        for element in color:
            if not element in "#ABCDEFabcdef1234567890":
                raise ValidationError('Invalid value')

        return color
