from http import HTTPStatus

from django.shortcuts import resolve_url
from pytest_django.asserts import assertTemplateUsed


def test_positive_template_used(client, simulation):
    resp = client.get(resolve_url("core:detail_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/detail_simulation.html")
