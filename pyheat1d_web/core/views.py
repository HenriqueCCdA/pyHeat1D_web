import json
from pathlib import Path

from django.conf import settings
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages

from django.shortcuts import render, resolve_url

BC_TYPES = {1: "Temperatura", 3: "Newton"}


analises = []


class NewAnalysisForm(forms.Form):
    tag = forms.CharField(label='Tag da simulação', initial="sim_01")
    length = forms.FloatField(label="Comprimento", initial=1.0)
    div = forms.IntegerField(label="Numero de divisões", initial=2)
    dt = forms.FloatField(label="Passo de Tempo", initial=1.0)
    nstep = forms.IntegerField(label="Número de Passos", initial=2)
    initialt = forms.FloatField(label="Temperatura Inicial", initial=1.0)
    prop_k = forms.FloatField(label="Coeficiente de difusão", initial=1.0)
    prop_ro = forms.FloatField(label="Calor especifico", initial=1.0)
    prop_cp = forms.FloatField(label="Criando um analise", initial=1.0)

    lbc_type = forms.ChoiceField(
        label="Tipo condição de contorno a Esquerda",
        required=False,
        choices=BC_TYPES,
    )

    lbc_value = forms.FloatField(
        label="Valor da condição de contorno a Esquerda",
        initial=10.0,
    )

    rbc_type = forms.ChoiceField(
        label="Tipo condição de contorno a Direita",
        required=False,
        choices=BC_TYPES,
    )
    rbc_value = forms.FloatField(
        label="Valor da condição de contorno a Direita",
        initial=20.0,
    )


def create_analysis_form(request):

    if request.method == 'POST':

        form = NewAnalysisForm(request.POST)

        if not form.is_valid():
            return HttpResponseRedirect(
                resolve_url('core:create_analysis_form'),
                context={"form": form },
                status=400,
            )

        new_case = form.cleaned_data.copy()

        tag = new_case.pop('tag')

        bcs = {
            "lbc": {
                "type": new_case.pop('lbc_type'),
                "params": {
                    "value": new_case.pop('lbc_value')
                }
            },
            "rbc": {
                "type": new_case.pop('rbc_type'),
                "params": {
                    "value": new_case.pop('rbc_value'),
                    "h": 1.0
                }
            },
        }

        new_case.update(bcs)

        if tag in analises:
            messages.success(request, 'Já existe simulação essa tag')
            return render(request, "core/create_analysis_form.html", context={"form": form})

        analises.append(tag)

        analisys_folder = Path(settings.MEDIA_ROOT)
        if not analisys_folder.exists():
            analisys_folder.mkdir()

        case_file = Path(settings.MEDIA_ROOT) / f"{tag}.json"

        json.dump(new_case, case_file.open(mode="w"), indent=2)

        return HttpResponseRedirect(resolve_url('core:analysis_list'))
    else:
        form = NewAnalysisForm()

    return render(request, "core/create_analysis_form.html", context={"form": form})


def run_analysis(request, tag):
    print(f"run {tag}")
    return HttpResponseRedirect(resolve_url('core:analysis_list'))


def analysis_list(request):
    return render(request, "core/analysis_list.html", context={'analysis': analises})


def analysis_detail(request, tag):
    case_file = Path(settings.MEDIA_ROOT) / f"{tag}.json"

    print(json.load(case_file.open(mode="r")))
    return HttpResponseRedirect(resolve_url('core:analysis_list'))
