from django.shortcuts import render
import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from web.forms import LogMessageForm, AdminLoginForm
from web.models import LogMessage, WebUser
from django.views.generic import ListView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView

class WebUserLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not isinstance(request.user, WebUser):
            return redirect('web:login')
        return super().dispatch(request, *args, **kwargs)

class HomeListView(WebUserLoginRequiredMixin, ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

class AboutView(WebUserLoginRequiredMixin, TemplateView):
    template_name = 'web/about.html'

class ContactView(WebUserLoginRequiredMixin, TemplateView):
    template_name = 'web/contact.html'

class LogView(WebUserLoginRequiredMixin, FormView):
    template_name = 'web/log_message.html'
    form_class = LogMessageForm
    success_url = '/home/'
    def form_valid(self, form):
        message = form.save(commit=False)
        message.log_date = datetime.now()
        message.save()
        return super().form_valid(form)

class Login(auth_views.LoginView):

    template_name = 'web/login.html'
    form_class = AdminLoginForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flag = self.request.GET.get("flag")
        if flag:
            self.template_name = 'web/login.html'
        else:
            self.template_name = 'web/login2.html'

        return context

class Logout(WebUserLoginRequiredMixin, auth_views.LogoutView):
    pass

def hello_there(request, name):
    return render(
        request,
        'web/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )
