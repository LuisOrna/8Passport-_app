#La unica finalidad de este script es la creacion de la base de datos. Una vez que se ejecute
from app import app
from database import db
from models.user import User



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de Datos Creada")
