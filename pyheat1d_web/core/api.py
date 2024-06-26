from functools import partial
from http import HTTPStatus
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Simulation
from .services import cleaned_isteps, read_mesh, read_results


@require_http_methods(["GET"])
def simulation_results(request, pk):
    sim = get_object_or_404(Simulation, pk=pk)

    if sim.status == Simulation.Status.SUCCESS:
        input_file = Path(sim.input_file)

        base_dir = input_file.parent

        graphs = {}

        mesh = read_mesh(base_dir)

        results = read_results(base_dir)

        isteps = [0, len(results) // 2, -1]

        if query_list := request.GET.getlist("istep"):
            try:
                isteps = cleaned_isteps(query_list, len(results))
            except ValueError:
                return JsonResponse(
                    {"detail": "Valores invalidos para o passo de tempo."},
                    status=HTTPStatus.UNPROCESSABLE_ENTITY,
                )

        graphs["mesh"] = list(map(partial(round, ndigits=2), mesh["xp"]))
        graphs["steps"] = [
            {
                "step": results[i]["istep"],
                "t": round(results[i]["t"], 2),
                "u": results[i]["u"],
            }
            for i in isteps
        ]

        return JsonResponse(graphs)

    return JsonResponse({"detail": f"Simulação '{sim.tag}' não tem resultados ainda."})
