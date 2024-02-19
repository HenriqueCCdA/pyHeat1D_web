from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

from pyheat1d_web.core.models import Simulation

view_name = "core:results_simulation"


@pytest.mark.integration
def test_user_must_be_logged(client, simulation):
    url = resolve_url(view_name, pk=simulation.pk)
    resp = client.get(url)

    assert resp.status_code == HTTPStatus.FOUND

    url_login = f"{resolve_url('accounts:login')}?next={url}"

    assertRedirects(resp, url_login)


@pytest.mark.integration
def test_positive_template_used(client_logged, simulation):
    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/results_simulation.html")


@pytest.mark.integration
def test_positive_button_voltar(client_logged, simulation):
    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    url = resolve_url("core:list_simulation")

    assertContains(resp, f'href="{url}"')
    assertContains(resp, "Voltar")


@pytest.mark.integration
def test_positive_api_url_with_be_status_success(client_logged, mocker, simulation):
    simulation.status = Simulation.Status.SUCCESS
    simulation.save()

    results_mocker = mocker.patch("pyheat1d_web.core.views.results_times")

    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))
    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, f"/api/results/{simulation.pk}")

    results_mocker.assert_called_once()


@pytest.mark.integration
def test_positive_without_be_status_success(client_logged, simulation):
    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))
    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, "Não existe resultados disponíveis para essa simulação ainda.")


@pytest.mark.integration
def test_graph_div(client_logged, mocker, simulation):
    simulation.status = Simulation.Status.SUCCESS
    simulation.save()
    results_mocker = mocker.patch("pyheat1d_web.core.views.results_times")

    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, '<canvas id="plot_area"></canvas>')

    results_mocker.assert_called_once()
