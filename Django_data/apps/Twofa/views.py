from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView, FormView

from .models import UserTwoFA
from .forms import My_2fa, TwoFAForm
from apps.Auth.models import User
from apps.Auth.forms import SignInForm

import pyotp

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
    template_name = 'Profile/enable_2fa.html'
    context = dict()

    try:
      def get(self, request):
        if "Load" not in request.headers:
          return redirect("/")
        _user = request.user

        _user2fa = otp_setter(user=_user)
        otp_secret = _user2fa.otp_secret

        self.context["otp"] = otp_secret
        self.context["qr_code"] = _user.to2fa.generate_qr_code(name=_user.username)
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
                return JsonResponse({'status': 'return'})
            _user.to2fa.enable = True
            _user.save()
            return JsonResponse({'status': 'continue'})
    if request.method == "GET":
      if "Load" not in request.headers:
        return redirect("/")
      return render(request, 'Profile/enable_2fa.html', {'profile_2fa': profile_2fa})


# __________________________________________________________________________ #
# _TwoFactorConfirmationView________________________________________________ #

class TwoFactorConfirmationView(FormView):
    template_name = "confirm_2fa.html"
    form = TwoFAForm()
    response = dict()

    def get(self, request):
      if "Load" not in request.headers:
        return redirect("/")
      if request.user.is_authenticated is True:
          _id = "confirm_2fa"
          _cancel = "cancel_2fa"
          _form = "form_2FA"
          _failure = "failure_2FA"
          _success = "success_2FA"
      else:
          _id = "code_2fa"
          _cancel = "cancel_code2fa"
          _form = "form_2FAcode"
          _failure = "failure_2FAcode"
          _success = "success_2FAcode"
      return render(request, 'Auth/confirm_2fa.html', {'form': self.form,
                                                        'div_ID': _id,
                                                        'cancel': _cancel,
                                                        'form_id': _form,
                                                        'success': _success,
                                                        'failure': _failure})

    def post(self, request):
        key: str = ''
        self.form = TwoFAForm(request.POST)
        _logged = True

        if request.user.is_anonymous is True:
            _logged = False
            signin_form = SignInForm(request.POST)
            if signin_form.is_valid():
                username = signin_form.cleaned_data['username']
                password = signin_form.cleaned_data['password']
                _user = authenticate(
                    request, username=username, password=password)
                if _user is None:
                    return JsonResponse({'success': False,
                                         'logs': 'Bad identificators'})
            else:
                return JsonResponse({'success': False,
                                     'logs': 'Bad identificators'})

        else:
            _user = User.objects.get(username=request.user.username)

        value = pyotp.TOTP(_user.to2fa.otp_secret).now()
        if self.form.is_valid():
            key = self.form.cleaned_data.get('otp')
            if key == value:

                self.response["success"] = True
                response = JsonResponse(self.response)
                if _logged is False:

                    login(request, _user)
                    from apps.Auth.views import create_jwt
                    jwt_token = create_jwt(_user)
                    response.set_cookie(key='jwt_token',
                                        value=str(jwt_token),
                                        httponly=True,
                                        secure=True,
                                        samesite='Lax')
                return response
            self.response["success"] = False
            self.response["logs"] = "Wrong 2fa code"
            return JsonResponse(self.response)
        self.response["success"] = False
        self.response["logs"] = "Something bad happend"
        return JsonResponse(self.response)
