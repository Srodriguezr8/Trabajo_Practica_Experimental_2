from django import forms
from .models import Sobretiempo

class SobretiempoForm(forms.ModelForm):
    class Meta:
        model = Sobretiempo
        fields = ["empleado", "fecha_registro", "tipo_sobretiempo", "numero_horas"]
        widgets = {
            "fecha_registro": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_numero_horas(self):
        horas = self.cleaned_data.get("numero_horas")
        if horas <= 0:
            raise forms.ValidationError("El número de horas debe ser mayor a 0.")
        return horas
    
    
