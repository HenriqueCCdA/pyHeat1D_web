from http import HTTPStatus

from django.shortcuts import resolve_url
from pytest_django.asserts import assertTemplateUsed


def test_create_analysis_form(client):
    resp = client.get(resolve_url("core:create_analysis_form"))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/create_analysis_form.html")
