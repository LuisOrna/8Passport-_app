#Creo la clase principal que se recibe en app.py
class Config:
    SECRET_KEY = 'mi-clave-secreta-temporal'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///passport.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  #Para que no me consuma memoria vigilando 
    JWT_SECRET_KEY = 'jwt-secret-string'