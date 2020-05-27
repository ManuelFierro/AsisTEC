from django.contrib import admin
from .models import Alumnos, Docentes, Materias, Asistencia

# Register your models here.

class alumnosAdmin(admin.ModelAdmin):
        list_display=("num_control","nom_alu")
        
class docentesAdmin(admin.ModelAdmin):
        list_display=("clave_doc","nom_doc")
        list_filter=("clave_doc","nom_doc")
        search_fields=("clave_doc","nom_doc")


class materiasAdmin(admin.ModelAdmin):
        list_display=("clave_mat","nom_mat","clave_doc")
        list_filter=("clave_mat","nom_mat","clave_doc")
        search_fields=("clave_mat","nom_mat","clave_doc")


class asistenciaAdmin(admin.ModelAdmin):
        list_display=("num_control","asist","fecha","clave_matA")
        list_filter=("asist","fecha","clave_matA")
        search_fields=("num_control","asist","fecha","clave_matA")

admin.site.register(Alumnos,alumnosAdmin)
admin.site.register(Docentes,docentesAdmin)
admin.site.register(Materias,materiasAdmin)
admin.site.register(Asistencia,asistenciaAdmin)