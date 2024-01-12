import json
from functools import partial
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Simulation


@require_http_methods(["GET"])
def simulation_results(request, pk):
    sim = get_object_or_404(Simulation, pk=pk)

    if sim.status == Simulation.Status.SUCCESS:
        input_file = Path(sim.input_file)

        base_dir = input_file.parent

        graphs = {}
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

    return JsonResponse({"detail": f"Simulação '{sim.tag}' não tem resultados ainda."})
