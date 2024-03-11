import pyotp
from .forms import My_2fa, TwoFAForm
from apps.Auth.models import User
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .models import UserTwoFA
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse


import logging
logger = logging.getLogger(__name__)


# __________________________________________________________________________ #
# _Create qrcode____________________________________________________________ #

def otp_setter(*, user):
    if hasattr(user, 'to2fa'):
        user.to2fa.otp_secret = pyotp.random_base32()
        user.save()
        return UserTwoFA.objects.get(user=user)


class create_qrcode(TemplateView):
    template_name = "setup_2fa.html"
    context: dict() = {}

    try:

        def post(self, request):
            logout(request)
            return redirect("/")

        def get(self, request):
            _user = request.user

            _user2fa = otp_setter(user=_user)
            otp_secret = _user2fa.otp_secret

            self.context["otp"] = otp_secret
            self.context["qr_code"] = _user.to2fa.generate_qr_code(
                name=_user.username
            )
            return render(request, self.template_name, context=self.context)

    except ValidationError as exc:
        context: dict() = {}
        context["form_errors"] = exc.messages


# __________________________________________________________________________ #
# _Enable 2fa_______________________________________________________________ #

def enable_2fa(request):
    _user = User.objects.get(username=request.user.username)
    profile_2fa = My_2fa(instance=_user.to2fa)
    if request.method == 'POST':
        profile_2fa = My_2fa(request.POST, instance=_user)
        if profile_2fa.is_valid():
            if _user.to2fa.enable:
                _user.to2fa.enable = False
                _user.save()
                return redirect('/')
            else:
                _user.to2fa.enable = True
                _user.save()
                return redirect('qrcode')
    return render(request, 'enable_2fa.html', {'profile_2fa': profile_2fa})


# __________________________________________________________________________ #
# _TwoFactorConfirmationView________________________________________________ #

class TwoFactorConfirmationView(FormView):
    template_name = "confirm_2fa.html"
    success_url = reverse_lazy("home")
    form = TwoFAForm()
    response: dict() = {}

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        key: str = ''
        self.form = TwoFAForm(request.POST)
        _user = User.objects.get(username=request.user.username)
        value = pyotp.TOTP(_user.to2fa.otp_secret).now()

        if self.form.is_valid():
            key = self.form.cleaned_data.get('otp')

        if key == value:
            self.response["success"] = True
            return JsonResponse(self.response)
        else:
            self.response["success"] = False
            self.response["logs"] = "Wrong 2fa code"
            return JsonResponse(self.response)
