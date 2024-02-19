from datetime import datetime

import pytest
from django.core.exceptions import ValidationError

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
def test_relationship(list_simulation, user_with_password):
    assert list_simulation[0].user == user_with_password
    assert user_with_password.simulation_set.count() == 2


@pytest.mark.unit
def test_unique_constrain_diferent_users_can_have_simulation_with_the_same_tag(user, other_user):
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
        tag="sim_01",
        input_file="analisys/sim_01/case.json",
        length=10.0,
        ndiv=200,
        dt=1.0,
        nstep=10,
        initialt=50.0,
        lbc_value=10.0,
        rbc_value=10.0,
        user=other_user,
    )

    sim1.save()
    sim2.save()

    assert Simulation.objects.count() == 2


@pytest.mark.unit
def test_unique_constrain_tag_must_be_unique_per_user(user):
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
        tag="sim_01",
        input_file="analisys/sim_01/case.json",
        length=10.0,
        ndiv=200,
        dt=1.0,
        nstep=10,
        initialt=50.0,
        lbc_value=10.0,
        rbc_value=10.0,
        user=user,
    )

    sim1.save()
    with pytest.raises(ValidationError) as e:
        sim2.full_clean()

    assert e.value.messages == ["Simulation com este Tag e User já existe."]
