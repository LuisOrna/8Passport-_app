#Dependencias
from app import db

#Creo la clase
class User(db.Model): #aprovecho y traigo una clase padre
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    nombre = db.Column(db.String(50), nullable = False)

    #Creo el constructor
    def __init__(self, email, password, nombre):
        self.email = email
        self.password = password
        self.nombre = nombre
        
#Para mostrar al usuario
    def __repr__(self):
        return f'<User {self.email}>'
    