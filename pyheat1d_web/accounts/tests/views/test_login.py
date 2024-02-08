from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

URL = resolve_url("accounts:login")
URL_REDIRECT = resolve_url("core:list_simulation")


@pytest.mark.integration
def test_positive_template_used(client):
    resp = client.get(URL)

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "accounts/login.html")


@pytest.mark.integration
def test_positive_login(client, user_with_password):
    data = {"username": user_with_password.email, "password": user_with_password.plain_password}

    resp = client.post(URL, data=data)
    assert resp.status_code == HTTPStatus.FOUND

    assertRedirects(resp, URL_REDIRECT)


@pytest.mark.integration
def test_positive_logged_user_must_be_redirect(client, user_logged):
    resp = client.get(URL)
    assert resp.status_code == HTTPStatus.FOUND

    assertRedirects(resp, URL_REDIRECT)


@pytest.mark.integration
def test_negative_wrong_credentials(client, user_with_password):
    data = {"username": user_with_password.email + "1", "password": user_with_password.plain_password}

    resp = client.post(URL, data=data)
    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, "Your username and password didn't match. Please try again.")
