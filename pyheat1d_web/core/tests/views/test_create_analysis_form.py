import json
from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

from pyheat1d_web.core.models import Simulation
from pyheat1d_web.core.services import _get_simulations_base_folder
from pyheat1d_web.core.tests.constants import CASE_FILE

URL = resolve_url("core:create_simulation_form")


@pytest.mark.integration
def test_user_must_be_logged(client):
    resp = client.get(URL)

    assert resp.status_code == HTTPStatus.FOUND

    url_login = f"{resolve_url('accounts:login')}?next={URL}"

    assertRedirects(resp, url_login)


@pytest.mark.integration
def test_positive_template_used(client_logged):
    resp = client_logged.get(URL)

    assert resp.status_code == HTTPStatus.OK

    assertTemplateUsed(resp, "core/create_simulation_form.html")


@pytest.mark.integration
def test_positive_must_have_buttons_criar_voltar(client_logged):
    resp = client_logged.get(URL)

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, '<button class="btn btn-primary" type="submit">Criar</button>')

    url = resolve_url("core:list_simulation")

    assertContains(resp, f'<a class="btn btn-secondary" href="{url}">Voltar</a>')


@pytest.mark.integration
def test_must_have_8_inputs(client_logged):
    resp = client_logged.get(URL)

    assert resp.status_code == HTTPStatus.OK

    assertContains(resp, "Tag")
    assertContains(resp, "Comprimento")
    assertContains(resp, "Numero de divisões")
    assertContains(resp, "Passo de Tempo")
    assertContains(resp, "Número de Passos")
    assertContains(resp, "Temperatura Inicial")
    assertContains(resp, "Temperatura a esquerda")
    assertContains(resp, "Temperatura a direita")

    assertContains(resp, 'type="number"', 7)
    assertContains(resp, 'type="text"')


@pytest.mark.integration
def test_positive_create(client_logged, user_with_password, payload_create):
    base_folder = _get_simulations_base_folder(user_with_password.pk)

    resp = client_logged.post(URL, data=payload_create)

    assert resp.status_code == HTTPStatus.FOUND
    assertRedirects(resp, resolve_url("core:list_simulation"))

    simulation = Simulation.objects.first()

    for key in payload_create.keys():
        assert getattr(simulation, key) == payload_create[key]

    assert simulation.user == user_with_password

    assert simulation.status == "I"

    file_case = base_folder / "sim_01/case.json"

    assert file_case.exists()

    case_read = json.load(file_case.open(mode="r"))

    assert case_read == CASE_FILE


@pytest.mark.integration
def test_negative_create_missing_inputs(client_logged, payload_create, db):
    data = payload_create.copy()
    del data["tag"]

    resp = client_logged.post(URL, data=data)

    assert resp.status_code == HTTPStatus.OK

    assert not Simulation.objects.exists()

    assert resp.context["form"]["tag"].errors == ["Este campo é obrigatório."]

    assertContains(resp, "Erro na hora da criação da simulação.")
    assertContains(resp, "Este campo é obrigatório.")


@pytest.mark.integration
def test_negative_create_simulation_tag_name_must_be_unique(client_logged, payload_create, simulation):
    data = payload_create.copy()

    resp = client_logged.post(URL, data=data)

    assert resp.status_code == HTTPStatus.OK

    assert Simulation.objects.count() == 1

    assertContains(resp, "Simulation com este Tag e User já existe.")
    # assertContains(resp, "Simulation com este Tag já existe.")
