from django.shortcuts import render

from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = "index.html"


class LoginView(TemplateView):
    template_name = "login.html"


class RegisterView(TemplateView):
    template_name = "register.html"