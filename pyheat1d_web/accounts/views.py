from django.contrib.auth.views import LoginView, LogoutView


class MyLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class MyLogout(LogoutView):
    template_name = None
