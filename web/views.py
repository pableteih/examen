from django.shortcuts import render, redirect, get_object_or_404
from .forms import EncuestaForm, CodigoForm, PreguntaForm, RespuestaForm
from .service import EncuestaService, CodigoService, RespuestaService, PreguntaService
from django.contrib.auth.decorators import login_required
from .models import Encuesta, Codigo, Pregunta, Respuesta
from django.contrib import messages


# Create your views here.


def index(request):
    if request.method == 'POST':
        codigo_input = request.POST.get('codigo', '').strip()
        try:
            codigo_obj = Codigo.objects.get(codigo=codigo_input)
            encuesta = codigo_obj.encuesta
            return redirect('responder_encuesta', encuesta_id=encuesta.id)
        except Codigo.DoesNotExist:
            messages.error(request, "El código ingresado no es válido.")

    return render(request, 'web/index.html')


def responder_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    preguntas = Pregunta.objects.filter(encuesta=encuesta)
    opciones_satisfaccion = Respuesta.NivelSatisfaccion.choices

    if request.method == 'POST':
        codigo_input = request.POST.get('codigo', '').strip()

        try:
            codigo_obj = Codigo.objects.get(
                codigo=codigo_input, encuesta=encuesta)
        except Codigo.DoesNotExist:
            messages.error(
                request, "Código de encuesta no válido o no está asociado con esta encuesta.")
            return redirect('index')

        for pregunta in preguntas:
            respuesta_valor = request.POST.get(f'respuesta_{pregunta.id}')
            if respuesta_valor:
                Respuesta.objects.create(
                    codigo=codigo_obj,
                    pregunta=pregunta,
                    valor=respuesta_valor
                )
        messages.success(
            request, "Tus respuestas han sido guardadas exitosamente.")
        return redirect('index')

    context = {
        'encuesta': encuesta,
        'preguntas': preguntas,
        'opciones_satisfaccion': opciones_satisfaccion,
    }
    return render(request, 'web/responder_encuesta.html', context)


@login_required
def crear_encuesta(request):
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.user = request.user
            encuesta.save()
            messages.success(
                request, "La encuesta ha sido creada exitosamente")
            return redirect('lista_encuestas')
    else:
        form = EncuestaForm()
    return render(request, 'web/crear_encuesta.html', {'form': form})


@login_required
def listar_encuestas(request):
    encuestas = Encuesta.objects.filter(user=request.user)
    context = {'encuestas': encuestas}
    return render(request, 'web/lista_encuestas.html', context)


@login_required
def editar_encuesta(request, id):
    try:
        encuesta = Encuesta.objects.get(id=id)
    except Encuesta.DoesNotExist:
        messages.error(request, "La encuesta no existe")
        return redirect('index')

    if request.method == 'POST':
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            messages.success(
                request, "La encuesta ha sido actualizada exitosamente")
            return redirect('index')
    else:
        form = EncuestaForm(instance=encuesta)
    return render(request, 'web/editar_encuesta.html', {'form': form})


@login_required
def eliminar_encuesta(request, id):
    try:
        encuesta = Encuesta.objects.get(id=id)
    except Encuesta.DoesNotExist:
        messages.error(request, "La encuesta no existe")
        return redirect('index')

    if request.method == 'POST':
        encuesta.delete()
        messages.success(request, "La encuesta ha sido eliminada")
        return redirect('lista_encuestas')

    return redirect('index')


@login_required
def crear_pregunta(request, id):
    try:
        encuesta = Encuesta.objects.get(id=id)
    except Encuesta.DoesNotExist:
        messages.error(request, "La encuesta no existe")
        return redirect('index')

    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.encuesta = encuesta
            pregunta.save()
            messages.success(
                request, "La pregunta ha sido creada exitosamente")
            return redirect('listar_preguntas', encuesta_id=encuesta.id)
    else:
        form = PreguntaForm()
    return render(request, 'web/crear_pregunta.html', {'form': form, 'encuesta': encuesta})


@login_required
def listar_preguntas(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    preguntas = Pregunta.objects.filter(encuesta=encuesta_id)
    context = {'preguntas': preguntas, 'encuesta': encuesta}
    return render(request, 'web/listar_preguntas.html', context)


@login_required
def editar_pregunta(request, id):
    pregunta = get_object_or_404(Pregunta, id=id)
    encuesta = pregunta.encuesta

    if request.method == 'POST':
        form = PreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            messages.success(request, "Pregunta actualizada exitosamente")
            return redirect('listar_preguntas', encuesta_id=encuesta.id)
    else:
        form = PreguntaForm(instance=pregunta)

    return render(request, 'web/editar_pregunta.html', {'form': form, 'encuesta': encuesta})


@login_required
def eliminar_pregunta(request, id):
    pregunta = get_object_or_404(Pregunta, id=id)
    encuesta_id = pregunta.encuesta.id

    if request.method == 'POST':
        pregunta.delete()
        messages.success(request, "La pregunta ha sido eliminada exitosamente")
        return redirect('listar_preguntas', encuesta_id=encuesta_id)
    else:
        messages.error(request, "Método no permitido")

    return redirect('listar_preguntas')


@login_required
def crear_codigos(request, id):
    encuesta = get_object_or_404(Encuesta, id=id)

    if request.method == 'POST':
        try:
            CodigoService.crear_codigos(encuesta_id=encuesta.id, cantidad=5)
            messages.success(
                request, "Los códigos han sido creados exitosamente")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('crear_codigos', id=encuesta.id)

    codigos_generados = Codigo.objects.filter(encuesta=encuesta)

    return render(request, 'web/crear_codigos.html', {'codigos_generados': codigos_generados, 'encuesta': encuesta})


@login_required
def crear_respuesta(request, codigo_id, pregunta_id):
    try:
        codigo = Codigo.objects.get(id=codigo_id)
    except Codigo.DoesNotExist:
        messages.error(request, "codigo no existe")
        return redirect('index')
    try:
        pregunta = Pregunta.objects.get(id=pregunta_id)
    except Pregunta.DoesNotExist:
        messages.error(request, "Pregunta no existe")
        return redirect('index')

    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.codigo = codigo
            respuesta.pregunta = pregunta
            respuesta.save()
            messages.success(
                request, "La respuesta ha sido enviada exitosamente")
            return redirect('index')
    else:
        form = RespuestaForm()
    return render(request, 'web/crear_respuesta.html', {'form': form})


@login_required
def listar_respuestas(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    respuestas = Respuesta.objects.filter(pregunta=pregunta)
    context = {'pregunta': pregunta, 'respuestas': respuestas}
    return render(request, 'web/listar_respuestas.html', context)
