import pytest

from pyheat1d_web.core.forms import EditSimulationForm


@pytest.mark.unit
def test_positive_validation(payload_edit, db):
    form = EditSimulationForm(payload_edit)

    assert form.is_valid()


@pytest.mark.unit
def test_positive_cleaned_data(payload_edit, db):
    form = EditSimulationForm(payload_edit)

    form.is_valid()

    for k, v in payload_edit.items():
        assert form.cleaned_data[k] == v


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
def test_negative_invalid_value(payload_edit, field, value, error, db):
    payload_edit[field] = value

    form = EditSimulationForm(payload_edit)

    assert not form.is_valid()

    assert form.errors[field] == [error]
