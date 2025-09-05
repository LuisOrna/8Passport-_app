#Dependencias
from flask import Flask, request, render_template, session, redirect #Para construir servidor
from flask_sqlalchemy import SQLAlchemy #Para manejar base de datos
from config import Config #Archivo de config
from database import db
'''from functools import wraps #Este me va a ayudar a decorar, aplicar logica comun a varios puntos'''
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp

#Creo la app
app = Flask(__name__)
app.config.from_object(Config) # Pido que la app se configure desde el objeto Config

#Conecto la Base de Datos a aqui
db.init_app(app)

#Conexion de la app al blueprint auth
app.register_blueprint(auth_bp)

#Conexion a blueprint admin
app.register_blueprint(admin_bp)


#Ruta de Prueba
@app.route('/')
def home():
    print(app.config['SECRET_KEY'])
    return "Hola Passport"


#Ruta para el DASHBOARD
@app.route('/dashboard', methods = ['GET'])
def dashboard():

    if 'id' not in session:
        return redirect('/login')
        
    #Si llega a aqui esta verificado    
    return render_template('dashboard.html', 
                                   nombre_usuario = session['name'],
                                   numero_de_usuario = session['id'],
                                   role = session['role'])


if __name__ == "__main__":
    app.run(debug=True)

