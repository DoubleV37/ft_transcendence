import logging
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from .models import User



# Now you can use `hashed_password` to store in your database
logger = logging.getLogger(__name__)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 49:
            raise forms.ValidationError("Username is too long.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) > 319:
            raise forms.ValidationError("Email invalid.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        from .views import create_jwt
        user.refresh_token = make_password(create_jwt(user, "refresh"))
        if commit:
            user.save()
        return user


class SignInForm(forms.Form):
    username = forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
            help_text=password_validation.password_validators_help_text_html(),
    )

#_____________________________________________________________________________#
#_SETTINGS FORMS______________________________________________________________#
class My_Avatar(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        # If avatar is changed, delete the previous image
        if self.instance.avatar and self.instance.avatar != avatar:
            return avatar
        return self.instance.avatar
    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False)
        instance.avatar = self.cleaned_data['avatar']
        if commit:
            instance.save()
        return instance

class My_Psswd(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)
        labels = {
            "password": "Password",
        }
        widgets = {
            "password": forms.PasswordInput(attrs={
                    'placeholder':'********',
                    'autocomplete': 'off',
                    'data-toggle': 'password'}
                ),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class My_Tournamentname(forms.ModelForm):
    class Meta:
        model = User
        fields = ('tournament_name',)
    def clean_name(self):
        tournament_name = self.cleaned_data.get('tournament_name')
        if User.objects.filter(tournament_name=tournament_name).exists():
            raise forms.ValidationError("tournament_name is already taken.")
        return tournament_name

class My_Name(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class My_Mail(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
