from flask import Flask
from configuracion import Config

#Creo la app
app = Flask(__name__)
app.config.from_object(Config)


#Ruta de Prueba
@app.route('/')
def home():
    return "Hola Passport"

if __name__ == "__main__":
    app.run(debug=True)
