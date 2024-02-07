from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertTemplateUsed

from pyheat1d_web.core.models import Simulation


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
def test_positive_api_url_with_be_status_success(client, mocker, simulation):
    simulation.status = Simulation.Status.SUCCESS
    simulation.save()

    results_mocker = mocker.patch("pyheat1d_web.core.views._read_results")

    resp = client.get(resolve_url("core:results_simulation", pk=simulation.pk))
    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, f"/api/results/{simulation.pk}")

    results_mocker.assert_called_once()


@pytest.mark.integration
def test_positive_without_be_status_success(client, simulation):
    resp = client.get(resolve_url("core:results_simulation", pk=simulation.pk))
    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, "Não existe resultados disponíveis para essa simulação ainda.")


@pytest.mark.integration
def test_graph_div(client, mocker, simulation):
    simulation.status = Simulation.Status.SUCCESS
    simulation.save()
    results_mocker = mocker.patch("pyheat1d_web.core.views._read_results")

    resp = client.get(resolve_url("core:results_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, '<canvas id="plot_area"></canvas>')

    results_mocker.assert_called_once()
