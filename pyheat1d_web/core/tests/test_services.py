import re
from json import load
from pathlib import Path

import pytest

from pyheat1d_web.core.services import (
    ResultFileNotFoundError,
    _get_simulations_base_folder,
    cleaned_isteps,
    create_or_update_simulation_case,
    read_mesh,
    read_results,
    results_times,
)
from pyheat1d_web.core.tests.constants import CASE_FILE, EDIT_CASE_FILE, INPUT_CASE_FILE


@pytest.mark.unit
def test_positive_create_file_case(user, payload_create):
    base_folder = _get_simulations_base_folder(user.pk)

    new_case = payload_create.copy()
    file_case = create_or_update_simulation_case(new_case, user)

    expected = base_folder / "sim_01/case.json"

    assert file_case == Path(expected)

    case_read = load(file_case.open(mode="r"))

    assert case_read == CASE_FILE


@pytest.mark.unit
def test_positive_update_file_case(file_case, user, simulation, payload_edit):
    new_case = payload_edit.copy()

    update_file_case = create_or_update_simulation_case(new_case, user, input_file=file_case)

    assert update_file_case == file_case

    case_read = load(update_file_case.open(mode="r"))

    assert case_read == EDIT_CASE_FILE


@pytest.mark.unit
def test_get_simulations_base_folder(analisys_folder):
    assert str(_get_simulations_base_folder(2)) == str(analisys_folder / "2")


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


@pytest.mark.unit
def test_positive_results_time_path():
    assert results_times(INPUT_CASE_FILE) == [0.0, 10.0, 20.0, 30.0]


@pytest.mark.unit
def test_positive_results_time_str():
    assert results_times(str(INPUT_CASE_FILE)) == [0.0, 10.0, 20.0, 30.0]


@pytest.mark.unit
def test_negative_results_times_not_found():
    input_file_path = Path.cwd() / "wrong/case.json"

    expected = f"Arquivo de resultado não achado no caminho '{input_file_path.parent}'"

    with pytest.raises(ResultFileNotFoundError, match=expected):
        results_times(input_file_path)


@pytest.mark.unit
def test_read_mesh():
    base_dir = INPUT_CASE_FILE.parent
    assert read_mesh(base_dir) == ""


@pytest.mark.unit
def test_read_results():
    base_dir = INPUT_CASE_FILE.parent
    assert read_results(base_dir) == ""
