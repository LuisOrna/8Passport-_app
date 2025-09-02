#Dependencias
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
import bcrypt


#Creo la app
app = Flask(__name__)
app.config.from_object(Config) # Pido que la app se configure desde el objeto Config

#Creo el objeto para hablar con la base de datos
db = SQLAlchemy(app)

#Importo del modelo 


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
    
if __name__ == "__main__":
    from models.user import User
    app.run(debug=True)

