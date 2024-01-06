import json
from functools import partial
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, resolve_url
from pyheat1d.controllers import run as run_simulation_cli
from pyheat1d.singleton import Singleton

from .forms import BC_TYPES, EditSimulationForm, NewSimulationForm
from .models import Simulation


def create_simulation_form(request):
    if request.method == "POST":
        form = NewSimulationForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Erro na hora da criação da simulação.")
            return render(
                request,
                "core/create_simulation_form.html",
                context={"form": form},
                status=400,
            )

        new_case = form.cleaned_data.copy()

        tag = new_case.pop("tag")

        bcs = {
            "lbc": {"type": 1, "params": {"value": new_case.pop("lbc_value")}},
            "rbc": {"type": 1, "params": {"value": new_case.pop("rbc_value")}},
        }

        props = {"k": 1.0, "ro": 1.0, "cp": 1.0}

        new_case.update(bcs)
        new_case.update({"prop": props, "write_every_steps": 100})

        analisys_folder = Path(settings.MEDIA_ROOT) / tag
        if not analisys_folder.exists():
            analisys_folder.mkdir()

        case_file = Path(settings.MEDIA_ROOT) / f"{tag}/case.json"

        json.dump(new_case, case_file.open(mode="w"), indent=2)

        Simulation.objects.create(tag=tag, input_file=case_file)

        return HttpResponseRedirect(resolve_url("core:list_simulation"))
    else:
        form = NewSimulationForm()

    return render(request, "core/create_simulation_form.html", context={"form": form})


def run_simulation(request, pk):
    sim = Simulation.objects.get(id=pk)
    sim.status = Simulation.Status.RUNNING
    sim.save()
    try:
        Singleton._instances = {}  # TODO: Gambirra para pode fazer funcionar
        run_simulation_cli(input_file=Path(sim.input_file))
    except Exception as e:
        messages.error(request, e)
        print(e)  # #TODO: logar
        sim.status = Simulation.Status.FAILED
    else:
        sim.status = Simulation.Status.SUCCESS
    finally:
        sim.save()

    return HttpResponseRedirect(resolve_url("core:list_simulation"))


def list_simulation(request):
    sim = Simulation.objects.all()
    return render(request, "core/list_simulation.html", context={"analysis": sim})


def detail_simulation(request, pk):
    sim = Simulation.objects.get(id=pk)
    case_file = Path(sim.input_file)

    case = json.load(case_file.open(mode="r"))

    data = {
        "Id": sim.pk,
        "Tag": sim.tag,
        "Arquivo de entrada": sim.input_file,
        "Status": sim.get_status_display(),
    }

    temporal_dist = {
        "Delta t": case["dt"],
        "passos de tempo": case["nstep"],
    }

    geom = {
        "Comprimento": case["length"],
        "Divisões": case["ndiv"],
    }

    props = {}

    bcs = {
        "Esquerda": {
            "tipo": BC_TYPES[int(case["lbc"]["type"])],
            "params": case["lbc"]["params"],
        },
        "Direita": {
            "tipo": BC_TYPES[int(case["rbc"]["type"])],
            "params": case["rbc"]["params"],
        },
    }

    initial_conditions = {"Temperatuta Inicial": case["initialt"]}

    context = {
        "data": data,
        "props": props,
        "bcs": bcs,
        "geom": geom,
        "temporal_dist": temporal_dist,
        "initial_conditions": initial_conditions,
    }

    return render(request, "core/detail_simulation.html", context=context)


def delete_simulation(request, pk):
    sim = Simulation.objects.get(id=pk)
    input_file = Path(sim.input_file)

    base_dir = input_file.parent

    input_file.unlink()

    mesh_file = base_dir / "mesh.json"
    if mesh_file.exists():
        mesh_file.unlink()

    results_file = base_dir / "results.json"
    if results_file.exists():
        results_file.unlink()

    base_dir.rmdir()

    sim.delete()

    return HttpResponseRedirect(resolve_url("core:list_simulation"))


# TODO: limitar ao metodo GET
def get_simulation_results_api(request, pk):
    sim = Simulation.objects.get(id=pk)

    input_file = Path(sim.input_file)

    base_dir = input_file.parent

    graphs = {}

    if sim.status == Simulation.Status.SUCCESS:
        mesh_file = base_dir / "mesh.json"
        mesh = json.load(mesh_file.open())
        results_file = base_dir / "results.json"
        results = json.load(results_file.open())

        graphs["mesh"] = list(map(partial(round, ndigits=2), mesh["xp"]))
        graphs["steps"] = [
            {
                "step": results[i]["istep"],
                "t": round(results[i]["t"], 2),
                "u": results[i]["u"],
            }
            for i in [0, 1, -1]
        ]

    return JsonResponse(graphs)


def simulation_results(request, pk):
    return render(request, "core/results_simulation.html", context={"id": pk})


def edit_simulation_form(request, pk):
    sim = Simulation.objects.get(id=pk)
    if request.method == "POST":
        form = EditSimulationForm(request.POST, instance=sim)

        if not form.is_valid():
            messages.error(request, "Erro na hora da criação da simulação.")
            return render(
                request,
                "core/create_simulation_form.html",
                context={"form": form},
                status=400,
            )

        form.save()

        new_case = form.cleaned_data.copy()

        bcs = {
            "lbc": {"type": 1, "params": {"value": new_case.pop("lbc_value")}},
            "rbc": {"type": 1, "params": {"value": new_case.pop("rbc_value")}},
        }

        props = {"k": 1.0, "ro": 1.0, "cp": 1.0}

        new_case.update(bcs)
        new_case.update({"prop": props, "write_every_steps": 100})

        case_file = Path(sim.input_file)

        json.dump(new_case, case_file.open(mode="w"), indent=2)

        return HttpResponseRedirect(resolve_url("core:list_simulation"))
    else:
        form = EditSimulationForm(instance=sim)

    return render(request, "core/edit_simulation_form.html", context={"form": form, "tag": sim.tag})
