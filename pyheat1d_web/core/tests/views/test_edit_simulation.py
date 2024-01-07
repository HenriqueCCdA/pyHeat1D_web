from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed


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


def test_positive_template_used(client, simulation):
    resp = client.get(resolve_url("core:edit_simulation_form", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/edit_simulation_form.html")


def test_positive_must_have_buttons_criar_voltar(client, simulation):
    resp = client.get(resolve_url("core:edit_simulation_form", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, '<button class="btn btn-primary" type="submit">Salvar</button>')

    url = resolve_url("core:list_simulation")

    assertContains(resp, f'<a class="btn btn-secondary" href="{url}">Voltar</a>')


def test_positive_edit(client, simulation, payload_edit):
    resp = client.post(
        resolve_url("core:edit_simulation_form", pk=simulation.pk),
        data=payload_edit,
    )

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))

    simulation.refresh_from_db()

    for k, v in payload_edit.items():
        assert getattr(simulation, k) == v
