import pytest

from pyheat1d_web.core.forms import NewSimulationForm


@pytest.mark.unit
def test_positive_validation(payload_create, db):
    form = NewSimulationForm(payload_create)

    assert form.is_valid()


@pytest.mark.unit
def test_positive_cleaned_data(payload_create, db):
    form = NewSimulationForm(payload_create)

    form.is_valid()

    for k, v in payload_create.items():
        assert form.cleaned_data[k] == v


@pytest.mark.unit
def test_negative_missing_tag_name(payload_create, db):
    del payload_create["tag"]

    form = NewSimulationForm(payload_create)

    assert not form.is_valid()

    assert form.errors == {"tag": ["Este campo é obrigatório."]}


@pytest.mark.unit
@pytest.mark.parametrize(
    "field,value,error",
    [
        ("length", "a", "Informe um número."),
        ("length", 0.0, "Número tem que ser maior que zero."),
        ("length", -1.0, "Número tem que ser maior que zero."),
        ("ndiv", "a", "Informe um número inteiro."),
        ("ndiv", 0, "Número tem que ser maior que zero."),
        ("ndiv", -1, "Número tem que ser maior que zero."),
        ("dt", "a", "Informe um número."),
        ("dt", 0.0, "Número tem que ser maior que zero."),
        ("dt", -0.1, "Número tem que ser maior que zero."),
        ("nstep", "a", "Informe um número inteiro."),
        ("nstep", 0, "Número tem que ser maior que zero."),
        ("nstep", -1, "Número tem que ser maior que zero."),
        ("initialt", "a", "Informe um número."),
        ("lbc_value", "a", "Informe um número."),
        ("rbc_value", "a", "Informe um número."),
    ],
)
def test_negative_invalid_value(payload_create, field, value, error, db):
    payload_create[field] = value

    form = NewSimulationForm(payload_create)

    assert not form.is_valid()

    assert form.errors[field] == [error]
