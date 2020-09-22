from django.urls import path
from web import views
from web.models import LogMessage


home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="web/home.html",
)

urlpatterns = [
    path("home/", home_list_view, name="home"),
    path("hello/<name>", views.hello_there,name="hello_there"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("log/", views.LogView.as_view(), name="log"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
]