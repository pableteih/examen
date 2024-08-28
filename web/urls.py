from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),



    # URLs para encuestas
    path('encuestas/crear/', views.crear_encuesta, name='crear_encuesta'),
    path('encuestas/listar/', views.listar_encuestas, name='lista_encuestas'),
    path('encuestas/editar/<int:id>/',
         views.editar_encuesta, name='editar_encuesta'),
    path('encuestas/eliminar/<int:id>/',
         views.eliminar_encuesta, name='eliminar_encuesta'),

    # URLs para preguntas
    path('preguntas/crear/<int:id>/', views.crear_pregunta, name='crear_pregunta'),
    path('preguntas/listar/<int:encuesta_id>/',
         views.listar_preguntas, name='listar_preguntas'),

    path('preguntas/editar/<int:id>/',
         views.editar_pregunta, name='editar_pregunta'),
    path('preguntas/eliminar/<int:id>/',
         views.eliminar_pregunta, name='eliminar_pregunta'),

    # URLs para respuestas
    path('respuestas/crear/<int:codigo_id>/<int:pregunta_id>/',
         views.crear_respuesta, name='crear_respuesta'),
    path('respuestas/listar/<int:pregunta_id>/',
         views.listar_respuestas, name='ver_respuestas'),
    path('encuesta/responder/<int:encuesta_id>/',
         views.responder_encuesta, name='responder_encuesta'),



    # URLs para códigos
    path('codigos/crear/<int:id>/', views.crear_codigos, name='crear_codigos'),
]
