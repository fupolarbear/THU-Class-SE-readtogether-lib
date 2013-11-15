from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField()
    password2 = forms.CharField()
    email = forms.EmailField()
    name = forms.CharField(max_length=100)
