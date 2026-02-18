from django import forms
from .models import Prestamo
from catalogo.models import Ejemplar
from usuarios.models import Socio


class PrestamoForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ['usuario', 'ejemplar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Solo mostrar usuarios activos
        self.fields['usuario'].queryset = Socio.objects.filter(activo=True)

        # ✅ Solo mostrar ejemplares DISPONIBLES
        self.fields['ejemplar'].queryset = Ejemplar.objects.filter(
            estado='DISPONIBLE'
        )
