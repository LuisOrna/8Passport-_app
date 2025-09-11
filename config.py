from datetime import timedelta

#Creo la clase principal que se recibe en app.py
class Config:
    SECRET_KEY = 'mi-clave-secreta-temporal'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///passport.db'
    JWT_SECRET_KEY = 'jwt-secret-string'
    # Cookies seguras
    SESSION_COOKIE_HTTPONLY = True #js no ouede leer
    SESSION_COOKIE_SECURE = False  # True solo con HTTPS
    SESSION_COOKIE_SAMESITE = 'Strict' #solo envia al mismo sitio
    # Tiempo de expiración
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # 2 horas

ADMIN_EMAILS = ['admin@email.com']