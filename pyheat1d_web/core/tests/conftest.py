from pathlib import Path

import pytest

from pyheat1d_web.core.models import Simulation


@pytest.fixture
def simulation(user):
    sim = Simulation.objects.create(
        tag="sim_01",
        input_file="analisys/sim_01/case.json",
        length=100.0,
        ndiv=100,
        dt=1.0,
        nstep=10,
        initialt=10.0,
        lbc_value=10.0,
        rbc_value=10.0,
        user=user,
    )

    return sim


@pytest.fixture
def list_simulation(user):
    sim1 = Simulation(
        tag="sim_01",
        input_file="analisys/sim_01/case.json",
        length=100.0,
        ndiv=100,
        dt=1.0,
        nstep=10,
        initialt=10.0,
        lbc_value=10.0,
        rbc_value=10.0,
        user=user,
    )

    sim2 = Simulation(
        tag="sim_02",
        input_file="analisys/sim_02/case.json",
        length=10.0,
        ndiv=200,
        dt=1.0,
        nstep=10,
        initialt=50.0,
        lbc_value=10.0,
        rbc_value=10.0,
        user=user,
    )

    return Simulation.objects.bulk_create([sim1, sim2])


@pytest.fixture
def payload_create():
    return {
        "tag": "sim_01",
        "length": 100.0,
        "ndiv": 10_000,
        "dt": 1.0,
        "nstep": 100,
        "initialt": 50.0,
        "lbc_value": 0.0,
        "rbc_value": 100.0,
    }


@pytest.fixture
def payload_edit():
    return {
        "length": 512.0,
        "ndiv": 11_234,
        "dt": 1.1,
        "nstep": 112,
        "initialt": 51.2,
        "lbc_value": 0.2,
        "rbc_value": 221.0,
    }


@pytest.fixture
def file_case(tmp_path, simulation):
    simulation_folder = Path(tmp_path) / simulation.tag
    simulation_folder.mkdir()
    file_case = simulation_folder / "case.json"
    file_case.open(mode="w")
    return file_case
