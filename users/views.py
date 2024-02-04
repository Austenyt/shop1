from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LoginView as BaseLogoutView


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    template_name = 'users/login.html'
