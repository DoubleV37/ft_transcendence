from django import forms
from .models import UserTwoFA

class My_2fa(forms.ModelForm):
    class Meta:
        model = UserTwoFA
        fields = ('enable',)


class TwoFAForm(forms.ModelForm):
    otp = forms.CharField(required=True)

    class Meta:
        model = UserTwoFA
        fields = ('otp',)

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not self.instance.validate_otp(otp):
            raise ValidationError('Invalid 2FA code.')

    # def get_form_class(self):
    #     return self.Form

    # def get_form(self, *args, **kwargs):
    #     form = super().get_form(*args, **kwargs)
    #
    #     form.user = self.request.user
    #
    #     return form

    # def form_valid(self, form):
    #     return super().form_valid(form)


    # def clean_otp(self):
    #     self.two_factor_auth_data = UserTwoFactorAuthData.objects.filter(
    #         user=self.user
    #     ).first()
    #
    #     if self.two_factor_auth_data is None:
    #         raise ValidationError('2FA not set up.')
    #
    #     otp = self.cleaned_data.get('otp')
    #
    #     if not self.two_factor_auth_data.validate_otp(otp):
    #         raise ValidationError('Invalid 2FA code.')
    #
    #     return otp
    #
