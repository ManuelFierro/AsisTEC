# AsisTEC

Es una version alternativa al proyecto integrador KeyNChek, mantiene la misma idea, mismo proposito, hubo cambios en el momento del desarrollo.
El sistema cuenta con mecanismos para identificar los horarios de los docentes para poder tomar asistencia, asi como metodos pasa visualizar la asistencia de sus alumnos.

### Las partes clave de este proyecto son:
```
Integración de un sistema android y aplicacion web.
Desarrollo en django.
Avisos en tiempo real de los alumnos que toman asistencia.
Detección de horarios
```

### Instrucciones de instalacion:
Instalar dependencias:
```
pipenv shell
pip install django
pip install twisted (si Twisted no se puede instalar revise después de la lista)
pip install channels
pip install channels_redis
pip install xlsxwriter
```

En caso de que no se pueda instalar twisted, descargarlo de este [enlace](https://pypi.org/project/Twisted/#filesy) colocarlo en la raíz del proyecto.
E instalarlo de la siguiente manera
```
pip install “nombredelarchivo”
pip install Twisted-20.3.0-cp38-cp38-win_amd64.whl
```

### Instalar redis server
[Instalador REDIS SERVER](https://github.com/microsoftarchive/redis/releases/tag/win-3.2.100)

Integrantes:
Fierro Cantú Manuel Alejandro

