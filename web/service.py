from .models import Encuesta, Codigo, Pregunta, Respuesta
from django.contrib.auth.models import User
import random
import string


class EncuestaService():
    @staticmethod
    def crear_encuesta(nombre, premio, user_id):
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError("Usuario no existe")
        return Encuesta.objects.create(
            nombre=nombre,
            premio=premio,
            user=usuario
        )

    @staticmethod
    def editar_encuesta(encuesta_id, **kwargs):
        try:
            encuesta = Encuesta.objects.get(id=encuesta_id)
            for key, value in kwargs.items():
                setattr(encuesta, key, value)
            encuesta.save()
            return encuesta
        except Encuesta.DoesNotExist:
            raise ValueError("Encuesta no existe")

    @staticmethod
    def eliminar_encuesta(encuesta_id):
        try:
            encuesta = Encuesta.objects.get(id=encuesta_id)
            encuesta.delete()
            return True  # Puedes devolver True o algún indicador de éxito
        except Encuesta.DoesNotExist:
            raise ValueError("Encuesta no existe")


class CodigoService():
    @staticmethod
    def generar_codigo_aleatorio():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    @staticmethod
    def crear_codigos(encuesta_id, cantidad=5):
        encuesta = Encuesta.objects.get(id=encuesta_id)

        codigos = []
        for _ in range(cantidad):
            codigo_aleatorio = CodigoService.generar_codigo_aleatorio()
            codigo = Codigo.objects.create(
                codigo=codigo_aleatorio, encuesta=encuesta)
            codigos.append(codigo)

        return codigos

    @staticmethod
    def eliminar_codigos(codigo_id):
        try:
            codigo = Codigo.objects.get(id=codigo_id)
            codigo.delete()
            return True
        except Codigo.DoesNotExist:
            raise ValueError("Código no existe")


class PreguntaService():
    @staticmethod
    def crear_pregunta(texto, encuesta_id):
        try:
            encuesta = Encuesta.objects.get(
                id=encuesta_id)
        except Encuesta.DoesNotExist:
            raise ValueError("Encuesta no existe")

        pregunta = Pregunta.objects.create(texto=texto, encuesta=encuesta)
        return pregunta

    @staticmethod
    def editar_pregunta(pregunta_id, **kwargs):
        try:
            pregunta = Pregunta.objects.get(id=pregunta_id)
        except Pregunta.DoesNotExist:
            raise ValueError("Pregunta no existe")
        for key, value in kwargs.items():
            setattr(pregunta, key, value)
        pregunta.save()
        return pregunta

    @staticmethod
    def eliminar_pregunta(pregunta_id):
        try:
            pregunta = Pregunta.objects.get(id=pregunta_id)
            pregunta.delete()
            return True
        except Pregunta.DoesNotExist:
            raise ValueError("Pregunta no existe")


class RespuestaService():
    @staticmethod
    def crear_respuesta(codigo_id, pregunta_id, valor):
        try:
            pregunta = Pregunta.objects.get(id=pregunta_id)
        except Pregunta.DoesNotExist:
            raise ValueError("Pregunta no existe")

        try:
            codigo = Codigo.objects.get(id=codigo_id)
        except Codigo.DoesNotExist:
            raise ValueError("Código no existe")

        respuesta = Respuesta.objects.create(
            codigo=codigo,
            pregunta=pregunta,
            valor=valor
        )
        return respuesta

    # no se crará ni editar ni eliminar para que nadie pueda adulterar las respuestas de las encuestas
