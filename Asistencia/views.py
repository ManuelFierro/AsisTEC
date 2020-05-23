from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User, Permission
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from calendar import monthrange, monthcalendar
from django.db.models import Count
from Asistencia.models import Asistencia, Alumnos, Docentes, Materias, Horarios

import datetime
import json
import locale
import random
import xlsxwriter
import io
import calendar


session = SessionStore()
session.session_key
session['nombre'] = ''
session['numero_empleado'] = ''
session['materia'] = ''


querynom = 'FAVOR DE ESCANEAR SU TARJETA'
querynum = ''

locale.setlocale(locale.LC_ALL, 'es_MX.utf8')

# ################################################# #
#           CREACION DE GRUPOS Y PERMISOS           #
# ################################################# #
# hora = datetime.datetime.strptime('2020-05-18 14:00:00', '%Y-%m-%d %H:%M:%S')  #HORA AL MOMENTO PARA LA BD datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# horamax = hora + datetime.timedelta(minutes = 15)  #HORA MAXIMA, HORA AL MOMENTO + 1HR hora + datetime.timedelta(minutes=60)
# dia = datetime.datetime.now().strftime("%A")
# horatest = datetime.datetime.strptime('2020-05-18 14:10:10', '%Y-%m-%d %H:%M:%S')  #HORA AL MOMENTO PARA LA BD datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# ################################################# #
#           CREACION DE GRUPOS Y PERMISOS           #
# ################################################# #

# HORA AL MOMENTO PARA LA BD datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hora = datetime.datetime.now()
# HORA MAXIMA, HORA AL MOMENTO + 1HR hora + datetime.timedelta(minutes=60)
horamax = hora + datetime.timedelta(minutes=59)
dia = datetime.datetime.now().strftime("%A")
print("LA HORA  ", hora)
print("LA HORA MAXIMA ", horamax)
session["horamax"] = horamax


def index(request):
    hora = datetime.datetime.now()
    # ################################################# #
    #           CREACION DE GRUPOS Y PERMISOS           #
    # ################################################# #

    #docente = User.objects.create_user(730, "Irma Tinoco Alcazar" ,730,first_name="Irma Tinoco Alcazar",is_staff=True)
    #docente = User.objects.create_user(902, "Rocio Lorena Rodriguez Chacon" ,902,first_name="Rocio Lorena Rodriguez Chacon",is_staff=True)
    #docente = User.objects.create_user(745, "Jesus Salas" ,730,first_name="Jesus Salas",is_staff=True)
    grupo = Group.objects.get(name="docentes")
    grupo_docentes, created = Group.objects.get_or_create(name='docentes')
    grupo_docentes.permissions.add('2', '4', '12', '14', '16',)

    # (2, 'Can change alumnos') (4, 'Can view alumnos') (16, 'Can view asistencia')
    # (8, 'Can view docentes') (12, 'Can view materias')

    #grupo = Group.objects.get(name="docentes").user_set.all()
    # existe = docentes.groups.filter(name='745').exists(
    # print(grupo)

    # ################################################# #
    #           CREACION DE GRUPOS Y PERMISOS           #
    # ################################################# #

    print("DOCENTE ACTIVO", session['numero_empleado'])
    
    usuario = authenticate(
        username=session['numero_empleado'], password=session['numero_empleado'])
    if usuario is not None:
        login(request, usuario)
        print("El usuario logeado es : ",
              usuario.get_username(), usuario.get_short_name())

        if usuario.is_authenticated:
            materiaquery = Materias.objects.filter(
                clave_doc=session['numero_empleado'], horarios__dia=dia, horarios__horaI__lte=hora, horarios__horaF__gte=hora).first()
            print("EL REQUEST ES: ", request.user.username)
            print("MATERIA A ESTA HORA: ", materiaquery)
            
            if materiaquery:
                print("MATERIA A ESTA HORA: ", materiaquery.clave_mat)
                session['materia'] = materiaquery.clave_mat
                nombreinicio = ('INICIO'+session['materia'])  
                inicio = True

                # DATOS GENERALES DE LA MATERIA#              
                horariomateria = Horarios.objects.get(
                    clave_mat=session['materia'], horaI__lte=hora, horaF__gte=hora, dia=dia)
                horaI = horariomateria.horaI
                horaF = horariomateria.horaF
                materia = materiaquery.nom_mat
                session["horafinal"] = horariomateria.horaF
                print("Docente: ", materiaquery.nom_mat)
                print("HORARIO: ", horariomateria.horaI,
                      " a ", horariomateria.horaF)
                print("LA HORA ES:", hora.time())
                # DATOS GENERALES DE LA MATERIA#  

                if Asistencia.objects.filter(num_control=nombreinicio, asist=True, fecha__date=hora, clave_matA=session['materia']):
                    horainicio = Asistencia.objects.get(
                        num_control=nombreinicio, asist=True, fecha__date=hora, clave_matA=session['materia'])
                    session["horamax"] = horainicio.fecha + datetime.timedelta(minutes=15)
                    print("LA HORA MAXIMA ES: ", session["horamax"])
                    print("LA HORA ES:", hora.time())
                    
                if hora <= session["horamax"].replace(tzinfo=None) and inicio == True and hora.time() <= session["horafinal"]:
                    nomateria = False
                    print("FINALIZA A LAS: ", session["horafinal"])
                    print("SE TOMARA LISTA HASTA LAS: ", session["horamax"])
                    return render(request, 'index2.html', {"materia": materia, "horaI": horaI, "horaF": horaF, "inicio": inicio})
                else:
                    if hora >= session["horamax"].replace(tzinfo=None):
                        horaI = "YA SE TOMO LISTA"
                        horaF = "YA SE TOMO LISTA"
                        materia = "YA TOMO ASISTENCIA"
                        print("LA HORA MAXIMA PARA TOMAR LISTA ES: ", session["horamax"])
                        print("LA MATERIA TERMINO A LAS: ", session["horafinal"])
                        print("LA HORA ES:", hora)
                        Asistencia.objects.filter(
                            num_control=nombreinicio, asist=True, fecha__date=hora).delete()
                        session["horamax"] = hora
                        inicio = False
                        nomateria = False
                        return render(request, 'index2.html', {"materia": materia, "horaI": horaI, "horaF": horaF, "inicio": inicio})

                    if hora.time() >= session["horafinal"]:
                        horaI = "SE ACABO LA CLASE"
                        horaF = "SE ACABO LA CLASE"
                        materia = "SE ACABO LA CLASE"
                        print("LA HORA MAXIMA PARA TOMAR LISTA ES: ", session["horamax"])
                        print("LA MATERIA TERMINO A LAS: ", session["horafinal"])
                        print("LA HORA ES:", hora)
                        Asistencia.objects.filter(
                            num_control=nombreinicio, asist=True, fecha__date=hora).delete()
                        inicio = False
                        nomateria = False
                        return render(request, 'index2.html', {"materia": materia, "horaI": horaI, "horaF": horaF, "inicio": inicio})
            else:
                horaI = "LIBRE"
                horaF = "LIBRE"
                materia = "NO TIENE MATERIAS AHORA"
                nomateria = True
                Asistencia.objects.filter(
                    num_control__contains="INICIO", asist=True, fecha__date=hora).delete()
                session["horamax"] = hora
                return render(request, 'index2.html', {"materia": materia, "horaI": horaI, "horaF": horaF, "nomateria": nomateria})
        else:
            querynom = 'FAVOR DE ESCANEAR SU TARJETA'
            return render(request, 'index.html', {"querynom": querynom})

    if request.user.is_anonymous:
        querynom = 'FAVOR DE ESCANEAR SU TARJETA'
        return render(request, 'index.html', {"querynom": querynom})
    else:
        querynom = 'FAVOR DE ESCANEAR SU TARJETA'
        return render(request, 'index.html', {"querynom": querynom})


@csrf_exempt
def logindocente(request):
    hora = datetime.datetime.now()
    # ################################################## #
    #        LOGEO DOCENTE SOLO PARA PRUEBAS             #
    # ################################################## #
    nombre = "JESUS SALAS MARIN"
    numero_empleado = 745

    if User.objects.filter(username=numero_empleado).exists():  # EL DOCENTE EXISTE
        docente = authenticate(username=numero_empleado,
                               password=numero_empleado)
        if docente is not None:
            login(request, docente)
            session['nombre'] = nombre
            session['numero_empleado'] = numero_empleado

            print("EXISTE Y SE LOGEO DOCENTE: ",
                  session['numero_empleado'], " ", session['nombre'])
            print()
    else:  # EL DOCENTE NO EXISTE ---> SE CREA
        # usuario(numero_control), correo, password
        docente = User.objects.create_user(
            numero_empleado, nombre, numero_empleado, first_name=nombre, is_staff=True)
        docente = authenticate(
            request, username=numero_empleado, password=numero_empleado)
        if docente is not None:
            grupo.user_set.add(docente)
            login(request, docente)

            session['nombre'] = nombre
            session['numero_empleado'] = numero_empleado
            print("EXISTE Y SE LOGEO DOCENTE:",
                  session['numero_empleado'], " ", session['nombre'])
            print()

    materiaquery = Materias.objects.filter(
        clave_doc=session['numero_empleado'], horarios__dia=dia, horarios__horaI__lte=hora, horarios__horaF__gte=hora).first()
    if materiaquery:
        session['materia'] = materiaquery.clave_mat
        print("MATERIA A ESTA HORA: ", materiaquery.clave_mat)
        horariomateria = Horarios.objects.get(
            clave_mat=materiaquery, horaI__lte=hora, horaF__gte=hora, dia=dia)
        horaI = horariomateria.horaI
        horaF = horariomateria.horaF
        print("HORARIO: ", horariomateria.horaI, " a ", horariomateria.horaF)
        inicio = True
    else:
        inicio = False
        print("NO HAY MATERIAS A ESTA HORA")
    # ################################################## #
    #        LOGEO DOCENTE SOLO PARA PRUEBAS             #
    # ################################################## #

    return HttpResponse('NO DEBERIAS ESTAR AQUI')


@csrf_exempt
def loginalumno(request):

    # ################################################## #
    #            LOGEO ALUMNO SOLO PARA PRUEBAS          #
    # ################################################## #
    hora = datetime.datetime.now()
    #numerorand = random.randint(17231000, 17231020)
    numero_control = random.randint(17231000, 17231020)
    nombre = ('Alumno'+str(numero_control))
    print("ALUMNO:", nombre)
    
    materia = session['materia']
    clave_doc = session['numero_empleado']
    session['numero_empleado'] = clave_doc
    print("CLAVE DE LA MATERIA: ", materia)
    print("CLAVE DEL DOCENTE: ", clave_doc)
    print("DOCENTE ACTIVO: ", session['numero_empleado'])

    materiaquery = Materias.objects.filter(
        clave_doc=session['numero_empleado'], horarios__dia=dia, horarios__horaI__lte=hora, horarios__horaF__lte=hora).first()
    print("MATERIA QUERY: ", materiaquery)

    if materiaquery and hora <= session["horamax"].replace(tzinfo=None):
        inicio = True
        print("MATERIA A ESTA HORA: ", materiaquery.clave_mat)
        print("AUN ESTAS A TIEMPO")
        print("HORA MAXIMA ", session['horamax'])

       # if Alumnos.objects.filter(num_control=numero_control):
        #print("YA ESTA EN LA BD ALUMNOS: ",Alumnos.objects.filter(num_control=numero_control,nom_alu= nombre))
        # print("")
        # print("DOCENTE ACTIVO: ",session['numero_empleado'])
        # else:
        # Alumnos.objects.create(num_control=numero_control,nom_alu= nombre)
        # print("AGREGADO A LA BD ALUMNOS: ",Alumnos.objects.filter(num_control=numero_control,nom_alu= nombre))

        if User.objects.filter(username=numero_control):
            borrado = User.objects.filter(username=numero_control)
            borrado.delete()
            print("USUARIO BORRADO")
            print("")

        if Asistencia.objects.filter(num_control=numero_control, clave_matA=session['materia'], fecha__date=hora):
            listachk = Asistencia.objects.get(
                num_control=numero_control, clave_matA=session['materia'], fecha__date=hora)
            print("YA TOMO LISTA:", listachk.num_control,
                  listachk.nom_alu, listachk.clave_matA, listachk.fecha)
            print("")
            print("DOCENTE ACTIVO: ",
                  session['numero_empleado'], " ", session['nombre'])
        else:
            # usuario(numero_control), correo, password
            alumno = User.objects.create_user(
                numero_control, nombre, numero_control, first_name=nombre, is_staff=True)
            alumno = authenticate(username=numero_control,
                                  password=numero_control)  # YO #
            login(request, alumno)
            materiaObj = Materias.objects.filter(
                clave_doc=session['numero_empleado'], clave_mat=session['materia'])
            Asistencia.objects.create(
                num_control=numero_control, nom_alu=nombre, asist=True, fecha=hora, clave_matA=materiaObj[0])
            alumnoAsistencia = Asistencia.objects.get(
                num_control=numero_control, fecha=hora)
            print("AGREGADO A LA BD ASISTENCIA: ",
                  alumnoAsistencia.num_control, alumnoAsistencia.nom_alu)
            print("")
            print("DOCENTE ACTIVO PRE BORRADO: ",
                  session['numero_empleado'], " ", session['nombre'])
            borrado = User.objects.get(username=numero_control)
            borrado.delete()
            borrado.save()
            print("USUARIO BORRADO")
            print("")
            docentemat = Docentes.objects.get(materias=session['materia'])
            nombreinicio = ('INICIO'+session['materia'])
            horainicio = Asistencia.objects.get(
                num_control=nombreinicio, fecha__date=hora, clave_matA=session['materia'])
            print("HORA DE INICIO", horainicio.fecha)
            horamax = horainicio.fecha + datetime.timedelta(minutes=15)
            print("DOCENTE DE LA MATERIA", docentemat.clave_doc,
                  " ", docentemat.nom_doc)
            session['numero_empleado'] = docentemat.clave_doc
            session['nombre'] = docentemat.nom_doc
            session['materia'] = materia
            session['horamax'] = horamax
            print("DOCENTE ACTIVO DESPUES BORRADO: ",
                  session['numero_empleado'], " ", session['nombre'], session['materia'])
            print("REQUEST: ", request.user.username)
            print("HORA INICIO: ", horainicio.fecha)
            print("HORA MAXIMA: ", session['horamax'])
    else:
        inicio = False
        print("HORA INICIO: ", hora)
        print("INTENTO DE ASISTENCIA", hora)
        print("HORA MAXIMA ", session['horamax'])
        return HttpResponse("LLEGO TARDE")

    return HttpResponse('RESUMEN:')

    # ################################################## #
    #            LOGEO ALUMNO SOLO PARA PRUEBAS          #
    # ################################################## #


@csrf_exempt
def datos(request):
    grupo, created = Group.objects.get_or_create(name='docentes')
    hora = datetime.datetime.now()

    # ################################################## #
    #  LOGEO DE DOCENTE PREDETERMINADO SOLO PARA PRUEBAS #
    # ################################################## #

    # docente = User.objects.create_user(745, "Jesus Salas" ,745,first_name="Jesus Salas",is_staff=True) # usuario(numero_control), correo, password
    #usuario = authenticate(username=745, password=745) # 745 es salas #
    #login(request, usuario)
    #session['numero_empleado'] = 745
    #session['nombre'] = 'Jesus Salas'
    #print("Numero de empleado: " ,session['numero_empleado'],"Nombre: ",session['nombre'])
    #print("DOCENTE LOGEADO")
    # grupo.user_set.add(usuario)

    # ##################################################################### #
    #                    LISTADO DE TODOS LOS PERMISOS                      #
    #   permissions = [(x.id, x.name) for x in Permission.objects.all()]    #
    #   print(permissions)                                                  #
    #                                                                       #
    #                                                                       #
    #                    LISTADO DE TODOS LOS PERMISOS                      #
    # ##################################################################### #

    # ################################################# #
    #                 FUNCION PRINCIPAL                 #
    # ################################################# #
    print(request.method)
    if request.method == 'POST':  # FUNCION PRINCIPAL LECTORA QR
        datosqr = (request.POST['usuario'])
        print("Datos QR", datosqr)
        datosload = json.loads(datosqr)

        if "numero_empleado" in datosload:  # ES DOCENTE
            nombre = datosload["nombre"]
            numero_empleado = datosload["numero_empleado"]
            materiaquery = Materias.objects.get(
                clave_doc=session['numero_empleado'], horarios__dia=dia, horarios__hora__gte=hora, horarios__hora__lte=horamax)
            print("MATERIA DEL DIA: ", materiaquery.clave_mat)

            horariomateria = Horarios.objects.get(
                clave_mat=materiaquery, hora__gte=hora, hora__lte=horamax, dia=dia)
            print("HORARIO: ", horariomateria.hora)

            # EL DOCENTE EXISTE
            if User.objects.filter(username=numero_empleado).exists():
                docente = authenticate(
                    username=numero_empleado, password=numero_empleado)
                if docente is not None:
                    login(request, docente)
                    session['nombre'] = nombre
                    session['numero_empleado'] = numero_empleado
                    session['materia'] = materiaquery.clave_mat
                    print("EXISTE Y SE LOGEO DOCENTE: ",
                          session['numero_empleado'], " ", session['nombre'])
                    print()
                    # return redirect('/')

            else:  # EL DOCENTE NO EXISTE ---> SE CREA
                # usuario(numero_control), correo, password
                docente = User.objects.create_user(
                    numero_empleado, nombre, numero_empleado, first_name=nombre, is_staff=True)
                docente = authenticate(
                    request, username=numero_empleado, password=numero_empleado)
                if docente is not None:
                    grupo.user_set.add(docente)
                    login(request, docente)

                    session['nombre'] = nombre
                    session['numero_empleado'] = numero_empleado
                    print("EXISTE Y SE LOGEO DOCENTE:",
                          session['numero_empleado'], " ", session['nombre'])
                    print()
                   # return redirect('/')

        # and User.objects.filter(username=session['numero_empleado'], groups__name='docentes').exists() # ES ALUMNO Y DOCENTE ENTRO
        if "numero_control" in datosload:
            nombre = datosload["nombre"]
            numero_control = datosload["numero_control"]

            if Alumnos.objects.filter(num_control=numero_control):
                print("YA ESTA EN LA BD ALUMNOS: ", Alumnos.objects.filter(
                    num_control=numero_control, nom_alu=nombre))
                print("")
                print("DOCENTE ACTIVO: ", session['numero_empleado'])
            else:
                Alumnos.objects.create(
                    num_control=numero_control, nom_alu=nombre)
                print("AGREGADO A LA BD: ", Alumnos.objects.filter(
                    num_control=numero_control, nom_alu=nombre))

            if User.objects.filter(username=numero_control):
                borrado = User.objects.get(username=numero_control)
                borrado.delete()
                print("USUARIO BORRADO")
                print("")

            if Asistencia.objects.filter(num_control=numero_control, clave_matA=materia.clave_mat, fecha=fechadb):
                print("YA TOMO ASISTENCIA ESE ALUMNO")
                print("")
                print("DOCENTE ACTIVO: ", session['numero_empleado'])

            else:
                # usuario(numero_control), correo, password
                alumno = User.objects.create_user(
                    numero_control, nombre, numero_control, first_name=nombre, is_staff=True)
                alumno = authenticate(
                    username=numero_control, password=numero_control)  # YO #
                login(request, alumno)
                print("ALUMNO LOGEADO Numero de control: ",
                      numero_control, "Nombre: ", nombre)
                print("")
                materiaObj = Materias.objects.filter(
                    clave_doc="745")  # FALTA DEFINIR
                alumnosObj = Alumnos.objects.filter(
                    num_control=numero_control)  # FALTA DEFINIR
                Asistencia.objects.create(
                    num_control=alumnosObj[0], asist=True, fecha=fechadb, clave_matA=materiaObj[0])
                alumnoAsistencia = Asistencia.objects.get(
                    num_control=numero_control)
                print("AGREGADO A LA BD ASISTENCIA: ",
                      alumnoAsistencia.num_control)
                print("")
                borrado = User.objects.get(username=numero_control)
                borrado.delete()
                print("USUARIO BORRADO")
                print("")
                docente = authenticate(
                    username=session['numero_empleado'], password=session['numero_empleado'])  # YO #
                login(request, docente)
                print("DOCENTE ACTIVO: ", session['numero_empleado'])
                return HttpResponse("jalo")

    # ################################################# #
    #                 FUNCION PRINCIPAL                 #
    # ################################################# #

    return HttpResponse('NO DEBERIAS ESTAR AQUI')


@login_required(login_url='/')
def listado_alumnos(request):

    hora = datetime.datetime.now()
    print("DOCENTE ACTIVO: ", session['numero_empleado'])
    print("Clave de materia: ", session['materia'])

    nombreinicio = ('INICIO'+session['materia'])
    print("nombre inicio", nombreinicio)

    #CREACION DE CONTROL DE INICIO#
    materiaObj = Materias.objects.filter(
        clave_doc=session['numero_empleado'], clave_mat=session['materia'])
    if session['materia']:
        if Asistencia.objects.filter(num_control=nombreinicio, asist=True, fecha__date=hora, clave_matA=session['materia']):
            print("YA ESTA CREADO EL INICIO: ", Asistencia.objects.get(
                num_control=nombreinicio, asist=True, fecha__date=hora, clave_matA=session['materia']))
            horainicio = Asistencia.objects.get(
                num_control=nombreinicio, asist=True, fecha__date=hora, clave_matA=session['materia'])
            session["horamax"] = horainicio.fecha + \
                datetime.timedelta(minutes=15)
            print("HORA MAXIMA: ", session["horamax"])
            print("")
        else:
            Asistencia.objects.create(
                num_control=nombreinicio, asist=True, fecha=hora, clave_matA=materiaObj[0])
            horainicio = Asistencia.objects.get(
                num_control=nombreinicio, asist=True, fecha__date=hora, clave_matA=session['materia'])
            session["horamax"] = horainicio.fecha + \
                datetime.timedelta(minutes=15)
            print("HORA INICIO: ", horainicio.fecha)
            print("INICIO CREADO: ", Asistencia.objects.get(
                num_control=nombreinicio, asist=True, fecha=hora, clave_matA=session['materia']))
        #CREACION DE CONTROL DE INICIO#

        alumno_activo = Asistencia.objects.latest('fecha')
        # asistenciaF = Alumnos.objects.filter(asistencia__fecha__date=hora,asistencia__clave_matA = session['materia']).exclude(num_control=nombreinicio) #ALUMNOS DEL DIA
        asistenciaF = Asistencia.objects.filter(fecha__date=hora, clave_matA=session['materia']).exclude(
            num_control=nombreinicio)  # ALUMNOS DEL DIA
        materia = Materias.objects.get(clave_mat=session['materia'])
        print("Ultimo alumno:", alumno_activo)
        print("ALUMNOS ESTE DIA", asistenciaF)
        print("DOCENTE ACTIVO REQUEST",
              request.user.username, request.user.first_name)
    else:
        horaI = "LIBRE"
        horaF = "LIBRE"
        materia = "NO TIENE MATERIAS AHORA"
        nomateria = True
        session["horamax"] = hora
        return render(request, 'index2.html', {"materia": materia, "horaI": horaI, "horaF": horaF, "nomateria": nomateria})

    usuario = authenticate(
        username=session['numero_empleado'], password=session['numero_empleado'])
    if usuario is not None:
        login(request, usuario)
        print("El usuario logeado es : ",
              usuario.get_username(), usuario.get_short_name())
        if usuario.is_authenticated:
            print("EL REQUEST ES: ", request.user.username)
            return render(request, 'listado_alumnos.html', {"hora": hora, "asistenciaF": asistenciaF, "alumno_activo": alumno_activo, "materia": materia})
        else:
            querynom = 'FAVOR DE ESCANEAR SU TARJETA'
            return render(request, 'index.html', {"querynom": querynom})

    return render(request, 'listado_alumnos.html', {"hora": hora, "asistenciaF": asistenciaF, "alumno_activo": alumno_activo, "materia": materia})


@login_required(login_url='/')
def resumen_dia(request):
    docente = session['numero_empleado']
    nom_docente = session['nombre']
    materia_clave = session['materia']
    nombreinicio = ('INICIO'+session['materia'])

    asistenciaF2 = Asistencia.objects.filter(fecha__date=hora, clave_matA=materia_clave).exclude(
        num_control=nombreinicio).values()  # ALUMNOS DEL DIA
    nombre = asistenciaF2
    print("QUERY ALUMNOS: ", nombre)

    if Horarios.objects.filter(clave_mat=materia_clave, horaI__lte=hora, horaF__gte=hora, dia=dia).first():
        horarioquery = Horarios.objects.get(
            clave_mat=materia_clave, horaI__lte=hora, horaF__gte=hora, dia=dia)
        horaI = horarioquery.horaI
        horaF = horarioquery.horaF
        materiaquery = Materias.objects.get(
            clave_doc=session['numero_empleado'], horarios__dia=dia, horarios__horaI__lte=hora, horarios__horaF__gte=hora)
        materia = materiaquery.nom_mat
        print("Nombre Materia: ", materiaquery.nom_mat)

        asistenciaF = Asistencia.objects.filter(fecha__date=hora, clave_matA=materia_clave).exclude(
            num_control=nombreinicio)  # ALUMNOS DEL DIA
        print("asistenciaF QUERY: ", asistenciaF)

        return render(request, 'resumen_dia.html', {
            "materia": materiaquery.nom_mat,
            "docente": docente,
            "nom_docente": nom_docente,
            "horaI": horaI,
            "horaF": horaF,
            "dia": hora.strftime("%m-%d"),
            "asistenciaF": asistenciaF})
    else:
        horaI = "LIBRE"
        horaF = "LIBRE"
        materia = "NO TIENE MATERIAS AHORA"
        nomateria = True
        return render(request, 'index2.html', {"materia": materia, "horaI": horaI, "horaF": horaF, "nomateria": nomateria})


@login_required(login_url='/')
def resumen(request):

    if session['materia']:
        materia_clave = session['materia']
    else:
        materias_select = Materias.objects.filter(clave_doc=session['numero_empleado']).first()
        materias_select = session['materia']
        print("MATERIA SI NO HAY SELECT", materias_select)

    docente = session['numero_empleado']
    nom_docente = session['nombre']
    materia_clave = session['materia']
    dia_select = hora.day
    mes_select = hora.month

    materias_select = Materias.objects.filter(
        clave_doc=session['numero_empleado'])
    print("SELECT PARA MATERIAS",  materias_select)

    if request.method == "POST":
        materia_select = request.POST['materias']
        session['materia'] = materia_select
        materia_clave = session['materia']
        print("Materia seleccionada POST:", session['materia'])

    cal = calendar.Calendar()
    dias = cal.itermonthdates(hora.year, hora.month)
    print("Calendario: ", dias)

    asistenciaC = Asistencia.objects.filter(
        clave_matA=materia_clave, fecha__day=dia_select).order_by('fecha')  # ALUMNOS DEL DIA
    print("CLAVE MATERIA AQUI:", materia_clave)
    print("QUERY ALUMNOS: ", asistenciaC)

    if Horarios.objects.filter(clave_mat=materia_clave):
        horarioquery = Horarios.objects.filter(
            clave_mat=materia_clave)
        #horaI = horarioquery.horaI
        #horaF = horarioquery.horaF
        materiaquery = Materias.objects.get(
            clave_doc=session['numero_empleado'], clave_mat=materia_clave)
        materia = materiaquery.nom_mat
        print("Nombre Materia: ", materiaquery.nom_mat)

        return render(request, 'resumen_completo.html', {
            "hora":hora,
            "mes_select":mes_select,
            "materia_clave":materia_clave,
            "materia_nombre": materiaquery.nom_mat,
            "docente": docente,
            "nom_docente": nom_docente,
            "horarioquery": horarioquery,
            "dias": dias,
            "materias_select": materias_select,
            "asistenciaC": asistenciaC})

    return render(request, 'resumen_completo.html', {
        "hora":hora,
        "dia_select":dia_select,
        "mes_select":mes_select,
        "docente": docente,
        "dias": dias,
        "nom_docente": nom_docente,
        "materias_select": materias_select})


@login_required(login_url='/')
def resumenPOST(request):
    docente = session['numero_empleado']
    nom_docente = session['nombre']
    materia_clave = session['materia']
    mes_select = hora.month

    materias_select = Materias.objects.filter(
        clave_doc=session['numero_empleado'])
    print("SELECT PARA MATERIAS", materias_select)

    cal = calendar.Calendar()
    dias = cal.itermonthdates(hora.year, hora.month)
    print("SELECT DIAS: ", dias)

    if Horarios.objects.filter(clave_mat=materia_clave):
        horarioquery = Horarios.objects.filter(
                clave_mat=materia_clave)
        materiaquery = Materias.objects.get(
                clave_doc=session['numero_empleado'], clave_mat=materia_clave)
        print("Nombre Materia: ", materiaquery.nom_mat)
    else:
        aviso = "SELECCIONE UNA MATERIA"
        return render(request, 'resumen_completo.html', {
            "aviso":aviso,
            "hora":hora,
            "mes_select":mes_select,
            "materia_clave":materia_clave,
            "docente": docente,
            "nom_docente": nom_docente,
            "dias": dias,
            "materias_select": materias_select,})

    if request.method == "POST":
        dia_select = request.POST['dia']
        print("FECHA ELEGIDA:", dia_select)

        asistenciaC = Asistencia.objects.filter(
                clave_matA=session['materia'], fecha__day=dia_select).order_by('fecha')  # ALUMNOS DEL DIA

        if asistenciaC:
            print("CLAVE MATERIA POST:", session['materia'])
            print("QUERY ALUMNOS POST: ", asistenciaC)
            return render(request, 'resumen_completo.html', {      
                "hora":hora,
                "mes_select":mes_select,
                "materia_clave":materia_clave,
                "materia_nombre": materiaquery.nom_mat,      
                "docente": docente,
                "nom_docente": nom_docente,
                "horarioquery": horarioquery,
                "dias": dias,
                "materias_select": materias_select,
                "asistenciaC": asistenciaC})   
        else:
            aviso = "NO HUBO ALUMNOS ESE DIA"
            return render(request, 'resumen_completo.html', {
                "aviso":aviso,
                "hora":hora,
                "mes_select":mes_select,
                "materia_clave":materia_clave,
                "materia_nombre": materiaquery.nom_mat,      
                "docente": docente,
                "nom_docente": nom_docente,
                "horarioquery": horarioquery,
                "dias": dias,
                "materias_select": materias_select,
                "asistenciaC": asistenciaC}) 
          

@login_required(login_url='/')
def reporte(request):

    docente = session['numero_empleado']
    nom_docente = session['nombre']
    materia_clave = session['materia']

    if Materias.objects.filter(clave_doc=session['numero_empleado'], clave_mat=materia_clave).first():
        materiaquery = Materias.objects.get(clave_doc=session['numero_empleado'], clave_mat=materia_clave)
        materia_nombre = materiaquery.nom_mat
        print("Nombre Materia: ", materiaquery.nom_mat)
    else:
        return redirect('resumen')

    horarioquery = Horarios.objects.filter(clave_mat=materia_clave).values_list()
    horarioSTR =' '

    for horarios in horarioquery:
        horario = horarios[1]+' '+ str(horarios[2])+'-' + str(horarios[3])
        horarioSTR += ' | '+horario + ' | '
    print("HORARIOS",horarioSTR)
  
    if request.method == "POST":
        mes = request.POST['mes']
        print("MES ELEGIDO:", mes)
    else:
        mes = hora.month

    materia = 'MATERIA : ' + materia_clave +' - '+ materia_nombre
    print("RENGLON MATERIA: " + materia)
    maestro = 'MAESTRO : '+ str(docente) + ' - '+ nom_docente
    print("RENGLON MAESTRO: " + maestro)
    horariosF = 'HORARIO : '+horarioSTR

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(
        output, {'in_memory': True, 'remove_timezone': True})
    worksheet = workbook.add_worksheet('Asistencia')

    worksheet.set_column(0, 0, 3)
    worksheet.set_column(1, 1, 10)
    worksheet.set_column(2, 3, 40)
    worksheet.set_column(3, 35, 3)
    bold = workbook.add_format({'bold': True, 'border': True})
    fullborder = workbook.add_format({'border': True}) 
    noasistio = workbook.add_format({'border': True, 'bg_color': '#FFFFCC'})
    asistio = workbook.add_format({'border': True, 'bg_color': '#CCFFCC'})

    print("Dias en el mes: ", monthrange(hora.year, int(mes))[1])

    dias = monthrange(hora.year, int(mes))[1] + 1
    row = 10
    col = 0
    numero = 1
    coldia = 3
    rowasist = 10
    coldiaA = 3

    worksheet.write(
        'A1', '             INSTITUTO TECNOLÓGICO SUPERIOR DE LERDO')
    worksheet.write('A2', '')
    worksheet.write(
        'A3', 'DEPARTAMENTO ACADEMICO                ACTA DE ASISTENCIA DETALLADA MES '+ mes)
    worksheet.write('A4', 'CONTIENE:        TODOS LOS ALUMNOS')
    worksheet.write(
        'A5', 'CARRERA :      7   ING.INFORMATICA   IINF-2010-220                       PERIODO : ENE-JUN-2020')
    worksheet.write('A6', materia)
    worksheet.write('A7', maestro)
    worksheet.write('A8', horariosF)
    worksheet.write('A10', 'No', bold)
    worksheet.write('B10', 'Num Ctrol', bold)
    worksheet.write('C10', 'Nombre', bold)

    queryalumnos = Asistencia.objects.values('nom_alu', 'num_control', 'asist').annotate(
        Count('id')).order_by().filter(id__count__gt=0,fecha__month=int(mes),clave_matA=materia_clave)

    print("QUERY ALUMNOS", queryalumnos.count())
    conteo_alumnos = queryalumnos.count()

    for dia in range(dias):
        worksheet.write(9, coldia, dia, bold)
        coldia += 1

    for alumno in queryalumnos:
        worksheet.write(row, col, numero, fullborder)
        worksheet.write(row, col + 1, alumno['num_control'], fullborder)
        worksheet.write(row, col + 2, alumno['nom_alu'], fullborder)
        row += 1
        numero += 1
        numero_control = alumno['num_control']
        print("ALUMNO A VERIFICAR ASISTENCIA",
              numero_control, alumno['nom_alu'])

    for alumno in queryalumnos:
        numero_control = alumno['num_control']
        coldiaA = 3
        for dia in range(dias):
            if Asistencia.objects.filter(num_control=numero_control, fecha__month=hora.month, fecha__day=dia,clave_matA=materia_clave):
                Asistencia_Mes = Asistencia.objects.get(
                    num_control=numero_control, fecha__month=hora.month, fecha__day=dia,clave_matA=materia_clave)
                print("ALUMNOS A ESE DIA:", Asistencia_Mes)
                worksheet.write(rowasist, coldiaA, '\U0001F5F8', asistio)
                coldiaA += 1
            else:
                print("NO hubo en este dia", dia)
                worksheet.write(rowasist, coldiaA, '', noasistio)
                coldiaA += 1
        rowasist += 1
    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=Asistencia-'+materia_clave+'-'+mes+'.xlsx'

    return response


def logout_view(request):
    logout(request)
    if request.user.is_anonymous:
        querynom = 'FAVOR DE ESCANEAR SU TARJETA'
        return render(request, 'index.html', {"querynom": querynom})
    else:
        querynom = 'FAVOR DE ESCANEAR SU TARJETA'
        return render(request, 'index.html', {"querynom": querynom})
