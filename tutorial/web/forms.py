from django import forms
from web.models import LogMessage
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from web.models import WebUser
from django.contrib.auth.models import User

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required

class AdminLoginForm(AuthenticationForm):
    webid = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'username'
        self.fields['password'].widget.attrs['class'] = 'password'
        self.fields['webid'].widget.attrs['class'] = 'webid'
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        webid = self.cleaned_data.get('webid')
        if username is not None and webid is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                try:
                    user = WebUser.objects.get(username=username)
                    if user.deleted == False and user.webid == webid:
                        self.confirm_login_allowed(self.user_cache)
                    else:
                        raise self.get_invalid_login_error()
                except WebUser.DoesNotExist:
                    raise self.get_invalid_login_error()
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if user.deleted:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
