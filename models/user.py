#Dependencias
from database import db

#Creo la clase
class User(db.Model): #aprovecho y traigo una clase padre
    #Logica de SQLAlchemy
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    nombre = db.Column(db.String(50), nullable = False)
    #Agrego el rol, refetente a la realizacion de user vs admin
    role = db.Column(db.String(20), nullable = False, default = 'usuario')

    #Creo el constructor
    def __init__(self, email, password, nombre, role = 'usuario'):
        self.email = email
        self.password = password
        self.nombre = nombre
        self.role = role #Por defecto 'ususrio'

        
#Para mostrar al usuario
    def __repr__(self):
        return f'<User {self.email}, nombre {self.nombre}>'
    