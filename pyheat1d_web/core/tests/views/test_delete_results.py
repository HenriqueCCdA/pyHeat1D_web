from http import HTTPStatus
from pathlib import Path

from django.shortcuts import resolve_url
from pytest_django.asserts import assertRedirects

from pyheat1d_web.core.models import Simulation


def test_positive_delete_simulation(client, mocker, simulation, tmp_path):
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

    resp = client.get(resolve_url("core:delete_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))

    assert not simulation_folder.exists()

    assert not Simulation.objects.exists()


def test_negative_wrong_id(client, db):
    resp = client.get(resolve_url("core:delete_simulation", pk=404))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))


def test_negative_delete_dir_not_empty(client, mocker, simulation, tmp_path):
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

    resp = client.get(resolve_url("core:delete_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))

    assert simulation_folder.exists()

    assert Simulation.objects.exists()
