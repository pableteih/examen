from django import forms
from .models import Encuesta, Codigo, Pregunta, Respuesta


class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['nombre', 'premio']


class CodigoForm(forms.ModelForm):
    class Meta:
        model = Codigo
        fields = ['codigo', 'encuesta']


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto']


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['codigo', 'pregunta', 'valor']
        widgets = {
            'valor': forms.Select(choices=Respuesta.NivelSatisfaccion.choices),
        }
