from datetime import datetime

from pyheat1d_web.core.models import Simulation


def test_model_fiels(simulation):
    assert simulation._meta.get_field("input_file")
    assert simulation._meta.get_field("status")
    assert simulation._meta.get_field("tag")
    assert simulation._meta.get_field("length")
    assert simulation._meta.get_field("ndiv")
    assert simulation._meta.get_field("dt")
    assert simulation._meta.get_field("nstep")
    assert simulation._meta.get_field("initialt")
    assert simulation._meta.get_field("lbc_value")
    assert simulation._meta.get_field("rbc_value")
    assert simulation._meta.get_field("created_at")
    assert simulation._meta.get_field("modified_at")


def test_create_at_and_modified_at(simulation):
    assert isinstance(simulation.created_at, datetime)
    assert isinstance(simulation.modified_at, datetime)


def test_str(simulation):
    assert str(simulation) == simulation.tag


def test_default(simulation):
    assert simulation.status == Simulation.Status.INIT
