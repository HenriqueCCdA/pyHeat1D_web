from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertTemplateUsed


@pytest.mark.integration
def test_positive_template_used(client, simulation):
    resp = client.get(resolve_url("core:results_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/results_simulation.html")


@pytest.mark.integration
def test_positive_button_voltar(client, simulation):
    resp = client.get(resolve_url("core:results_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    url = resolve_url("core:list_simulation")

    assertContains(resp, f'href="{url}"')
    assertContains(resp, "Voltar")


@pytest.mark.integration
def test_positive_api(client, simulation):
    resp = client.get(resolve_url("core:results_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, f"/api/results/{simulation.pk}")


@pytest.mark.integration
def test_graph_div(client, simulation):
    resp = client.get(resolve_url("core:results_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, '<canvas id="plot_area"></canvas>')
