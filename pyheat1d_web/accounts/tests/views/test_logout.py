from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertRedirects

URL = resolve_url("accounts:logout")


@pytest.mark.integration
def test_positive_post(client_logged):
    resp = client_logged.post(URL)
    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("accounts:login"))
