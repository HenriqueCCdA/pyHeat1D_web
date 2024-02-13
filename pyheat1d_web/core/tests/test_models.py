from datetime import datetime

import pytest

from pyheat1d_web.core.models import Simulation


@pytest.mark.unit
def test_model_fiels(simulation):
    assert simulation._meta.get_field("input_file")
    assert simulation._meta.get_field("status")
    assert simulation._meta.get_field("tag")
    assert simulation._meta.get_field("length")
    assert simulation._meta.get_field("ndiv")
    assert simulation._meta.get_field("dt")
    assert simulation._meta.get_field("nstep")
    assert simulation._meta.get_field("initialt")
    assert simulation._meta.get_field("user")
    assert simulation._meta.get_field("lbc_value")
    assert simulation._meta.get_field("rbc_value")
    assert simulation._meta.get_field("celery_task")
    assert simulation._meta.get_field("created_at")
    assert simulation._meta.get_field("modified_at")


@pytest.mark.unit
def test_create_at_and_modified_at(simulation):
    assert isinstance(simulation.created_at, datetime)
    assert isinstance(simulation.modified_at, datetime)


@pytest.mark.unit
def test_str(simulation):
    assert str(simulation) == simulation.tag


@pytest.mark.unit
def test_default(simulation):
    assert simulation.status == Simulation.Status.INIT


@pytest.mark.unit
def test_relationship(list_simulation, user):
    assert list_simulation[0].user == user
    assert set(user.simulation_set.all()) == set(list_simulation)
