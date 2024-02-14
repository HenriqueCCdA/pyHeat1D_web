from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

URL = resolve_url("core:list_simulation")


@pytest.mark.integration
def test_user_must_be_logged(client):
    resp = client.get(URL)

    assert resp.status_code == HTTPStatus.FOUND

    url_login = f"{resolve_url('accounts:login')}?next={URL}"

    assertRedirects(resp, url_login)


@pytest.mark.integration
def test_positive_template_used(client_logged, simulation):
    resp = client_logged.get(URL)

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/list_simulation.html")


@pytest.mark.integration
def test_positive_table_list_simulation_two_simulation(client_logged, list_simulation):
    resp = client_logged.get(URL)
    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, "Id")
    assertContains(resp, "Tag")
    assertContains(resp, "Status")
    assertContains(resp, "Ações")

    assertContains(resp, "<table")
    assertContains(resp, "<thead>")
    assertContains(resp, "<tbody>")
    assertContains(resp, "<tr>", 3)

    assertContains(resp, "Rodar", 2)
    assertContains(resp, "Detalhes", 2)
    assertContains(resp, "Editar", 2)
    assertContains(resp, "Rodar", 2)
    assertContains(resp, "Deletar", 2)

    assertContains(resp, "Resultados")


@pytest.mark.integration
def test_positive_create_button(client_logged, list_simulation):
    resp = client_logged.get(URL)

    assert resp.status_code == HTTPStatus.OK

    route_create = resolve_url("core:create_simulation_form")

    assertContains(resp, "Nova simulacao")
    assertContains(resp, f'href="{route_create}"')
