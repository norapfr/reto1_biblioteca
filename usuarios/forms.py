from django import forms
from .models import Socio

class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ['dni', 'nombre', 'apellidos', 'email', 'telefono', 'tipo_usuario']

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if Socio.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Ya existe un usuario con este DNI.")
        return dni
