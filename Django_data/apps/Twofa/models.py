from typing import Optional

from django.db import models
from django.conf import settings

import pyotp
import qrcode
import qrcode.image.svg


class UserTwoFA(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='to2fa',
        on_delete=models.CASCADE, primary_key=True,
    )
    enable = models.BooleanField(default=False)
    otp = models.CharField(max_length=255, blank=True, null=True)
    otp_expiry_time = models.DateTimeField(blank=True, null=True)

    def generate_qr_code(self, name: Optional[str] = None) -> str:
        totp = pyotp.TOTP(self.otp)
        qr_uri = totp.provisioning_uri(
            name=name,
            issuer_name='Pooong'
        )

        image_factory = qrcode.image.svg.SvgPathImage
        qr_code_image = qrcode.make(
            qr_uri,
            image_factory=image_factory
        )

        # The result is going to be an HTML <svg> tag
        return qr_code_image.to_string().decode('utf_8')

    def __str__(self):
        return self
