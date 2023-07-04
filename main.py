
from flask import Flask, render_template, request, session, redirect, url_for, flash
from bdd import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tid@205'


@app.route('/pr')

def prueba() -> 'html':
  return render_template('invitado/dcatalogo.html',titulo ='Inicio')

@app.route('/')

def index() -> 'html':
  return render_template('invitado/index.html',titulo ='Inicio')

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

  res=nuevousuario(cedula, nombre, apellido, provincia, domicilio, correo, clave)
  #print(res)

  if res :
    return redirect(url_for('login'))
  else:
    return redirect(url_for('index'))

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

    return render_template('cliente/detallecatalogo.html',data=data,titulo=data[0][1])

  else:

    return redirect(url_for('index'))

@app.route('/cpedidos')
def pedidos()->'html':
  if 'cedula' in session:

    cedula=str(session['cedula'])
    data=carrito_cliente(cedula)

    return render_template(
      'cliente/pedidos.html',
      titulo='Carrito Compras',
      data=data,
      nom=str(session['nombres']),
      ced=str(session['cedula']),
      cor=str(session['correo'])
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




@app.route('/logout')
def cerrarsesion()->'html':
  session.clear()

  return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
