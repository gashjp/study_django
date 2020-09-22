from django.shortcuts import render
import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from web.forms import LogMessageForm
from web.models import LogMessage
from django.views.generic import ListView
from django.contrib.auth import views as auth_views

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

class Login(auth_views.LoginView):

    template_name = 'web/login.html'
    def get_context_data(self, **kwargs):
        context = super(auth_views.LoginView, self).get_context_data(**kwargs)
        flag = self.request.GET.get("flag")
        if flag:
            self.template_name = 'web/login.html'
        else:
            self.template_name = 'web/login2.html'

        return context

def about(request):
    return render(request, "web/about.html")

def contact(request):
    return render(request, "web/contact.html")

def hello_there(request, name):
    return render(
        request,
        'web/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

# Add this code elsewhere in the file:
def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "web/log_message.html", {"form": form})
