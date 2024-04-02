from django import forms
from django.db.models.query import InstanceCheckMeta
from apps.Auth.models import User

import logging
logger = logging.getLogger(__name__)


class FriendForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('friends',)

    def __str__(self):
        return self.instance.username

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.friends = self.cleaned_data['friends']
    #     if commit:
    #         instance.save()
    #     return instance
