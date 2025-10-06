from django import forms
from .models import Empleado, Nomina, NominaDetalle

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['cedula', 'nombre', 'sueldo', 'departamento', 'cargo']
        widgets = {
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'sueldo': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class NominaForm(forms.ModelForm):
    class Meta:
        model = Nomina
        fields = ['aniomes']
        widgets = {
            'aniomes': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ej: 202509'}),
        }


class NominaDetalleForm(forms.ModelForm):
    class Meta:
        model = NominaDetalle
        fields = ['empleado', 'bono', 'prestamo']  
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'bono': forms.NumberInput(attrs={'class': 'form-control'}),
            'prestamo': forms.NumberInput(attrs={'class': 'form-control'}),
        }

