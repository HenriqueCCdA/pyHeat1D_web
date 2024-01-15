from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertRedirects

from pyheat1d_web.core.models import Simulation

view_name = "core:run_simulation"
redirect_view_name = "core:list_simulation"


@pytest.mark.integration
def test_positive_init_status(client, mocker, simulation):
    run_simulation_task = mocker.patch("pyheat1d_web.core.views.run_simulation_task")

    resp = client.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url(redirect_view_name))

    run_simulation_task.delay.assert_called_once()
    run_simulation_task.delay.assert_called_once_with(simulation_id=simulation.pk)


@pytest.mark.integration
@pytest.mark.parametrize(
    "status",
    [
        Simulation.Status.FAILED,
        Simulation.Status.RUNNING,
        Simulation.Status.SUCCESS,
    ],
    ids=[
        Simulation.Status.FAILED.label,
        Simulation.Status.RUNNING.label,
        Simulation.Status.SUCCESS.label,
    ],
)
def test_negative_should_be_called_only_to_the_init_status(client, mocker, simulation, status):
    run_simulation_task = mocker.patch("pyheat1d_web.core.views.run_simulation_task")

    simulation.status = status
    simulation.save()

    resp = client.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url(redirect_view_name))

    run_simulation_task.delay.assert_not_called()


def test_negative_wrong_id(client, mocker, db):
    run_simulation_task = mocker.patch("pyheat1d_web.core.views.run_simulation_task")

    url = resolve_url(view_name, pk=404)
    resp = client.get(url)

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url(redirect_view_name))

    run_simulation_task.delay.assert_not_called()
