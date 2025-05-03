from django.urls import path
from .views import inicio, listar_actividades, nueva_actividad, detalle_actividad, editar_actividad, eliminar_actividad, \
    listar_usuarios, nuevo_usuario, detalle_usuario, editar_usuario, eliminar_usuario, listar_monitores, nuevo_monitor, \
    detalle_monitor, editar_monitor, eliminar_monitor, listar_salas, nueva_sala, detalle_sala, editar_sala, \
    eliminar_sala, listar_inscripciones, inscribir_usuario, cancelar_inscripcion

urlpatterns = [
    path('', inicio, name='inicio'),
    # Actividades
    path('actividades/', listar_actividades, name='listar_actividades'),
    path('actividades/nueva/', nueva_actividad, name='nueva_actividad'),
    path('actividades/<int:id>/', detalle_actividad, name='detalle_actividad'),
    path('actividades/<int:id>/editar/', editar_actividad, name='editar_actividad'),
    path('actividades/<int:id>/eliminar/', eliminar_actividad, name='eliminar_actividad'),

    # Usuarios
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/nuevo/', nuevo_usuario, name='nuevo_usuario'),
    path('usuarios/<int:id>/', detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:id>/editar/', editar_usuario, name='editar_usuario'),
    path('usuarios/<int:id>/eliminar/', eliminar_usuario, name='eliminar_usuario'),

    # Monitores
    path('monitores/', listar_monitores, name='listar_monitores'),
    path('monitores/nuevo/', nuevo_monitor, name='nuevo_monitor'),
    path('monitores/<int:id>/', detalle_monitor, name='detalle_monitor'),
    path('monitores/<int:id>/editar/', editar_monitor, name='editar_monitor'),
    path('monitores/<int:id>/eliminar/', eliminar_monitor, name='eliminar_monitor'),

    # Salas
    path('salas/', listar_salas, name='listar_salas'),
    path('salas/nueva/', nueva_sala, name='nueva_sala'),
    path('salas/<int:id>/', detalle_sala, name='detalle_sala'),
    path('salas/<int:id>/editar/', editar_sala, name='editar_sala'),
    path('salas/<int:id>/eliminar/', eliminar_sala, name='eliminar_sala'),

    # Inscripciones
    path('actividades/<int:id>/inscripciones/', listar_inscripciones, name='listar_inscripciones'),
    path('actividades/<int:id>/inscribir/', inscribir_usuario, name='inscribir_usuario'),
    path('actividades/<int:id>/inscripciones/<int:usuario_id>/eliminar/', cancelar_inscripcion,
         name='cancelar_inscripcion'),

]
