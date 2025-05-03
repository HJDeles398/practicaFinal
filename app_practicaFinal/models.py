from django.db import models


class ResponsableSala(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Sala(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    responsable = models.OneToOneField(ResponsableSala, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.ubicacion})"


class Monitor(models.Model):
    nombre = models.CharField(max_length=100)
    especializacion = models.CharField(max_length=100)
    numero_actividades = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion = models.DurationField()
    plazas_disponibles = models.IntegerField()
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    sala_principal = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='actividades_principales')
    salas_secundarias = models.ManyToManyField(Sala, related_name='actividades_secundarias', blank=True)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    actividades = models.ManyToManyField(Actividad, through='Inscripcion')

    def __str__(self):
        return self.nombre


class Inscripcion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} inscrito en {self.actividad}"
