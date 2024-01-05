from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.analysis_list, name="analysis_list"),
    path("create/", views.create_analysis_form, name="create_analysis_form"),
    path("run/<int:pk>/", views.run_analysis, name="run_analysis"),
    path("edit/<int:pk>/", views.edit_analysis_form, name="edit_analysis_form"),
    path("detail/<int:pk>/", views.analysis_detail, name="analysis_detail"),
    path("delete/<int:pk>/", views.analysis_delete, name="analysis_delete"),
    path("results/<int:pk>/", views.simulation_results, name="simulation_results"),
    path("api/results/<int:pk>/", views.get_simulation_results_api, name="get_simulation_results_api"),
]
