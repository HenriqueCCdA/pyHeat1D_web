import json
from pathlib import Path

from django.conf import settings


def _get_simulations_base_folder():
    return Path(settings.MEDIA_ROOT)


def create_or_update_simulation_case(new_case, indent=2, update=False):
    bcs = {
        "lbc": {"type": 1, "params": {"value": new_case.pop("lbc_value")}},
        "rbc": {"type": 1, "params": {"value": new_case.pop("rbc_value")}},
    }

    props = {"k": 1.0, "ro": 1.0, "cp": 1.0}

    new_case.update(bcs)
    new_case.update({"prop": props, "write_every_steps": 100})

    tag = new_case.pop("tag")
    base_folder = _get_simulations_base_folder()
    if not update:
        simulation_folder = base_folder / tag
        if not simulation_folder.exists():
            simulation_folder.mkdir(parents=True)

    case_file = base_folder / f"{tag}/case.json"

    # TODO: trata a exceção
    json.dump(new_case, case_file.open(mode="w"), indent=indent)

    return case_file


def delete_simulation_folder(input_file):
    if input_file.exists():
        input_file.unlink()

    base_dir = input_file.parent

    mesh_file = base_dir / "mesh.json"
    if mesh_file.exists():
        mesh_file.unlink()

    results_file = base_dir / "results.json"
    if results_file.exists():
        results_file.unlink()

    base_dir.rmdir()
