
from flask import Flask, render_template, request, session, redirect, url_for, flash
from bdd import *
from datetime import datetime
import aiml

app = Flask(__name__)
app.secret_key = 'tid@205'

# Crea el objeto Kernel de AIML y carga los archivos AIML
kernel = aiml.Kernel()
kernel.learn("bot.aiml")


@app.route('/pr')

def prueba() -> 'html':
  return render_template('invitado/dcatalogo.html',titulo ='Inicio')

@app.route('/')

def index() -> 'html':
  return render_template('invitado/index.html',titulo ='Inicio')

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]
    response = kernel.respond(user_message)
    return str(response)

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
  return render_template('invitado/catalogo.html',titulo ='Nuestros Productos',data=data)

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
  v_correo=validar_userxcedula(correo)


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

@app.route('/ccatalogo')
def catalogo_cliente()->'html':
  if 'cedula' in session:

    data = verproductos()
    #print(data)

    return render_template('cliente/catalogo.html', titulo='Catalogo de Productos',data=data)

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
    print(data)
    suma_total = 0

    for tupla in data:
      valor_decimal = tupla[4]
      suma_total += float(valor_decimal)

    return render_template(
      'cliente/pedidos.html',
      titulo='Carrito Compras',
      data=data,
      nom=str(session['nombres']),
      ced=str(session['cedula']),
      cor=str(session['correo']),
      sum=suma_total
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

   res=pedido_exitoso(cedula,fecha_actual,total)
   rese= eliminar_carrito(cedula)

   if res and rese :
     flash('Pedido realizado con Exito, dirigite a Comprobantes para visualizar el documento.')
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

    return render_template(
      'cliente/prestamos.html',
      titulo='Prestamos de Equipos',
      data=data
    )

  else:

    return redirect(url_for('index'))


@app.route('/logout')
def cerrarsesion()->'html':
  session.clear()

  return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
