from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Encuesta(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    premio = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Codigo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo


class Pregunta(models.Model):
    texto = models.TextField(null=False)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    class NivelSatisfaccion(models.IntegerChoices):
        MUY_DESACUERDO = 1, 'Muy en desacuerdo'
        DESACUERDO = 2, 'En desacuerdo'
        NEUTRO = 3, 'Ni de acuerdo ni en desacuerdo'
        ACUERDO = 4, 'De acuerdo'
        MUY_ACUERDO = 5, 'Muy de acuerdo'

    codigo = models.ForeignKey(Codigo, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    valor = models.IntegerField(choices=NivelSatisfaccion.choices)

    def __str__(self):
        return self.get_valor_display()
