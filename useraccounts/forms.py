from django import forms
from django.contrib.auth.models import User
# # from django.contrib.auth.models import 





class LoginForm(forms.ModelForm):
    # username = forms.CharField(max_length=256, widget=forms.TextInput(), help_text="UserName     ::")
    email    = forms.CharField(max_length=256, widget=forms.EmailInput(), help_text="Email addr    ::")
    password = forms.CharField(max_length=256, widget=forms.PasswordInput(), help_text="Password    ::")
    # role     = forms.CharField(max_length=256, widget=forms.Select())

    class Meta:
        model  = User
        fields = ( 'email', 'password')
