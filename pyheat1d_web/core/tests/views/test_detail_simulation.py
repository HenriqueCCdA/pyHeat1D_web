from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

view_name = "core:detail_simulation"


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

    assertTemplateUsed(resp, "core/detail_simulation.html")


@pytest.mark.integration
def test_positive_must_have_buttons_voltar(client_logged, simulation):
    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

    assert resp.status_code == HTTPStatus.OK

    url = resolve_url("core:list_simulation")
    assertContains(resp, f'<a class="btn btn-secondary" href="{url}">Voltar</a>')

    url = resolve_url("core:run_simulation", pk=simulation.pk)
    assertContains(resp, '<button type="submit" class="btn btn-primary">Rodar</button>')


@pytest.mark.integration
def test_table(client_logged, simulation):
    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

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
def test_table_value(client_logged, simulation):
    resp = client_logged.get(resolve_url(view_name, pk=simulation.pk))

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
