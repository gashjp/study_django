from django import forms
from web.models import LogMessage
from django.contrib.auth.forms import AuthenticationForm

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required

class AdminLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args,**kwargs)