from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pyheat1d_web.core.urls")),
    path("accounts/", include("pyheat1d_web.accounts.urls")),
]
