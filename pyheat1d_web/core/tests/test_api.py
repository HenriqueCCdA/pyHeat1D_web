from http import HTTPStatus
from pathlib import Path

import pytest
from django.shortcuts import resolve_url

from pyheat1d_web.core.models import Simulation

CT_JSON = "application/json"

pytestmark = pytest.mark.django_db

ROUTE_NAME = "core:simulation_results"


@pytest.mark.integration
def test_positive_get_simulation_results_without_status_success(client, simulation):
    response = client.get(resolve_url(ROUTE_NAME, simulation.pk), content_type=CT_JSON)

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {"detail": "Simulação 'sim_01' não tem resultados ainda."}


@pytest.mark.integration
def test_positive_get_simulation_results_with_status_success(client, simulation):
    simulation.status = Simulation.Status.SUCCESS

    base_dir = Path.cwd()

    simulation.input_file = base_dir / "pyheat1d_web/core/tests/assets/results.json"
    simulation.save()

    response = client.get(
        resolve_url(ROUTE_NAME, simulation.pk),
        content_type=CT_JSON,
    )

    assert response.status_code == HTTPStatus.OK

    body = response.json()

    assert body["mesh"] == [0.17, 0.5, 0.83]

    assert len(body["steps"]) == 3

    expected = [
        {
            "step": 0,
            "t": 0.0,
            "u": [0.0, 0.0, 0.0],
        },
        {
            "step": 200,
            "t": 20.0,
            "u": [6.666666666666668, 0.0, -6.666666666666668],
        },
        {
            "step": 300,
            "t": 30.0,
            "u": [6.666666666666668, 0.0, -6.666666666666668],
        },
    ]

    for e, b in zip(expected, body["steps"]):
        assert e == b


@pytest.mark.integration
def test_positive_get_simulation_query_params(client, simulation):
    simulation.status = Simulation.Status.SUCCESS

    base_dir = Path.cwd()

    simulation.input_file = base_dir / "pyheat1d_web/core/tests/assets/results.json"
    simulation.save()

    response = client.get(
        resolve_url(ROUTE_NAME, simulation.pk)+"?istep=0&istep=3",
        content_type=CT_JSON,
    )

    assert response.status_code == HTTPStatus.OK

    body = response.json()

    assert body["mesh"] == [0.17, 0.5, 0.83]

    assert len(body["steps"]) == 2

    expected = [
        {
            "step": 0,
            "t": 0.0,
            "u": [0.0, 0.0, 0.0],
        },
        {
            "step": 300,
            "t": 30.0,
            "u": [6.666666666666668, 0.0, -6.666666666666668],
        },
    ]

    for e, b in zip(expected, body["steps"]):
        assert e == b


@pytest.mark.integration
@pytest.mark.parametrize("values", [
    ("-1", "1", "2"),
    ("0", "1", "50"),
    ("0", "not a int", "3"),
])
def test_negative_get_simulation_invalid_query_params(client, simulation, values):
    simulation.status = Simulation.Status.SUCCESS

    base_dir = Path.cwd()

    simulation.input_file = base_dir / "pyheat1d_web/core/tests/assets/results.json"
    simulation.save()

    query_string=f"?istep={values[0]}&istep={values[1]}&istep={values[2]}"

    response = client.get(
        resolve_url(ROUTE_NAME, simulation.pk)+query_string,
        content_type=CT_JSON,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": "Valores invalidos para o passo de tempo."}


@pytest.mark.integration
def test_negative_simularion_not_found(client):
    response = client.get(
        resolve_url(ROUTE_NAME, 404),
        content_type=CT_JSON,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.integration
def test_negative_only_allowd_get(client, simulation):
    HTTP_METHOD = [
        client.post,
        client.put,
        client.patch,
        client.delete,
    ]

    for http_method in HTTP_METHOD:
        response = http_method(
            resolve_url(ROUTE_NAME, simulation.pk),
            content_type=CT_JSON,
        )

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
