
from flask import Flask,render_template

app = Flask(__name__)
app.secret_key = 'tid@205'

@app.route('/')

def formulario() -> 'html':
  return render_template('index.html',titulo ='Inicio')


if __name__ == '__main__':
    app.run(debug=True)
