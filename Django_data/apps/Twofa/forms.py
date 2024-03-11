from django import forms
from .models import UserTwoFA

import logging
logger = logging.getLogger(__name__)


class My_2fa(forms.ModelForm):
    class Meta:
        model = UserTwoFA
        fields = ('enable',)


class TwoFAForm(forms.ModelForm):
    otp = forms.CharField(required=True)

    class Meta:
        model = UserTwoFA
        fields = ('otp',)
