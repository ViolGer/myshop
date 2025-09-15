from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={'placeholder': 'example@gmail.com', 'class': 'Input'}),
            'username': forms.TextInput(
                attrs={'placeholder': 'your username', 'class': 'Input'}),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'John', 'class': 'Input'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Doe', 'class': 'Input'}),
        }

        labels = {
            'email': 'Email',
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in ("password1", "password2"):
             self.fields[name].widget = forms.PasswordInput(attrs={"class": "form-control"})
             self.fields[name].help_text = ""
             self.fields[name].label = "Password" if name == "password1" else "Confirm Password"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self._meta.model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'example@gmail.com', 'class': 'Input'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'qwerty123', 'class': 'Input'}
    ))


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'username', 'email',
            'phone', 'image',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'Input'}),
            'last_name': forms.TextInput(attrs={'class': 'Input'}),
            'username': forms.TextInput(attrs={'class': 'Input'}),
            'email': forms.EmailInput(attrs={'class': 'Input'}),
            'phone': forms.TextInput(attrs={'class': 'Input'}),
            # ВАЖНО: обычный FileInput — без "Currently / Clear / Change"
            'image': forms.FileInput(attrs={'accept': 'image/*', 'id': 'id_avatar'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


