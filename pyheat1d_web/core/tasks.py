from pathlib import Path

from celery import shared_task
from pyheat1d.controllers import run as run_simulation_cli
from pyheat1d.errors import InputFileNotFoundError
from pyheat1d.singleton import Singleton

from pyheat1d_web.core.models import Simulation


@shared_task()
def run_simulation(simulation_id):
    Singleton._instances = {}  # TODO: Gambirra para pode fazer funcionar
    sim = Simulation.objects.get(id=simulation_id)
    msg = None
    try:
        sim.status = Simulation.Status.RUNNING
        run_simulation_cli(input_file=Path(sim.input_file))
    except InputFileNotFoundError as e:
        print(e)  # #TODO: logar
        msg = str(e)
        sim.status = Simulation.Status.FAILED
    else:
        sim.status = Simulation.Status.SUCCESS
    finally:
        sim.save()

    return {"status": sim.get_status_display(), "detail": msg}
