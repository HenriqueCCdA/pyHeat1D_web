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
def test_positive_update_file_case(mocker, simulation, payload_edit, tmp_path):
    simulation_folder = Path(tmp_path) / simulation.tag
    simulation_folder.mkdir()
    file_case = simulation_folder / "case.json"
    file_case.open(mode="w")

    base_folder = Path(tmp_path)
    mocker.patch("pyheat1d_web.core.services._get_simulations_base_folder", return_value=base_folder)

    new_case = payload_edit.copy()
    new_case.update({"tag": simulation.tag})

    file_case = create_or_update_simulation_case(new_case, update=True)

    expected = base_folder / "sim_01/case.json"

    assert file_case == Path(expected)

    case_read = load(file_case.open(mode="r"))

    assert case_read == EDIT_CASE_FILE
