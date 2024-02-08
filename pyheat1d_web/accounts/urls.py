from django.urls import path

from pyheat1d_web.accounts import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("logout/", views.MyLogout.as_view(), name="logout"),
]
