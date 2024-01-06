from http import HTTPStatus

from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertTemplateUsed

URL = resolve_url("core:create_simulation_form")


def test_positive_template_used(client):
    resp = client.get(URL)

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/create_simulation_form.html")


def test_positive_buttons(client):
    resp = client.get(URL)

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, '<button class="btn btn-primary" type="submit">Criar</button>')

    url = resolve_url("core:list_simulation")

    assertContains(resp, f'<a class="btn btn-secondary" href="{url}">Voltar</a>')
