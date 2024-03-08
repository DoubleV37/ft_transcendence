import pyotp
from .forms import My_2fa, TwoFAForm
from apps.Auth.models import User
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .serializers import UserTwoFASerializer
from .models import UserTwoFA
from django.shortcuts import render, redirect

from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import logout, authenticate, login

from django.http import HttpResponse

# from django.core.mail import send_mail

import logging
logger = logging.getLogger(__name__)

# from rest_framework import status, generics
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response


#
#
# def generate_random_digits(n=6):
#     return "".join(map(str, random.sample(range(0, 10), n)))
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def twofa_login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#
#     user = authenticate(request, username=username, password=password)
#
#     if user is not None:
#         # User credentials are valid, proceed with code generation and email sending
#         user_profile = UserTwoFA.objects.get(user=user)
#
#         # Generate a 6-digit code and set the expiry time to 1 hour from now
#         verification_code = generate_random_digits
#         user_profile.otp = verification_code
#         user_profile.otp_expiry_time = timezone.now() + timedelta(hours=1)
#         user_profile.save()
#
#         # Send the code via email (use Django's send_mail function)
#         send_mail(
#             'Verification Code',
#             f'Your verification code is: {otp}',
#             'from@example.com',
#             [email],
#             fail_silently=False,
#         )
#
#         return Response({'detail': 'Verification code sent successfully.'}, status=status.HTTP_200_OK)
#
#     return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def twofa_verify(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#     otp = request.data.get('otp')
#
#     user = authenticate(request, email=email, password=password)
#
#     if user is not None:
#         user_profile = UserTwoFA.objects.get(user=user)
#
#         # Check if the verification code is valid and not expired
#         if (
#             user_profile.verification_code == otp and
#             user_profile.otp_expiry_time is not None and
#             user_profile.otp_expiry_time > timezone.now()
#         ):
#             # Verification successful, generate access and refresh tokens
#             django_login(request, user)
#             # Implement your token generation logic here
#
#             # Use djangorestframework_simplejwt to generate tokens
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#
#             # Reset verification code and expiry time
#             user_profile.otp = ''
#             user_profile.otp_expiry_time = None
#             user_profile.save()
#
#             return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
#
#     return Response({'detail': 'Invalid verification code or credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


def user_two_factor_set(*, user):
    if hasattr(user, 'to2fa'):
        user.to2fa.otp = pyotp.random_base32()
        user.save()
        return UserTwoFA.objects.get(user=user)

    # two_factor_auth_data = UserTwoFA.objects.create(
    #     user=user,
    #     otp=pyotp.random_base32()
    # )
    #
    # return two_factor_auth_data

# return user.to2fa

    # user.to2fa.otp = pyotp.random_base32()
    # user.save()
    # return UserTwoFA.objects.get(user=user)


class create_qrcode(TemplateView):
    template_name = "setup_2fa.html"
    context: dict() = {}

    try:

        def post(self, request):
            logout(request)
            return self.render_to_response(self.context)

        def get(self, request):
            _user = request.user

            _user2fa = user_two_factor_set(user=_user)
            otp_secret = _user2fa.otp

            self.context["otp"] = otp_secret
            self.context["qr_code"] = _user.to2fa.generate_qr_code(
                name=_user.username
            )
            return render(request, self.template_name, context=self.context)

    except ValidationError as exc:
        context: dict() = {}
        context["form_errors"] = exc.messages


def enable_2fa(request):
    _user = User.objects.get(username=request.user.username)
    profile_2fa = My_2fa(instance=_user.to2fa)
    if request.method == 'POST':
        profile_2fa = My_2fa(request.POST, instance=_user)
        if profile_2fa.is_valid():
            if _user.to2fa.enable:
                _user.to2fa.enable = False
            else:
                _user.to2fa.enable = True
            _user.save()
            return redirect('qrcode')
            # return HttpResponse('<h1>Success</h1>')
    return render(request, 'enable_2fa.html', {'profile_2fa': profile_2fa})


class TwoFactorConfirmationView(FormView):
    template_name = "confirm_2fa.html"
    success_url = reverse_lazy("home")
    form = TwoFAForm()

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):

        _user = User.objects.get(username=request.user.username)
        logger.info(f'{"":_<10}{_user.username = }{"":_>10}')
        logger.info(f'{_user.to2fa.enable = }')
        logger.info(f'{_user.to2fa.otp = }')
        logger.info(f"{'request.POST':_^20}")
        logger.info(f'{self.form =}')

        if self.form.clean_otp:
            return HttpResponse('<h1>Ouai</h1>')
        else:
            return HttpResponse('<h1>Nooon</h1>')

        if self.form.is_valid():
            logger.info(f"{'is_valid = true':#^20}")
            self.form.clean_otp
            return render(request, self.success_url)
        else:
            # logout
            return HttpResponse('<h1>Pleurer</h1>')
