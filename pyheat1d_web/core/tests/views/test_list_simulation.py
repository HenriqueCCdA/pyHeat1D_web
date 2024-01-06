from http import HTTPStatus

from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertTemplateUsed

URL = resolve_url("core:list_simulation")


def test_positive_template_used(client, simulation):
    resp = client.get(URL)

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/list_simulation.html")


def test_positive_table_list_simulation_two_simulation(client, list_simulation):
    resp = client.get(URL)

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


def test_positive_create_button(client, list_simulation):
    resp = client.get(URL)

    assert resp.status_code == HTTPStatus.OK

    rote_create = resolve_url("core:create_simulation_form")

    assertContains(resp, "Nova simulacao")
    assertContains(resp, f'href="{rote_create}"')
