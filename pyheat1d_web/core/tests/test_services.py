import re
from json import load
from pathlib import Path

import pytest

from pyheat1d_web.core.services import _get_simulations_base_folder, cleaned_isteps, create_or_update_simulation_case
from pyheat1d_web.core.tests.constants import CASE_FILE, EDIT_CASE_FILE


@pytest.mark.unit
def test_positive_create_file_case(mocker, payload_create, tmp_path):
    base_folder = Path(tmp_path)
    mocker.patch("pyheat1d_web.core.services._get_simulations_base_folder", return_value=base_folder)

    new_case = payload_create.copy()
    file_case = create_or_update_simulation_case(new_case)

    expected = base_folder / "sim_01/case.json"

    assert file_case == Path(expected)

    case_read = load(file_case.open(mode="r"))

    assert case_read == CASE_FILE


@pytest.mark.unit
def test_positive_update_file_case(file_case, simulation, payload_edit):
    new_case = payload_edit.copy()

    update_file_case = create_or_update_simulation_case(new_case, input_file=file_case)

    assert update_file_case == file_case

    case_read = load(update_file_case.open(mode="r"))

    assert case_read == EDIT_CASE_FILE


@pytest.mark.unit
def test_get_simulations_base_folder():
    assert str(_get_simulations_base_folder()) == "analisys"


@pytest.mark.unit
def test_postive_cleaned_isteps():
    assert cleaned_isteps(["0", "1", "45", "49"], 50) == [0, 1, 45, 49]


@pytest.mark.unit
@pytest.mark.parametrize(
    "values, error",
    [
        (("-1", "1", "2"), "O passo de tempo não pode ser negativo."),
        (("0", "1", "50"), "O passo de tempo não pode ser maior ou igual a 50."),
        (("0", "not a int", "3"), "invalid literal for int() with base 10: 'not a int'"),
    ],
)
def test_negative_invalid_isteps(values, error):
    with pytest.raises(ValueError, match=re.escape(error)):
        cleaned_isteps(values, 50)
