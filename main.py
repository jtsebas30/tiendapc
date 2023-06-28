
from flask import Flask, render_template, request, session, redirect, url_for, flash
from bdd import *

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


#####RUTAS CON SESION

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







if __name__ == '__main__':
    app.run(debug=True)
