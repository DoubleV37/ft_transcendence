from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SignInForm(forms.Form):
    username = forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={'placeholder':
                                          'Username'}),
            )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder':
                                              'Password'}),
            help_text=password_validation.password_validators_help_text_html(),
            )

#_____________________________________________________________________________#
#_MODIFICATION FORMS__________________________________________________________#
class InfoAvatar(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)

    def save(self, *args, **kwargs):
        self.avatar = self.cleaned_data['avatar']
        user = super().save(*args, **kwargs)


class InfoPsswd(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('password1',)


class InfoName(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)


class InfoMail(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)
