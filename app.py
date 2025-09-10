#Dependencias
from flask import Flask, request, render_template, session, redirect #Para construir servidor
from flask_sqlalchemy import SQLAlchemy #Para manejar base de datos
from config import Config #Archivo de config
from database import db
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect  #Agregado para la proteccion CSRF


#Creo la app
app = Flask(__name__)
#Le aplico la proteccion a la App
csrf = CSRFProtect(app)
# Excluir rutas API de CSRF
csrf.exempt('blueprints.auth.api_login')
# Pido que la app se configure desde el objeto Config
app.config.from_object(Config) 
#Conecto la Base de Datos a aqui
db.init_app(app)

#Inicio de de JWT
jwt = JWTManager(app)


#Conexion de la app al blueprint auth
app.register_blueprint(auth_bp)

#Conexion a blueprint admin
app.register_blueprint(admin_bp)


#Headers de seguridad
@app.after_request
def security_headers(response): 
    response.headers['X-Content-Type-Options'] = 'nosniff' #contra ataques de tipo MIME sniffing
    response.headers['X-Frame-Options'] = 'DENY' #Protege contra clickjacking
    return response


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

