from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    personal_number = forms.CharField(max_length=20, required=True)
    birth_date = forms.DateField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'full_name', 'personal_number', 'birth_date', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different email.")
        return email

    def clean_personal_number(self):
        personal_number = self.cleaned_data.get('personal_number')
        if CustomUser.objects.filter(personal_number=personal_number).exists():
            raise forms.ValidationError("This personal number is already in use. Please use different personal number.")
        return personal_number
