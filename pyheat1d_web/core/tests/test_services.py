from json import load
from pathlib import Path

import pytest

from pyheat1d_web.core.services import create_or_update_simulation_case
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
