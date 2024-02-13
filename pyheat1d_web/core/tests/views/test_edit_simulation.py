import json
from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

from pyheat1d_web.core.models import Simulation
from pyheat1d_web.core.tests.constants import EDIT_CASE_FILE

view_name = "core:edit_simulation_form"


@pytest.mark.integration
def test_user_must_be_logged(client, simulation):
    url = resolve_url(view_name, pk=simulation.pk)
    resp = client.get(url)

    assert resp.status_code == HTTPStatus.FOUND

    url_login = f"{resolve_url('accounts:login')}?next={url}"

    assertRedirects(resp, url_login)


@pytest.mark.integration
def test_positive_template_used(client_logged, simulation):
    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/edit_simulation_form.html")


@pytest.mark.integration
def test_positive_must_have_buttons_criar_voltar(client_logged, simulation):
    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, '<button class="btn btn-primary" type="submit">Salvar</button>')

    url = resolve_url("core:list_simulation")

    assertContains(resp, f'<a class="btn btn-secondary" href="{url}">Voltar</a>')


@pytest.mark.integration
def test_positive_edit(client_logged, file_case, simulation, payload_edit):
    simulation.input_file = file_case
    simulation.status = Simulation.Status.SUCCESS
    simulation.save()

    resp = client_logged.post(resolve_url(view_name, pk=simulation.pk), data=payload_edit)

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))

    simulation.refresh_from_db()

    assert simulation.status == Simulation.Status.INIT

    for k, v in payload_edit.items():
        assert getattr(simulation, k) == v

    assert file_case.exists()
    case_read = json.load(file_case.open(mode="r"))

    assert case_read == EDIT_CASE_FILE
