from http import HTTPStatus
from uuid import uuid4

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertRedirects

from pyheat1d_web.core.models import Simulation

view_name = "core:run_simulation"
redirect_view_name = "core:list_simulation"


@pytest.mark.integration
def test_user_must_be_logged(client, simulation):
    url = resolve_url(view_name, pk=simulation.pk)
    resp = client.get(url)

    assert resp.status_code == HTTPStatus.FOUND

    url_login = f"{resolve_url('accounts:login')}?next={url}"

    assertRedirects(resp, url_login)


@pytest.mark.integration
def test_positive_init_status(client_logged, mocker, simulation):
    AsyncResultMock = type("AsyncResultMock", (), {"id": uuid4()})

    run_simulation_task_delay = mocker.patch(
        "pyheat1d_web.core.views.run_simulation_task.delay",
        return_value=AsyncResultMock,
    )

    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url(redirect_view_name))

    run_simulation_task_delay.assert_called_once()
    run_simulation_task_delay.assert_called_once_with(simulation_id=simulation.pk)

    simulation.refresh_from_db()

    assert simulation.celery_task == AsyncResultMock.id


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
def test_negative_should_be_called_only_to_the_init_status(client_logged, mocker, simulation, status):
    run_simulation_task = mocker.patch("pyheat1d_web.core.views.run_simulation_task")

    simulation.status = status
    simulation.save()

    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url(redirect_view_name))

    run_simulation_task.delay.assert_not_called()

    simulation.refresh_from_db()

    assert simulation.celery_task is None


def test_negative_wrong_id(client_logged, mocker, db):
    run_simulation_task = mocker.patch("pyheat1d_web.core.views.run_simulation_task")

    url = resolve_url(view_name, pk=404)
    resp = client_logged.get(url)

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url(redirect_view_name))

    run_simulation_task.delay.assert_not_called()
