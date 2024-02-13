from http import HTTPStatus
from pathlib import Path

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertRedirects

from pyheat1d_web.core.models import Simulation

view_name = "core:delete_simulation"


@pytest.mark.integration
def test_user_must_be_logged(client, simulation):
    url = resolve_url(view_name, pk=simulation.pk)
    resp = client.get(url)

    assert resp.status_code == HTTPStatus.FOUND

    url_login = f"{resolve_url('accounts:login')}?next={url}"

    assertRedirects(resp, url_login)


@pytest.mark.integration
def test_positive_delete_simulation(client_logged, mocker, simulation, tmp_path):
    case_folder_base = Path(tmp_path)

    tag = simulation.tag
    simulation_folder = case_folder_base / f"analisys/{tag}"
    simulation_case_file = simulation_folder / "case.json"

    simulation_folder.mkdir(parents=True)
    simulation_case_file.open(mode="w")
    (simulation_folder / "mesh.json").open(mode="w")
    (simulation_folder / "results.json").open(mode="w")

    simulation.input_file = simulation_case_file
    simulation.save()

    mocker.patch("pyheat1d_web.core.services._get_simulations_base_folder", return_value=case_folder_base)

    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))

    assert not simulation_folder.exists()

    assert not Simulation.objects.exists()


@pytest.mark.integration
def test_negative_wrong_id(client_logged, db):
    resp = client_logged.get(resolve_url(view_name, pk=404))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))


@pytest.mark.integration
def test_negative_delete_dir_not_empty(client_logged, mocker, simulation, tmp_path):
    case_folder_base = Path(tmp_path)

    tag = simulation.tag
    simulation_folder = case_folder_base / f"analisys/{tag}"
    simulation_case_file = simulation_folder / "case.json"

    simulation_folder.mkdir(parents=True)
    simulation_case_file.open(mode="w")
    (simulation_folder / "mesh_wrong_name.json").open(mode="w")
    (simulation_folder / "results_wrong_name.json").open(mode="w")

    simulation.input_file = simulation_case_file
    simulation.save()

    mocker.patch("pyheat1d_web.core.services._get_simulations_base_folder", return_value=case_folder_base)

    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))

    assert simulation_folder.exists()

    assert Simulation.objects.exists()
