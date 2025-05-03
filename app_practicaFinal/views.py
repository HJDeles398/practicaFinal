from .models import ResponsableSala, Sala, Monitor, Actividad, Usuario, Inscripcion
from .forms import ActividadForm, UsuarioForm, MonitorForm, SalaForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


def inicio(request):
    contexto = {'mensaje': '¡Bienvenid@!'}
    return render(request, 'inicio.html', contexto)


# Actividades ---------------------------------------------------------------------
def listar_actividades(request):
    actividades = Actividad.objects.all()

    tipo = request.GET.get('tipo')
    monitor_id = request.GET.get('monitor')

    if tipo:
        actividades = actividades.filter(tipo__iexact=tipo)

    if monitor_id:
        actividades = actividades.filter(monitor_id=monitor_id)

    return render(request, 'actividades/listar_actividades.html', {
        'actividades': actividades,
        'tipo_filtrado': tipo,
        'monitor_filtrado': monitor_id
    })


def nueva_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            actividad = form.save()
            monitor = actividad.monitor
            monitor.numero_actividades = Actividad.objects.filter(monitor=monitor).count()
            monitor.save()
            messages.success(request, "Actividad creada con éxito.")
            return redirect('listar_actividades')
        else:
            messages.error(request, "Error al crear la actividad. Revisa el formulario.")
    else:
        form = ActividadForm()
    return render(request, 'actividades/formulario.html', {'form': form, 'titulo': 'Nueva Actividad'})


def detalle_actividad(request, id):
    actividad = get_object_or_404(
        Actividad.objects.select_related('monitor', 'sala_principal').prefetch_related('salas_secundarias'), id=id)
    return render(request, 'actividades/detalle_actividad.html', {'actividad': actividad})


def editar_actividad(request, id):
    actividad = get_object_or_404(Actividad, id=id)
    monitor_anterior = actividad.monitor

    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            actividad = form.save()
            monitor_nuevo = actividad.monitor

            for monitor in {monitor_anterior, monitor_nuevo}:
                monitor.numero_actividades = Actividad.objects.filter(monitor=monitor).count()
                monitor.save()

            messages.success(request, "Actividad editada con éxito.")
            return redirect('detalle_actividad', id=id)
        else:
            messages.error(request, "Error al editar la actividad.")
    else:
        form = ActividadForm(instance=actividad)
    return render(request, 'actividades/formulario.html', {'form': form, 'titulo': 'Editar Actividad'})


def eliminar_actividad(request, id):
    actividad = get_object_or_404(Actividad, id=id)
    monitor = actividad.monitor

    if request.method == 'POST':
        actividad.delete()
        monitor.numero_actividades = Actividad.objects.filter(monitor=monitor).count()
        monitor.save()
        messages.success(request, "Actividad eliminada correctamente.")
        return redirect('listar_actividades')

    return render(request, 'actividades/confirmar_eliminar.html', {'objeto': actividad, 'tipo': 'Actividad'})


# Usuarios ---------------------------------------------------------------------
def listar_usuarios(request):
    actividad_id = request.GET.get('actividad')
    actividades_disponibles = Actividad.objects.all()

    if actividad_id:
        usuarios = Usuario.objects.filter(actividades__id=actividad_id).distinct()
    else:
        usuarios = Usuario.objects.all()

    return render(request, 'usuarios/listar_usuarios.html', {
        'usuarios': usuarios,
        'actividad_filtrada': actividad_id,
        'actividades_disponibles': actividades_disponibles
    })


def nuevo_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario inscrito con éxito.")
            return redirect('listar_usuarios')
        else:
            messages.error(request, "Error al inscribir el usuario.")
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/formulario.html', {'form': form, 'titulo': 'Nuevo Usuario'})


def detalle_usuario(request, id):
    usuario = get_object_or_404(Usuario.objects.prefetch_related('actividades'), id=id)
    return render(request, 'usuarios/detalle_usuario.html', {'usuario': usuario})


def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario editado correctamente.")
            return redirect('detalle_usuario', id=id)
        else:
            messages.error(request, "Error al editar el usuario.")
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/formulario.html', {'form': form, 'titulo': 'Editar Usuario'})


def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('listar_usuarios')
    return render(request, 'usuarios/confirmar_eliminar.html', {'objeto': usuario, 'tipo': 'Usuario'})


# Monitores ---------------------------------------------------------------------

def listar_monitores(request):
    monitores = Monitor.objects.all()
    return render(request, 'monitores/listar_monitores.html', {'monitores': monitores})


def nuevo_monitor(request):
    if request.method == 'POST':
        form = MonitorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Monitor creado con éxito.")
            return redirect('listar_monitores')
        else:
            messages.error(request, "Error al crear el monitor.")
    else:
        form = MonitorForm()
    return render(request, 'monitores/formulario.html', {'form': form, 'titulo': 'Nuevo Monitor'})


def detalle_monitor(request, id):
    monitor = get_object_or_404(Monitor, id=id)
    return render(request, 'monitores/detalle_monitor.html', {'monitor': monitor})


def editar_monitor(request, id):
    monitor = get_object_or_404(Monitor, id=id)
    if request.method == 'POST':
        form = MonitorForm(request.POST, instance=monitor)
        if form.is_valid():
            form.save()
            messages.success(request, "Monitor editado correctamente.")
            return redirect('detalle_monitor', id=id)
        else:
            messages.error(request, "Error al editar el monitor.")
    else:
        form = MonitorForm(instance=monitor)
    return render(request, 'monitores/formulario.html', {'form': form, 'titulo': 'Editar Monitor'})


def eliminar_monitor(request, id):
    monitor = get_object_or_404(Monitor, id=id)
    if request.method == 'POST':
        monitor.delete()
        messages.success(request, "Monitor eliminado correctamente.")
        return redirect('listar_monitores')
    return render(request, 'monitores/confirmar_eliminar.html', {'objeto': monitor, 'tipo': 'Monitor'})


# Salas ---------------------------------------------------------------------

def listar_salas(request):
    salas = Sala.objects.all()
    return render(request, 'salas/listar_salas.html', {'salas': salas})


def nueva_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            sala = form.save(commit=False)

            nombre_resp = form.cleaned_data['nombre_responsable'].strip()

            responsable = ResponsableSala.objects.filter(nombre__iexact=nombre_resp).exclude(sala__isnull=False).first()

            if not responsable:
                responsable = ResponsableSala.objects.create(nombre=nombre_resp)

            sala.responsable = responsable
            sala.save()

            messages.success(request, "Sala creada con éxito.")
            return redirect('listar_salas')
        else:
            messages.error(request, "Error al crear la sala.")
    else:
        form = SalaForm()
    return render(request, 'salas/formulario.html', {'form': form, 'titulo': 'Nueva Sala'})


def detalle_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    return render(request, 'salas/detalle_sala.html', {'sala': sala})


def editar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            messages.success(request, "Sala editada correctamente.")
            return redirect('detalle_sala', id=id)
        else:
            messages.error(request, "Error al editar la sala.")
    else:
        form = SalaForm(instance=sala)
    return render(request, 'salas/formulario.html', {'form': form, 'titulo': 'Editar Sala'})


def eliminar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        sala.delete()
        messages.success(request, "Sala eliminada correctamente.")
        return redirect('listar_salas')
    return render(request, 'salas/confirmar_eliminar.html', {'objeto': sala, 'tipo': 'Sala'})


# Inscripciones ---------------------------------------------------------------------

def listar_inscripciones(request, id):
    actividad = get_object_or_404(Actividad, id=id)
    inscripciones = Inscripcion.objects.filter(actividad=actividad).select_related('usuario')
    return render(request, 'inscripciones/listar_inscripciones.html', {
        'actividad': actividad,
        'inscripciones': inscripciones
    })


def inscribir_usuario(request, id):
    actividad = get_object_or_404(Actividad, id=id)

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = get_object_or_404(Usuario, id=usuario_id)

        # Verifica que no esté ya inscrito
        if not Inscripcion.objects.filter(usuario=usuario, actividad=actividad).exists():
            Inscripcion.objects.create(usuario=usuario, actividad=actividad)
            messages.success(request, f"{usuario.nombre} inscrito con éxito.")
        else:
            messages.warning(request, f"{usuario.nombre} ya está inscrito en esta actividad.")
        return redirect('listar_inscripciones', id=id)

    usuarios = Usuario.objects.exclude(actividades=actividad)
    return render(request, 'inscripciones/inscribir_usuario.html', {
        'actividad': actividad,
        'usuarios': usuarios
    })


def cancelar_inscripcion(request, id, usuario_id):
    actividad = get_object_or_404(Actividad, id=id)
    usuario = get_object_or_404(Usuario, id=usuario_id)
    inscripcion = get_object_or_404(Inscripcion, actividad=actividad, usuario=usuario)

    if request.method == 'POST':
        inscripcion.delete()
        messages.success(request, f"Inscripción de {usuario.nombre} cancelada.")
        return redirect('listar_inscripciones', id=id)

    return render(request, 'inscripciones/confirmar_cancelar.html', {
        'actividad': actividad,
        'usuario': usuario
    })
