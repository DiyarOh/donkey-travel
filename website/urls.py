from django.urls import path
from website.views import HomepageView, LoginView, RegisterView

urlpatterns = [
    path("", HomepageView.as_view(), name='index'),
    path("login/", LoginView.as_view(), name='login'),
    path("register/", RegisterView.as_view(), name='register'),
]