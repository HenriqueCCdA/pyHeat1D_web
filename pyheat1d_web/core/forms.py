from django import forms

from .models import Simulation

BC_TYPES = {1: "Temperatura", 3: "Newton"}


class NewAnalysisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control col-sm-10"

    length = forms.FloatField(
        label="Comprimento",
        initial=1.0,
    )
    ndiv = forms.IntegerField(
        label="Numero de divisões",
        initial=10_000,
    )
    dt = forms.FloatField(
        label="Passo de Tempo",
        initial=1.0,
    )
    nstep = forms.IntegerField(
        label="Número de Passos",
        initial=100,
    )
    initialt = forms.FloatField(
        label="Temperatura Inicial",
        initial=100.0,
    )
    # prop_k = forms.FloatField(
    #     label="Coeficiente de difusão",
    #     initial=1.0,
    # )
    # prop_ro = forms.FloatField(
    #     label="Calor especifico",
    #     initial=1.0,
    # )
    # prop_cp = forms.FloatField(
    #     label="Criando um analise",
    #     initial=1.0,
    # )

    # lbc_type = forms.ChoiceField(
    #     label="Tipo condição de contorno a Esquerda",
    #     required=False,
    #     choices=BC_TYPES,
    # )

    lbc_value = forms.FloatField(
        label="Temperatura a esquerda",
        initial=10.0,
    )

    # rbc_type = forms.ChoiceField(
    #     label="Tipo condição de contorno a Direita",
    #     required=False,
    #     choices=BC_TYPES,
    # )

    rbc_value = forms.FloatField(
        label="Temperatura a direita",
        initial=20.0,
    )

    class Meta:
        model = Simulation
        fields = ("tag",)
