from rest_framework import serializers
from .models import UserTwoFA

class UserTwoFASerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTwoFA
        fields = ('otp', 'otp_expiry_time')

