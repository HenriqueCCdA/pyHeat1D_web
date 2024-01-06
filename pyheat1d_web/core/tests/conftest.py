import pytest

from pyheat1d_web.core.models import Simulation


@pytest.fixture
def simulation(db):
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
    )

    return sim


@pytest.fixture
def list_simulation(db):
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
    )

    return Simulation.objects.bulk_create([sim1, sim2])
