from http import HTTPStatus

from django.shortcuts import resolve_url
from pytest_django.asserts import assertTemplateUsed


def test_create_simulation_form(client):
    resp = client.get(resolve_url("core:create_simulation_form"))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/create_simulation_form.html")
