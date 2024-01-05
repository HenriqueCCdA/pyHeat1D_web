from django import forms

from .models import Simulation

BC_TYPES = {1: "Temperatura", 3: "Newton"}


class NewSimulationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control col-sm-10"

    length = forms.FloatField(label="Comprimento", initial=1.0)
    ndiv = forms.IntegerField(label="Numero de divisões", initial=100_000)
    dt = forms.FloatField(label="Passo de Tempo", initial=0.0001)
    nstep = forms.IntegerField(label="Número de Passos", initial=10_000)
    initialt = forms.FloatField(label="Temperatura Inicial", initial=100.0)

    lbc_value = forms.FloatField(label="Temperatura a esquerda", initial=0.0)

    rbc_value = forms.FloatField(label="Temperatura a direita", initial=0.0)

    class Meta:
        model = Simulation
        fields = ("tag",)


class EditSimulationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control col-sm-10"

    length = forms.FloatField(label="Comprimento")
    ndiv = forms.IntegerField(label="Numero de divisões")
    dt = forms.FloatField(label="Passo de Tempo")
    nstep = forms.IntegerField(label="Número de Passos")
    initialt = forms.FloatField(label="Temperatura Inicial")
    lbc_value = forms.FloatField(label="Temperatura a esquerda")
    rbc_value = forms.FloatField(label="Temperatura a direita")
