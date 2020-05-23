from django.db import models

# Create your models here.

class Alumnos(models.Model):
    num_control=models.CharField(
        max_length=30,
        primary_key=True,
        verbose_name="Número de Control")
    nom_alu=models.CharField(
        max_length=30,
        verbose_name="Nombre del Alumno")
    semestre=models.IntegerField()

    def __str__(self):
        return '%s, %s' %(self.num_control, self.nom_alu)

class Docentes(models.Model):
    clave_doc=models.CharField(
        max_length=3,
        primary_key=True,
        verbose_name="Clave del Maestro")
    nom_doc=models.CharField(
        max_length=30,
        verbose_name="Nombre del Maestro")

    def __str__(self):
        return '%s, %s' %(self.clave_doc, self.nom_doc)

class Materias(models.Model):
    clave_mat=models.CharField(
        max_length=30,
        primary_key=True,
        verbose_name="Clave de la Materia")
    semestre=models.IntegerField(
        verbose_name="Clave de la Materia")
    nom_mat=models.CharField(
        max_length=80,
        verbose_name="Nombre de la Materia")
    clave_doc = models.ForeignKey(
        'Docentes',
        on_delete=models.CASCADE,
        verbose_name="Datos del Maestro")

    def __str__(self):
        return '%s, %s, %s' %(self.clave_mat, self.nom_mat,self.clave_doc)

class Asistencia(models.Model):
    nom_alu=models.CharField(
        max_length=30,
        verbose_name="Nombre del Alumno")
    asist=models.BooleanField()
    fecha=models.DateTimeField() 
    num_control=models.CharField(
        max_length=30,
        verbose_name="Número de Control/Nombre") 
    clave_matA=models.ForeignKey(
        'Materias',
        on_delete=models.CASCADE,
        verbose_name="Datos de la materia")
    
    def __str__(self):
        return '%s, %s, %s, %s, %s' %(self.num_control,self.nom_alu,self.asist,self.fecha,self.clave_matA)

class Horarios(models.Model):
    dia=models.CharField(
        max_length=30)
    horaI=models.TimeField()
    horaF=models.TimeField()
    clave_mat=models.ForeignKey(
        'Materias',
        on_delete=models.CASCADE,
        verbose_name="Datos de la materia")
    
    def __str__(self):
        return '%s, %s, %s, %s' %(self.dia, self.horaI,self.horaF,self.clave_mat)