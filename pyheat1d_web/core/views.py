from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, resolve_url

from .forms import EditSimulationForm, NewSimulationForm
from .models import Simulation
from .services import create_or_update_simulation_case, delete_simulation_folder, results_times
from .tasks import run_simulation as run_simulation_task


@login_required
def create_simulation_form(request):
    if request.method == "POST":
        form = NewSimulationForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Erro na hora da criação da simulação.")
            return render(
                request,
                "core/create_simulation_form.html",
                context={"form": form},
            )
        new_simulation = form.instance

        new_simulation.user = request.user
        try:
            new_simulation.validate_constraints()
        except ValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)
            return render(
                request,
                "core/create_simulation_form.html",
                context={"form": form},
            )

        # TODO: Tratar o erros que pode contantecer na funcao create
        case_new = create_or_update_simulation_case(form.cleaned_data.copy(), user=request.user)
        new_simulation.input_file = str(case_new)
        new_simulation.save()

        return HttpResponseRedirect(resolve_url("core:list_simulation"))
    else:
        form = NewSimulationForm()

    return render(request, "core/create_simulation_form.html", context={"form": form})


@login_required
def run_simulation(request, pk):
    url_out = resolve_url("core:list_simulation")

    try:
        sim = Simulation.objects.get(id=pk)
    except Simulation.DoesNotExist:
        messages.error(request, f"Simulação com {id} não foi encontrada.")
        return HttpResponseRedirect(url_out)

    if sim.status == Simulation.Status.INIT:
        sim.status = Simulation.Status.RUNNING
        sim.save()
        messages.success(request, f"Simulação {sim.pk} enviada para fila de execução.")
        task = run_simulation_task.delay(simulation_id=pk)
        sim.celery_task = task.id
        sim.save()
    else:
        msg = (
            f"O status da simulação {sim.pk} é '{sim.get_status_display()}'. "
            f"Apenas simulações com status '{Simulation.Status.INIT.label}' ."
        )
        messages.warning(request, msg)

    return HttpResponseRedirect(url_out)


@login_required
def list_simulation(request):
    sim = Simulation.objects.filter(user=request.user).order_by("tag")
    return render(request, "core/list_simulation.html", context={"analysis": sim})


def _recover_info_detail_from_db(sim):
    data = {
        "Id": sim.pk,
        "Tag": sim.tag,
        "Arquivo de entrada": sim.input_file,
        "Status": sim.get_status_display(),
    }

    temporal_dist = {"Delta t": sim.dt, "Passos de tempo": sim.nstep}

    geom = {"Comprimento": sim.length, "Divisões": sim.ndiv}

    bcs = {"Esquerda": sim.lbc_value, "Direita": sim.rbc_value}

    initial_conditions = {"Temperatuta Inicial": sim.initialt}
    return {
        "data": data,
        "bcs": bcs,
        "geom": geom,
        "temporal_dist": temporal_dist,
        "initial_conditions": initial_conditions,
    }


@login_required
def detail_simulation(request, pk):
    sim = Simulation.objects.get(id=pk)

    context = _recover_info_detail_from_db(sim)

    return render(request, "core/detail_simulation.html", context=context)


@login_required
def delete_simulation(request, pk):
    url_out = resolve_url("core:list_simulation")

    try:
        sim = Simulation.objects.get(id=pk)
    except Simulation.DoesNotExist:
        messages.error(request, f"Simulação com {id} não foi encontrada.")
        return HttpResponseRedirect(url_out)

    try:
        delete_simulation_folder(Path(sim.input_file))
    except OSError:  # TODO: Criar um exeção personalizadas
        messages.error(request, f"Não foi possivel deletar o diretório da Simulação {sim.tag}.")
        return HttpResponseRedirect(url_out)

    sim.delete()

    return HttpResponseRedirect(url_out)


@login_required
def results_simulation(request, pk):
    sim = get_object_or_404(Simulation, pk=pk)

    if sim.status == Simulation.Status.SUCCESS:
        isteps = results_times(sim.input_file)

        endpoint = f"/api/results/{pk}/?{request.GET.urlencode()}" if request.GET.urlencode() else f"/api/results/{pk}/"

        context = {
            "id": pk,
            "endpoint": endpoint,
            "isteps": isteps,
            "results_available": True,
        }

        return render(request, "core/results_simulation.html", context)

    context = {"results_available": False}

    return render(request, "core/results_simulation.html", context)


@login_required
def edit_simulation_form(request, pk):
    sim = get_object_or_404(Simulation, id=pk)

    if request.method == "POST":
        form = EditSimulationForm(request.POST, instance=sim)

        if not form.is_valid():
            messages.error(request, "Erro na hora da criação da simulação.")
            return render(
                request,
                "core/edit_simulation_form.html",
                context={"form": form},
            )
        form.instance.status = Simulation.Status.INIT
        form.save()

        case_data = form.cleaned_data.copy()
        create_or_update_simulation_case(case_data, form.instance.user, input_file=Path(sim.input_file))
        messages.success(request, f"Dados da simulação atualizados {sim.tag}")
        return HttpResponseRedirect(resolve_url("core:list_simulation"))
    else:
        form = EditSimulationForm(instance=sim)

    return render(request, "core/edit_simulation_form.html", context={"form": form, "tag": sim.tag})


def redirect_flower(request):
    return HttpResponseRedirect("http://localhost:/flower/")
