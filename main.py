
from flask import Flask,render_template

app = Flask(__name__)
app.secret_key = 'tid@205'

@app.route('/pr')

def prueba() -> 'html':
  return render_template('pr.html',titulo ='Inicio')

@app.route('/')

def formulario() -> 'html':
  return render_template('invitado/index.html',titulo ='Inicio')

@app.route('/login')

def login() -> 'html':
  return render_template('invitado/login.html',titulo ='Iniciar Sesion')

@app.route('/registro')

def registro() -> 'html':
  return render_template('invitado/registro.html',titulo ='Registro')

if __name__ == '__main__':
    app.run(debug=True)
