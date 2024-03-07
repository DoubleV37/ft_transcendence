from django import forms
from .models import UserTwoFA

class My_2fa(forms.ModelForm):
    class Meta:
        model = UserTwoFA
        fields = ('enable',)



