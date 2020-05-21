from django.contrib import admin
from .models import Alumnos, Docentes, Materias, Asistencia

# Register your models here.

class alumnosAdmin(admin.ModelAdmin):
        list_display=("num_control","nom_alu")
        
class docentesAdmin(admin.ModelAdmin):
        list_display=("clave_doc","nom_doc")

class materiasAdmin(admin.ModelAdmin):
        list_display=("clave_mat","nom_mat","clave_doc")

class asistenciaAdmin(admin.ModelAdmin):
        list_display=("num_control","asist","fecha","clave_matA")

admin.site.register(Alumnos,alumnosAdmin)
admin.site.register(Docentes,docentesAdmin)
admin.site.register(Materias,materiasAdmin)
admin.site.register(Asistencia,asistenciaAdmin)