from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertTemplateUsed


@pytest.mark.integration
def test_positive_template_used(client, simulation):
    resp = client.get(resolve_url("core:detail_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/detail_simulation.html")


@pytest.mark.integration
def test_positive_must_have_buttons_voltar(client, simulation):
    resp = client.get(resolve_url("core:detail_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    url = resolve_url("core:list_simulation")
    assertContains(resp, f'<a class="btn btn-secondary" href="{url}">Voltar</a>')

    url = resolve_url("core:run_simulation", pk=simulation.pk)
    assertContains(resp, '<button type="submit" class="btn btn-primary">Rodar</button>')


@pytest.mark.integration
def test_table(client, simulation):
    resp = client.get(resolve_url("core:detail_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, "<tr>", 11)

    assertContains(resp, "Id")
    assertContains(resp, "Tag")
    assertContains(resp, "Arquivo de entrada")
    assertContains(resp, "Status")
    assertContains(resp, "Comprimento")
    assertContains(resp, "Divisões")
    assertContains(resp, "Delta t")
    assertContains(resp, "Passos de tempo")
    assertContains(resp, "Temperatuta Inicial")
    assertContains(resp, "Condição de contorno a Esquerda")
    assertContains(resp, "Condição de contorno a Direita")


@pytest.mark.integration
def test_table_value(client, simulation):
    resp = client.get(resolve_url("core:detail_simulation", pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK
    assertContains(resp, simulation.pk)
    assertContains(resp, simulation.tag)
    assertContains(resp, simulation.input_file)
    assertContains(resp, simulation.status)
    assertContains(resp, simulation.length)
    assertContains(resp, simulation.ndiv)
    assertContains(resp, simulation.nstep)
    assertContains(resp, simulation.dt)
    assertContains(resp, simulation.initialt)
    assertContains(resp, simulation.lbc_value)
    assertContains(resp, simulation.rbc_value)
