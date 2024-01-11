import json
from http import HTTPStatus
from pathlib import Path

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

from pyheat1d_web.core.models import Simulation


@pytest.fixture
def payload_edit():
    return {
        "tag": "sim_01",
        "length": 512.0,
        "ndiv": 11_234,
        "dt": 1.1,
        "nstep": 112,
        "initialt": 51.2,
        "lbc_value": 0.2,
        "rbc_value": 221.0,
    }


CASE_FILE = {
    "length": 512.0,
    "ndiv": 11_234,
    "dt": 1.1,
    "nstep": 112,
    "initialt": 51.2,
    "lbc": {"type": 1, "params": {"value": 0.2}},
    "rbc": {"type": 1, "params": {"value": 221.0}},
    "prop": {"k": 1.0, "ro": 1.0, "cp": 1.0},
    "write_every_steps": 100,
}


@pytest.mark.integration
def test_positive_template_used(client, simulation):
    resp = client.get(resolve_url("core:edit_simulation_form", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/edit_simulation_form.html")


@pytest.mark.integration
def test_positive_must_have_buttons_criar_voltar(client, simulation):
    resp = client.get(resolve_url("core:edit_simulation_form", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, '<button class="btn btn-primary" type="submit">Salvar</button>')

    url = resolve_url("core:list_simulation")

    assertContains(resp, f'<a class="btn btn-secondary" href="{url}">Voltar</a>')


@pytest.mark.integration
def test_positive_edit(client, tmp_path, mocker, simulation, payload_edit):
    mocker.patch("pyheat1d_web.core.services._get_simulations_base_folder", return_value=Path(tmp_path))

    simulation_foldder = Path(tmp_path) / simulation.tag
    simulation_foldder.mkdir()
    file_case = simulation_foldder / "case.json"
    file_case.open(mode="w")

    simulation.status = Simulation.Status.SUCCESS
    simulation.save()

    resp = client.post(
        resolve_url("core:edit_simulation_form", pk=simulation.pk),
        data=payload_edit,
    )

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))

    simulation.refresh_from_db()

    assert simulation.status == Simulation.Status.INIT

    for k, v in payload_edit.items():
        assert getattr(simulation, k) == v

    assert file_case.exists()

    case_read = json.load(file_case.open(mode="r"))

    assert case_read == CASE_FILE
