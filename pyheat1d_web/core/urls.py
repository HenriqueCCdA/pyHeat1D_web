from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.list_simulation, name="list_simulation"),
    path("create/", views.create_simulation_form, name="create_simulation_form"),
    path("run/<int:pk>/", views.run_simulation, name="run_simulation"),
    path("edit/<int:pk>/", views.edit_simulation_form, name="edit_simulation_form"),
    path("detail/<int:pk>/", views.detail_simulation, name="detail_simulation"),
    path("delete/<int:pk>/", views.delete_simulation, name="delete_simulation"),
    path("results/<int:pk>/", views.results_simulation, name="results_simulation"),
    path("api/results/<int:pk>/", views.get_simulation_results_api, name="get_simulation_results_api"),
]
