from django import forms
from .models import Titulo, Ejemplar


class TituloForm(forms.ModelForm):
    cantidad_ejemplares = forms.IntegerField(
        min_value=1,
        label="Cantidad de ejemplares",
        required=True
    )
    class Meta:
        model = Titulo
        fields = ['titulo', 'autor', 'isbn', 'categoria']

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if Titulo.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError("Ya existe un título con este ISBN.")
        return isbn


class EjemplarForm(forms.ModelForm):
    class Meta:
        model = Ejemplar
        fields = ['codigo_interno', 'titulo']

    def clean_codigo_interno(self):
        codigo = self.cleaned_data.get('codigo_interno')
        if Ejemplar.objects.filter(codigo_interno=codigo).exists():
            raise forms.ValidationError("Ya existe un ejemplar con este código.")
        return codigo
