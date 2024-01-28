from django import forms

from .models import Simulation

BC_TYPES = {1: "Temperatura", 3: "Newton"}


class NewSimulationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control form-control-sm"

    class Meta:
        model = Simulation
        fields = (
            "tag",
            "length",
            "ndiv",
            "dt",
            "nstep",
            "initialt",
            "lbc_value",
            "rbc_value",
        )


class EditSimulationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control col-sm-10"

    class Meta:
        model = Simulation
        fields = (
            "length",
            "ndiv",
            "dt",
            "nstep",
            "initialt",
            "lbc_value",
            "rbc_value",
        )
