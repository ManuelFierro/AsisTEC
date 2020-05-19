from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group, User ,Permission
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import random 

from Asistencia.models import Asistencia, Alumnos, Docentes, Materias, Horarios

import datetime
import json
import locale
from django.contrib.sessions.backends.db import SessionStore

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
    #hora = datetime.datetime.strptime('2020-05-18 14:00:00', '%Y-%m-%d %H:%M:%S')  #HORA AL MOMENTO PARA LA BD datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #horamax = hora + datetime.timedelta(minutes = 15)  #HORA MAXIMA, HORA AL MOMENTO + 1HR hora + datetime.timedelta(minutes=60)
    #dia = datetime.datetime.now().strftime("%A")
    #horatest = datetime.datetime.strptime('2020-05-18 14:10:10', '%Y-%m-%d %H:%M:%S')  #HORA AL MOMENTO PARA LA BD datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ################################################# #
    #           CREACION DE GRUPOS Y PERMISOS           #
    # ################################################# # 

hora = datetime.datetime.now()  #HORA AL MOMENTO PARA LA BD datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
horamax = hora + datetime.timedelta(minutes = 59)  #HORA MAXIMA, HORA AL MOMENTO + 1HR hora + datetime.timedelta(minutes=60)
dia = datetime.datetime.now().strftime("%A")
print("LA HORA  ",hora)
print("LA HORA MAXIMA ",horamax)
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
    grupo_docentes.permissions.add('2','4','12','14','16',)
    
    # (2, 'Can change alumnos') (4, 'Can view alumnos') (16, 'Can view asistencia') 
    # (8, 'Can view docentes') (12, 'Can view materias')

    #grupo = Group.objects.get(name="docentes").user_set.all()
    #existe = docentes.groups.filter(name='745').exists(
    #print(grupo) 

    # ################################################# #
    #           CREACION DE GRUPOS Y PERMISOS           #
    # ################################################# # 

    print("DOCENTE ACTIVO",session['numero_empleado'])
    
    usuario = authenticate(username=session['numero_empleado'], password=session['numero_empleado'])
    if usuario is not None:                
        login(request, usuario) 
        print("El usuario logeado es : ",usuario.get_username(),usuario.get_short_name()) 

        if usuario.is_authenticated:
            materiaquery = Materias.objects.filter(clave_mae= session['numero_empleado'],horarios__dia=dia,horarios__horaI__lte=hora,horarios__horaF__gte=hora).first()
            print("EL REQUEST ES: ",request.user.username)
            print("MATERIA A ESTA HORA: ",materiaquery)

            if materiaquery: 
                print("MATERIA A ESTA HORA: ",materiaquery.clave_mat)
                session['materia'] = materiaquery.clave_mat
                nombreinicio = ('INICIO'+session['materia'])
                materiaquery = Materias.objects.get(clave_mae=session['numero_empleado'],horarios__dia = dia,horarios__horaI__lte=hora,horarios__horaF__gte=hora)
                horariomateria= Horarios.objects.get(clave_mat = materiaquery,horaI__lte=hora,horaF__gte=hora,dia=dia)
                horaI = horariomateria.horaI
                horaF = horariomateria.horaF
                materia = materiaquery.nom_mat
                print("Docente: ",materiaquery.nom_mat)
                print("HORARIO: ",horariomateria.horaI, " a ",horariomateria.horaF)

                if Asistencia.objects.filter(num_control=nombreinicio,asist= True,fecha__date = hora,clave_matA = session['materia']):
                    horainicio = Asistencia.objects.get(num_control=nombreinicio,asist= True,fecha__date = hora,clave_matA = session['materia'])
                    session["horamax"] = horainicio.fecha + datetime.timedelta(minutes = 15)
                    print("LA HORA MAXIMA ES: ",session["horamax"])
                    print("LA HORA ES:",hora)               

                if hora <= session["horamax"].replace(tzinfo=None):
                    inicio = True
                    nomateria = False
                    print("AUN HAY TIEMPO HASTA LAS",session["horamax"])
                    return render(request,'index2.html',{"materia":materia,"horaI":horaI,"horaF":horaF,"inicio":inicio})            
                else:
                    horaI = "LIBRE"
                    horaF = "LIBRE"
                    materia = "YA TOMO ASISTENCIA"
                    Asistencia.objects.filter(num_control=nombreinicio,asist= True,fecha__date = hora).delete()
                    inicio = False
                    return render(request,'index2.html',{"materia":materia,"horaI":horaI,"horaF":horaF,"inicio":inicio})   
            else:
                horaI = "LIBRE"
                horaF = "LIBRE"
                materia = "NO TIENE MATERIAS AHORA"
                nomateria = True
                Asistencia.objects.filter(num_control__contains="INICIO",asist= True,fecha__date = hora).delete()
                session["horamax"] = hora
                return render(request,'index2.html',{"materia":materia,"horaI":horaI,"horaF":horaF,"nomateria":nomateria})
        else:
            querynom = 'FAVOR DE ESCANEAR SU TARJETA'
            return render(request,'index.html',{"querynom":querynom})

    if request.user.is_anonymous:
        querynom = 'FAVOR DE ESCANEAR SU TARJETA'
        return render(request,'index.html',{"querynom":querynom})
    else:
        querynom = 'FAVOR DE ESCANEAR SU TARJETA'
        return render(request,'index.html',{"querynom":querynom})

@csrf_exempt
def logindocente(request):
    hora = datetime.datetime.now()
    # ################################################## #
    #        LOGEO DOCENTE SOLO PARA PRUEBAS             #
    # ################################################## # 
    nombre = "JESUS SALAS MARIN"
    numero_empleado = 745

    if User.objects.filter(username=numero_empleado).exists(): # EL DOCENTE EXISTE
        docente = authenticate(username=numero_empleado, password=numero_empleado)
        if docente is not None:                    
            login(request, docente)     
            session['nombre'] = nombre
            session['numero_empleado'] = numero_empleado
            
            print("EXISTE Y SE LOGEO DOCENTE: ",session['numero_empleado']," ",session['nombre'])
            print()
    else: # EL DOCENTE NO EXISTE ---> SE CREA
        docente = User.objects.create_user(numero_empleado, nombre ,numero_empleado,first_name=nombre,is_staff=True) # usuario(numero_control), correo, password
        docente = authenticate(request, username=numero_empleado, password=numero_empleado)
        if docente is not None:
            grupo.user_set.add(docente)
            login(request, docente)    
                
            session['nombre'] = nombre
            session['numero_empleado'] = numero_empleado
            print("EXISTE Y SE LOGEO DOCENTE:",session['numero_empleado']," ",session['nombre'])
            print()  

    materiaquery = Materias.objects.filter(clave_mae= session['numero_empleado'],horarios__dia=dia,horarios__horaI__lte=hora,horarios__horaF__gte=hora).first()
    if materiaquery:
        session['materia'] = materiaquery.clave_mat
        print("MATERIA A ESTA HORA: ",materiaquery.clave_mat)
        horariomateria= Horarios.objects.get(clave_mat = materiaquery,horaI__lte=hora,horaF__gte=hora,dia=dia)
        horaI = horariomateria.horaI
        horaF = horariomateria.horaF
        print("HORARIO: ",horariomateria.horaI, " a ",horariomateria.horaF)
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
    print("ALUMNO:",nombre)
    materia = session['materia']
    clave_mae = session['numero_empleado']
    session['numero_empleado'] = clave_mae
    print("CLAVE DE LA MATERIA: ",materia)
    print("CLAVE DEL DOCENTE: ",clave_mae)
    print("DOCENTE ACTIVO: ",session['numero_empleado'])

    materiaquery = Materias.objects.filter(clave_mae = session['numero_empleado'],horarios__dia=dia,horarios__horaI__lte=hora,horarios__horaF__lte=session['horamax']).first()
    print("MATERIA QUERY: ",materiaquery)

    if materiaquery and hora <= session["horamax"].replace(tzinfo=None):
        print("MATERIA A ESTA HORA: ",materiaquery.clave_mat)
        print("AUN ESTAS A TIEMPO")
        print("HORA MAXIMA ",session['horamax'])
        
       #if Alumnos.objects.filter(num_control=numero_control):
            #print("YA ESTA EN LA BD ALUMNOS: ",Alumnos.objects.filter(num_control=numero_control,nom_alu= nombre))
           # print("")
           # print("DOCENTE ACTIVO: ",session['numero_empleado'])
        #else:
           # Alumnos.objects.create(num_control=numero_control,nom_alu= nombre)
           # print("AGREGADO A LA BD ALUMNOS: ",Alumnos.objects.filter(num_control=numero_control,nom_alu= nombre))
      
        if User.objects.filter(username = numero_control):
            borrado = User.objects.filter(username = numero_control)
            borrado.delete()
            print("USUARIO BORRADO")
            print("")

        if Asistencia.objects.filter(num_control=numero_control,clave_matA=session['materia'],fecha__date=hora):
            listachk = Asistencia.objects.get(num_control=numero_control,clave_matA=session['materia'],fecha__date=hora)
            print("YA TOMO LISTA:",listachk.num_control,listachk.nom_alu,listachk.clave_matA,listachk.fecha)
            print("")
            print("DOCENTE ACTIVO: ",session['numero_empleado']," ",session['nombre'])
        else:
            alumno = User.objects.create_user(numero_control, nombre ,numero_control,first_name=nombre, is_staff=True) # usuario(numero_control), correo, password
            alumno = authenticate(username=numero_control, password=numero_control) # YO #
            login(request, alumno)
            materiaObj = Materias.objects.filter(clave_mae=session['numero_empleado'],clave_mat=session['materia']) 
            #alumnosObj = Alumnos.objects.filter(num_control=numero_control) 
            Asistencia.objects.create(num_control=numero_control,nom_alu=nombre,asist= True,fecha= hora,clave_matA = materiaObj[0])                                 
            alumnoAsistencia = Asistencia.objects.get(num_control=numero_control,fecha= hora)
            print("AGREGADO A LA BD ASISTENCIA: ", alumnoAsistencia.num_control,alumnoAsistencia.nom_alu)
            print("")
            print("DOCENTE ACTIVO PRE BORRADO: ",session['numero_empleado']," ",session['nombre'])
            borrado = User.objects.get(username = numero_control)
            borrado.delete()
            borrado.save() 
            print("USUARIO BORRADO")
            print("")
            docentemat = Docentes.objects.get(materias=session['materia'])
            nombreinicio = ('INICIO'+session['materia'])   
            horainicio = Asistencia.objects.get(num_control=nombreinicio,fecha__date= hora,clave_matA=session['materia'])
            print("HORA DE INICIO",horainicio.fecha)
            horamax = horainicio.fecha + datetime.timedelta(minutes = 15)
            print("DOCENTE DE LA MATERIA", docentemat.clave_mae," ",docentemat.nomb_mae)
            session['numero_empleado'] = docentemat.clave_mae
            session['nombre'] = docentemat.nomb_mae
            session['materia'] = materia
            session['horamax'] = horamax
            print("DOCENTE ACTIVO DESPUES BORRADO: ",session['numero_empleado']," ",session['nombre'], session['materia'])
            print("REQUEST: ",request.user.username)
            print("HORA INICIO: ",horainicio.fecha)
            print("HORA MAXIMA: ",session['horamax'])
    else:
        inicio = False
        print("HORA INICIO: ",hora)
        print("INTENTO DE ASISTENCIA",hora)
        print("HORA MAXIMA ",session['horamax'])
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

    #docente = User.objects.create_user(745, "Jesus Salas" ,745,first_name="Jesus Salas",is_staff=True) # usuario(numero_control), correo, password                              
    #usuario = authenticate(username=745, password=745) # 745 es salas #
    #login(request, usuario)
    #session['numero_empleado'] = 745
    #session['nombre'] = 'Jesus Salas'
    #print("Numero de empleado: " ,session['numero_empleado'],"Nombre: ",session['nombre'])
    #print("DOCENTE LOGEADO")
    #grupo.user_set.add(usuario)

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
    if request.method=='POST': #FUNCION PRINCIPAL LECTORA QR
        datosqr = (request.POST['usuario'])
        print("Datos QR",datosqr)
        datosload = json.loads(datosqr)

        if "numero_empleado" in  datosload: #ES DOCENTE 
            nombre = datosload["nombre"]
            numero_empleado = datosload["numero_empleado"]
            materiaquery = Materias.objects.get(clave_mae= session['numero_empleado'],horarios__dia=dia,horarios__hora__gte=hora,horarios__hora__lte=horamax)
            print("MATERIA DEL DIA: ",materiaquery.clave_mat)
            
            horariomateria= Horarios.objects.get(clave_mat = materiaquery,hora__gte=hora,hora__lte=horamax,dia=dia)
            print("HORARIO: ",horariomateria.hora)

            if User.objects.filter(username=numero_empleado).exists(): # EL DOCENTE EXISTE
                docente = authenticate(username=numero_empleado, password=numero_empleado)
                if docente is not None:                    
                    login(request, docente)     
                    session['nombre'] = nombre
                    session['numero_empleado'] = numero_empleado
                    session['materia'] = materiaquery.clave_mat
                    print("EXISTE Y SE LOGEO DOCENTE: ",session['numero_empleado']," ",session['nombre'])
                    print()
                    #return redirect('/')
                   
            else: # EL DOCENTE NO EXISTE ---> SE CREA
                docente = User.objects.create_user(numero_empleado, nombre ,numero_empleado,first_name=nombre,is_staff=True) # usuario(numero_control), correo, password
                docente = authenticate(request, username=numero_empleado, password=numero_empleado)
                if docente is not None:
                        grupo.user_set.add(docente)
                        login(request, docente)    
            
                        session['nombre'] = nombre
                        session['numero_empleado'] = numero_empleado
                        print("EXISTE Y SE LOGEO DOCENTE:",session['numero_empleado']," ",session['nombre'])
                        print()      
                       # return redirect('/')   

        if "numero_control" in datosload: #and User.objects.filter(username=session['numero_empleado'], groups__name='docentes').exists() # ES ALUMNO Y DOCENTE ENTRO
            nombre = datosload["nombre"]
            numero_control = datosload["numero_control"]

            if Alumnos.objects.filter(num_control=numero_control):
                print("YA ESTA EN LA BD ALUMNOS: ",Alumnos.objects.filter(num_control=numero_control,nom_alu=nombre))
                print("")
                print("DOCENTE ACTIVO: ",session['numero_empleado'])
            else:
                Alumnos.objects.create(num_control=numero_control,nom_alu=nombre)
                print("AGREGADO A LA BD: ",Alumnos.objects.filter(num_control=numero_control,nom_alu= nombre))

            if User.objects.filter(username = numero_control):
                borrado = User.objects.get(username = numero_control)
                borrado.delete()
                print("USUARIO BORRADO")
                print("")

            if Asistencia.objects.filter(num_control=numero_control,clave_matA=materia.clave_mat,fecha=fechadb):
                print("YA TOMO ASISTENCIA ESE ALUMNO")
                print("")
                print("DOCENTE ACTIVO: ",session['numero_empleado'])

            else:
                alumno = User.objects.create_user(numero_control,nombre,numero_control,first_name=nombre, is_staff=True) # usuario(numero_control), correo, password
                alumno = authenticate(username=numero_control, password=numero_control) # YO #
                login(request, alumno)
                print("ALUMNO LOGEADO Numero de control: ",numero_control,"Nombre: ",nombre)
                print("")
                materiaObj = Materias.objects.filter(clave_mae="745") #FALTA DEFINIR
                alumnosObj = Alumnos.objects.filter(num_control=numero_control) #FALTA DEFINIR
                Asistencia.objects.create(num_control=alumnosObj[0],asist= True,fecha= fechadb,clave_matA = materiaObj[0])                                
                alumnoAsistencia = Asistencia.objects.get(num_control=numero_control)
                print("AGREGADO A LA BD ASISTENCIA: ", alumnoAsistencia.num_control)
                print("")
                borrado = User.objects.get(username = numero_control)
                borrado.delete()
                print("USUARIO BORRADO")
                print("")
                docente = authenticate(username=session['numero_empleado'], password=session['numero_empleado']) # YO #
                login(request, docente)
                print("DOCENTE ACTIVO: ",session['numero_empleado'])
                return HttpResponse("jalo")

    # ################################################# #
    #                 FUNCION PRINCIPAL                 #
    # ################################################# #

    return HttpResponse('NO DEBERIAS ESTAR AQUI') 

@login_required(login_url='/')
def listado_alumnos(request):

    hora = datetime.datetime.now()
    print("DOCENTE ACTIVO: ",session['numero_empleado'])
    print("Clave de materia: ", session['materia'])

    nombreinicio = ('INICIO'+session['materia'])
    print("nombre inicio",nombreinicio)

    #CREACION DE CONTROL DE INICIO#
    materiaObj = Materias.objects.filter(clave_mae=session['numero_empleado'],clave_mat=session['materia'])
    #alumnosObj = Alumnos.objects.filter(num_control=nombreinicio) 
    if session['materia']:
        if Asistencia.objects.filter(num_control=nombreinicio,asist= True,fecha__date = hora,clave_matA = session['materia']):
            print("YA ESTA CREADO EL INICIO: ",Asistencia.objects.get(num_control=nombreinicio,asist= True,fecha__date= hora,clave_matA = session['materia']))
            horainicio = Asistencia.objects.get(num_control=nombreinicio,asist= True,fecha__date = hora,clave_matA = session['materia'])
            session["horamax"] = horainicio.fecha + datetime.timedelta(minutes = 15)
            print("HORA MAXIMA: ",session["horamax"])
            print("")
        else:
            Asistencia.objects.create(num_control=nombreinicio,asist= True,fecha = hora,clave_matA = materiaObj[0])
            horainicio = Asistencia.objects.get(num_control=nombreinicio,asist= True,fecha__date = hora,clave_matA = session['materia'])
            session["horamax"] = horainicio.fecha + datetime.timedelta(minutes = 15)
            print("HORA INICIO: ",horainicio.fecha)
            print("INICIO CREADO: ",Asistencia.objects.get(num_control=nombreinicio,asist= True,fecha= hora,clave_matA = session['materia']))
        #CREACION DE CONTROL DE INICIO#

        alumno_activo = Asistencia.objects.latest('fecha')
        #asistenciaF = Alumnos.objects.filter(asistencia__fecha__date=hora,asistencia__clave_matA = session['materia']).exclude(num_control=nombreinicio) #ALUMNOS DEL DIA
        asistenciaF = Asistencia.objects.filter(fecha__date=hora,clave_matA = session['materia']).exclude(num_control=nombreinicio) #ALUMNOS DEL DIA
        materia = Materias.objects.get(clave_mat = session['materia'])
        print("Ultimo alumno:" ,alumno_activo)
        print("ALUMNOS ESTE DIA",asistenciaF)
        print("DOCENTE ACTIVO REQUEST" ,request.user.username,request.user.first_name)
    else:
        horaI = "LIBRE"
        horaF = "LIBRE"
        materia = "NO TIENE MATERIAS AHORA"
        nomateria = True
        session["horamax"] = hora
        return render(request,'index2.html',{"materia":materia,"horaI":horaI,"horaF":horaF,"nomateria":nomateria})

    usuario = authenticate(username=session['numero_empleado'], password=session['numero_empleado'])
    if usuario is not None:                
        login(request, usuario)  
        print("El usuario logeado es : ",usuario.get_username(),usuario.get_short_name()) 
        if usuario.is_authenticated:
            print("EL REQUEST ES: ",request.user.username)
            return render(request,'listado_alumnos.html',{"hora":hora,"asistenciaF":asistenciaF,"alumno_activo":alumno_activo,"materia":materia})
        else:
            querynom = 'FAVOR DE ESCANEAR SU TARJETA'
            return render(request,'index.html',{"querynom":querynom})

    return render(request,'listado_alumnos.html',{"hora":hora,"asistenciaF":asistenciaF,"alumno_activo":alumno_activo,"materia":materia})

def resumen_dia(request):
    
    docente = session['numero_empleado'] 
    nom_docente = session['nombre'] 
    materia_clave = session['materia']

    asistenciaF2 = Asistencia.objects.filter(fecha__date=hora,clave_matA = "IFD-1010").exclude(num_control=nombreinicio).values() #ALUMNOS DEL DIA
    nombre = asistenciaF2
    print("Nombre Alumno: ",nombre)

    if Horarios.objects.filter(clave_mat = materia_clave,horaI__lte=hora,horaF__gte=hora,dia=dia).first():
        horarioquery = Horarios.objects.get(clave_mat = materia_clave,horaI__lte=hora,horaF__gte=hora,dia=dia)
        horaI = horarioquery.horaI
        horaF = horarioquery.horaF
        materiaquery = Materias.objects.get(clave_mae=session['numero_empleado'],horarios__dia = dia,horarios__horaI__lte=hora,horarios__horaF__gte=hora)
        materia = materiaquery.nom_mat
        print("Nombre Materia: ",materiaquery.nom_mat)

        asistenciaF = Alumnos.objects.filter(asistencia__fecha__date=hora,asistencia__clave_matA = materia_clave).exclude(num_control=nombreinicio) #ALUMNOS DEL DIA
        asistenciaF2 = Asistencia.objects.filter(fecha__date=hora,clave_matA = materia_clave).exclude(num_control=nombreinicio) #ALUMNOS DEL DIA
        print("asistenciaF QUERY: ",asistenciaF)

        return render(request,'resumen_dia.html',{
            "materia":materiaquery.nom_mat,
            "docente":docente,
            "nom_docente":nom_docente,
            "horaI":horaI,
            "horaF":horaF,
            "queryF":QF,
            "asistenciaF2":asistenciaF2})
    else:
        horaI = "LIBRE"
        horaF = "LIBRE"
        materia = "NO TIENE MATERIAS AHORA"
        nomateria = True
        return render(request,'index2.html',{"materia":materia,"horaI":horaI,"horaF":horaF,"nomateria":nomateria})

def resumen(request):
     
    return render(request,'resumen_completo.html')
