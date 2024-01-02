from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.analysis_list, name="analysis_list"),
    path("create/", views.create_analysis_form, name="create_analysis_form"),
    path("run/<int:pk>", views.run_analysis, name="run_analysis"),
    path("detail/<int:pk>", views.analysis_detail, name="analysis_detail"),
    path("delete/<int:pk>", views.analysis_delete, name="analysis_delete"),
]
