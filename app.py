#Dependencias
from flask import Flask, request, render_template, session, redirect #Para construir servidor
from flask_sqlalchemy import SQLAlchemy #Para manejar base de datos
from config import Config #Archivo de config
from database import db
import bcrypt #Para hash


#Creo la app
app = Flask(__name__)
app.config.from_object(Config) # Pido que la app se configure desde el objeto Config

#Conecto la Base de Datos a aqui
db.init_app(app)

from models.user import User

#Ruta de Prueba
@app.route('/')
def home():
    print(app.config['SECRET_KEY'])
    return "Hola Passport"

#Ruta para loging de Prueba
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_ingresado = request.form['email']
        password_ingresada = request.form['password']
        
        #Bosco al uaurio que quiere logearse en la db
        usuario = User.query.filter_by(email=email_ingresado).first()

        #Si no coincide el correo electronico
        if not usuario:
            return "Email o contrasenha incorrectos"
        
        #Si hay un usuario aplico esto
        if usuario and bcrypt.checkpw(password_ingresada.encode('utf-8'), usuario.password.encode('utf-8')):
            #Creo la sesion
            session['id'] = usuario.id
            session['name'] = usuario.nombre
            #Redirijo al Dashboard
            return render_template('dashboard.html', 
                                   nombre_usuario = session['name'],
                                   numero_de_usuario = session['id'])
        else:
            return "Email o contrasenha incorrectos"
    
    
    #Cuando el methodo no es POST, es decir que es GET
    return render_template('login.html')


#Ruta para registro
@app.route('/register', methods = ['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        password = request.form['password']

        #Hago el hashing de la contrasenha --> la variable almacenada esta hasheada pero ademas encodeada
        password_hasheada = bcrypt.hashpw(password= password.encode('utf-8'), salt=bcrypt.gensalt()) #Con el metodo que estoy aplicando en sal el mismo password produce un hash diferente cada vez
        
        #Creo el usuario    
        nuevo_usuario = User(email=email, password=password_hasheada.decode('utf-8'), nombre=nombre)

        #Lo guardo en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        return f'Usuario {nombre} registrado correctamente'
    
    #Cuando no sea el metodo POST
    return render_template('register.html')


#Ruta para el DASHBOARD
@app.route('/dasboard', methods = ['GET'])
def dashboard():

    if 'id' not in session:
        return redirect('/login')
        
    #Si llega a aqui esta verificado    
    return render_template('dashboard.html', 
                                   nombre_usuario = session['name'],
                                   numero_de_usuario = session['id'])
    
#Ruta para logout
@app.route('/logout', methods = ['POST'])
def logout():
    session.clear() #Borra la sesion
    return redirect('/login')


if __name__ == "__main__":
    #TODO Importo del modelo, lo hago aqui para evitar el error de circulo Vicioso 
    app.run(debug=True)

