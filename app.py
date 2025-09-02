#Dependencias
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

#Creo la app
app = Flask(__name__)
app.config.from_object(Config) # Pido que la app se configure desde el objeto Config

#Creo el objeto para hablar con la base de datos
db = SQLAlchemy(app)

#Ruta de Prueba
@app.route('/')
def home():
    print(app.config['SECRET_KEY'])
    return "Hola Passport"

#Ruta para loging de Prueba
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return f'Login exitoso {email}'


    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
