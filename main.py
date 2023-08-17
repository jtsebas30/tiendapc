from flask import Flask, render_template, request, session, redirect, url_for, flash
from bdd import *
from datetime import datetime
import aiml
from bdmetricas import *
import time

app = Flask(__name__)
app.secret_key = 'tid@205'

# Crea el objeto Kernel de AIML y carga los archivos AIML
kernel = aiml.Kernel()
kernel.learn("bot.aiml")


@app.route('/metricas')

def metricas() -> 'html':

  d_entendibilidad=verEntendibilidad()
  d_efectividad=verEfectividad()
  d_eficiencia=verEficiencia()


  return render_template('admin/metricas.html',titulo ='Metricas',ent=d_entendibilidad,efc=d_efectividad,efa=d_eficiencia)

@app.route('/')

def index() -> 'html':
  return render_template('invitado/index.html',titulo ='Inicio')


@app.route('/qc')

def index_qc() -> 'html':
  return render_template('invitado/index_qc.html',titulo ='Kallariy')


@app.route('/ch')

def index_ch() -> 'html':
  return render_template('invitado/index_ch.html',titulo ='开始')


@app.route('/fr')

def index_fr() -> 'html':
  return render_template('invitado/index_fr.html',titulo ='Début')



@app.route("/get_response", methods=["POST"])
def get_response():

    user_message = request.form["user_message"]
    response = kernel.respond(user_message)
    return str(response)


@app.route("/get_response_c", methods=["POST"])
def get_response_c():
  user_message = request.form["user_message"]
  response = kernel.respond(user_message)
  print("INGRESO AL CHATBOT DE CLIENTE")
  snayudas = int(session['e_nayudas']) + 1
  session['e_nayudas'] = snayudas  # Variable que al terminar la session se carga en BD.
  return str(response)


@app.route('/info')

def info() -> 'html':
  return render_template('invitado/ayudas.html',titulo ='Ayudas')

@app.route('/login')

def login() -> 'html':
  return render_template('invitado/login.html',titulo ='Iniciar Sesion')

@app.route('/registro')

def registro() -> 'html':
  provincias_ecuador = [
    "Azuay",
    "Bolívar",
    "Cañar",
    "Carchi",
    "Chimborazo",
    "Cotopaxi",
    "El Oro",
    "Esmeraldas",
    "Galápagos",
    "Guayas",
    "Imbabura",
    "Loja",
    "Los Ríos",
    "Manabí",
    "Morona Santiago",
    "Napo",
    "Orellana",
    "Pastaza",
    "Pichincha",
    "Santa Elena",
    "Santo Domingo de los Tsáchilas",
    "Sucumbíos",
    "Tungurahua",
    "Zamora Chinchipe"
  ]

  return render_template('invitado/registro.html',titulo ='Registro',pr=provincias_ecuador)

@app.route('/catalogo')

def catalogo() -> 'html':

  data=verproductos()
  data1=verCatalogoFiltado("Asus")
  data2=verCatalogoFiltado("Lenovo")
  data3=verCatalogoFiltado("Dell")
  return render_template('invitado/catalogo.html',titulo ='Nuestros Productos',data=data,data1=data1,data2=data2,data3=data3)

@app.route('/detalle',methods=['GET'])

def catalogo_detalle() -> 'html':

  id = request.args.get('id')
  data=verproductos_detalle(id)

  return render_template('invitado/dcatalogo.html',titulo =data[0][1],data=data)

@app.route('/newuser',methods=['POST'])
def nuevouser()->'html':
  cedula = request.form.get('cedula')
  nombre = request.form.get('nombre')
  apellido = request.form.get('apellido')
  provincia = request.form.get('provincia')
  domicilio = request.form.get('domicilio')
  correo = request.form.get('correo')
  clave = request.form.get('contrasenia')



  v_cedula=validar_userxcedula(cedula)
  v_correo=validar_correo(correo)


  if v_cedula !=[]:

    flash('<div class="alert alert-danger d-flex align-items-center" role="alert">'
          '<div>Error ya existe un usuario registrado con la cedula : ' + cedula +
          '</div>'
          '</div>')
    return redirect(url_for('registro'))
  else :
    bced = True

  if v_correo !=[]:
    flash('<div class="alert alert-danger d-flex align-items-center" role="alert">'
          '<div> <i class="bi bi-exclamation-diamond-fill"></i> Error ya existe un usuario registrado con el correo: ' + correo +
          '</div>'
          '</div>')
    return redirect(url_for('registro'))
  else:
    bcor = True


  if bced and bcor:
    res = nuevousuario(cedula, nombre, apellido, provincia, domicilio, correo, clave)

  if res :
    flash('<div class="alert alert-success d-flex align-items-center" role="alert">'
          '<div> Usuario registrado correctamente, clic para <a href="/login"> Iniciar Sesion </a>'
          '</div>'
          '</div>')
    return redirect(url_for('registro'))
  else:
    return redirect(url_for('registro'))

#####RUTAS CON SESION

@app.route('/ingreso',methods=['POST'])
def ingresou()->'html':
  correo = request.form.get('correo')
  clave = request.form.get('contrasenia')

  data=validar_user(correo,clave)
  #print(data)

  if data !=[]:
    # Variables de Sesion
    session['nombres']=data[0][1]+" "+data[0][2]
    session['cedula']=data[0][0]
    session['correo']=correo

    #Cuando se valida el ingreso se inicializan las variables de metricas para cada categoria

    # Enceramiento de variables para calculo de metricas
    # ENTENDIBILIDAD
    session['e_nayudas'] = 0
    session['e_pcerradas'] = 0
    session['e_nerrores'] = 0
    session['e_tiempop'] = 0
    session['init_tiempo']=time.time()

    #EFECTIVIDAD
    session['ef_transaccionesd']=0
    session['ef_sesionesd']=0

    #EFICIENCIA

    session['efc_tiempoinicio']=time.time() #Se inicia el conteo desde que inicia la sesion y finaliza hasta q se complete una compra.
    session['efc_tiempometrica']=0
    session['efc_ntransacciones']=0
    session['tiempo_paginas_init']=0
    ###########################

    return redirect(url_for('index_cliente'))
  else:
    flash('Error: Verifique que el correo y la contraseña se han correctos', 'error')
    return redirect(url_for('login'))

@app.route('/cinicio')

def index_cliente() -> 'html':

  if 'cedula' in session:

    return render_template('cliente/index.html',titulo ='Bienvenido '+session['nombres'],nom=session['nombres'])

  else :

    return redirect(url_for('index'))

@app.route('/cayudas')
def ayudas()->'html':
  if 'cedula' in session:

    # metrica veces que el usuario accede a ayudas en linea
    snayudas=int(session['e_nayudas'])+1
    session['e_nayudas']=snayudas #Variable que al terminar la session se carga en BD.


    return render_template('cliente/ayudas.html', titulo='Ayudas en Linea')

  else:

    return redirect(url_for('index'))

@app.route('/ccatalogo')
def catalogo_cliente()->'html':
  if 'cedula' in session:

    data = verproductos()
    data1 = verCatalogoFiltado("Asus")
    data2 = verCatalogoFiltado("Lenovo")
    data3 = verCatalogoFiltado("Dell")

    #Metrica de Entendibilidad :
    #Tiempo que pasa entre cambio de pagina de inicio a catalogo

    times=session['init_tiempo']
    calculo_tiempo=round(time.time()-times)

    if session['e_tiempop'] == 0:
      session['e_tiempop']=calculo_tiempo


    return render_template('cliente/catalogo.html', titulo='Catalogo de Productos',data=data,data1=data1,data2=data2,data3=data3)

  else:

    return redirect(url_for('index'))


@app.route('/ccatalogod',methods=['GET'])
def detallecatalogo()->'html':
  if 'cedula' in session:
    id=request.args.get('id')
    data = verproductos_detalle(id)


    return render_template(
      'cliente/detallecatalogo.html',
      data=data,
      titulo=data[0][1],
      nom=session['nombres'],
      cor=session['correo'],
      ced=session['cedula']
    )

  else:

    return redirect(url_for('index'))

@app.route('/solicitud',methods=['POST'])
def agregasolicitud()->'html':
  if 'cedula' in session:
    nombre = request.form.get('nombre')
    cedula = request.form.get('cedula')
    correo = request.form.get('correo')
    producto = request.form.get('producto')
    fecha_actual = datetime.now().date()

    res=solicitud_ingreso(nombre,cedula,correo,producto,fecha_actual)

    if res:
      flash("Solicitud Ingresada Correctamente")
      return redirect(url_for('prestamos'))
    else:
      flash("La Solicitud no fue Ingresada, por favor intente nuevamente.")
      return redirect(url_for('prestamos'))

  else:

    return redirect(url_for('index'))

@app.route('/cpedidos')
def pedidos()->'html':
  if 'cedula' in session:

    cedula=str(session['cedula'])
    data=carrito_cliente(cedula)
    suma_total = 0

    #Metrica de efectividad numero de transacciones diarias abandonadas.
    session['ef_transaccionesd'] = len(data)

    #Metrica de entendibilidad numero de paginas rapidamente abandonadas
    session['tiempo_paginas_init']=time.time()


    if len(data)>0:

      session['ef_sesionesd']=1 #Indica 1 que al menos un producto quedo en el carrito como pendiente de pago
    else:
      session['ef_sesionesd']=0 #Indica 0 que el carrito no tiene transacciones pendientes por lo tanto no existen sessiones abandonada.s


    for tupla in data:
      valor_decimal = tupla[4]
      suma_total += float(valor_decimal)

    if suma_total == 0:
      bandera_tarjeta="disabled"
    else :
      bandera_tarjeta=""


    return render_template(
      'cliente/pedidos.html',
      titulo='Carrito Compras',
      data=data,
      nom=str(session['nombres']),
      ced=str(session['cedula']),
      cor=str(session['correo']),
      sum=suma_total,
      btn=bandera_tarjeta
    )

  else:

    return redirect(url_for('index'))


@app.route('/ccarrito',methods=['POST'])
def agregarcesta()->'html':
  if 'cedula' in session:
    id = request.form.get('id')
    precio = request.form.get('precio')
    fecha_actual = datetime.now().date()
    res=agregarcestabd(id,str(session['cedula']),fecha_actual,1,precio)

    if res:
      return redirect(url_for('pedidos'))
    else:
      return redirect(url_for('catalogo_cliente'))

  else:

    return redirect(url_for('index'))

@app.route('/tarjeta',methods=['POST'])
def compra_finalizada()->'html':
  if 'cedula' in session:
   total = request.form.get('total')
   cedula=session['cedula']
   fecha_actual = datetime.now().date()

   #Entendibilidad : Numero de Errores en el campo de tarjeta exactamente en numero y cv
   errores=request.form.get('errores')
   session['e_nerrores']=errores

   res=pedido_exitoso(cedula,fecha_actual,total)
   rese= eliminar_carrito(cedula)


   if res and rese :
     flash('Pedido realizado con Exito, dirigite a Comprobantes para visualizar el documento.')
     #Metrica de Eficiencia : Tiempo en completar una transaccion

     times_tran = session['efc_tiempoinicio']
     calculo_tiempo_transaccion = round(time.time() - times_tran)
     session['efc_tiempometrica'] = calculo_tiempo_transaccion

     eficiencia(session['efc_tiempometrica'],1,fecha_actual)
     #session['efc_tiempometrica']=0
     session['efc_tiempoinicio'] = 0
     session['efc_tiempoinicio'] = time.time()

     return redirect(url_for('pedidos'))
   else:
      flash('Ocurrio un Error al realizar el pedido,intentalo más adelante.')
      return redirect(url_for('pedidos'))

  else:
   return redirect(url_for('index'))


@app.route('/eliminar',methods=['GET'])
def eliminar_producto_carrito()->'html':
  if 'cedula' in session:
   id=request.args.get('id')
   print(id)

   res=eliminar_producto(id)

   if res :
     flash('El producto ha sido eliminado de su carrito.')
     return redirect(url_for('pedidos'))
   else:
      flash('Ocurrio un Error no se puede eliminar el producto de su carrito.')
      return redirect(url_for('pedidos'))

  else:
   return redirect(url_for('index'))


@app.route('/ccomprobantes')
def comprobantes()->'html':
  if 'cedula' in session:

    cedula=str(session['cedula'])
    data=cliente_comprobantes(cedula)


    return render_template(
      'cliente/comprobantes.html',
      titulo='Comprobantes de Venta',
      data=data,
      nom=str(session['nombres']),
      ced=str(session['cedula']),
      cor=str(session['correo']),
    )

  else:

    return redirect(url_for('index'))

@app.route('/cprestamos')
def prestamos()->'html':
  if 'cedula' in session:

    data=cliente_solicitudes(session['cedula'])


    times = session['tiempo_paginas_init']


    calculo=round(time.time()-times)

    #Metrica de paginas cerradas

    if calculo <4:
      session['e_pcerradas']=session['e_pcerradas']+1

    session['tiempo_paginas_init']=0

    return render_template(
      'cliente/prestamos.html',
      titulo='Prestamos de Equipos',
      data=data
    )

  else:

    return redirect(url_for('index'))


@app.route('/logout')
def cerrarsesion()->'html':
    #session['e_nayudas'] = 0
    #session['e_pcerradas'] = 0
    #session['e_nerrores'] = 0
    #session['e_tiempop'] = 0
  fecha = datetime.now()
  fechas = fecha.date()

  #Ingreso de datos para entendibildad
  entendibilidad(session['e_nayudas'],session['e_pcerradas'], session['e_nerrores'], session['e_tiempop'], fechas)
  # Ingreso de datos para efectividad
  efectividad(session['ef_transaccionesd'],session['ef_sesionesd'],fechas)


  session.clear()

  return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
