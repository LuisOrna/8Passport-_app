from flask import Blueprint, request, jsonify
from models.user import User
import bcrypt
from database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity



#Creo el blueprint
jwt_bp = Blueprint(name='jwt', import_name=__name__)


#Funcion para verificar ADMIN
def verificar_admin_jwt():
    usuario_actual_id = get_jwt_identity()
    usuario = User.query.get(usuario_actual_id)
    
    if usuario.role != 'admin':
        return {'error': 'Acceso denegado. Solo administradores.'}, 403
    
    return None

#Ruta login con JWT
@jwt_bp.route('/api/login', methods = ['POST'])
def api_login():

    data = request.get_json()
    email = data['email']
    password = data['password']

    usuario = User.query.filter_by(email=email).first()

    if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
        #Si se valida, creo el token 
        access_token = create_access_token(identity=str(usuario.id)) #si no es str da error
        return {'access_token': access_token, 'user_name': usuario.nombre}
    
    #si no se valida
    return {'error': "credenciales de ingreso incorrectas"}, 401


#Ruta protegida con JWT
@jwt_bp.route('/api/users', methods = ['GET'])
@jwt_required()
def protegida():

    #Filtro admin
    error = verificar_admin_jwt()
    if error:
        return error
    
    #Hago la solicitud para traer todos los datos de db
    usuarios = User.query.all()

    #Convierto el usuarios que es un objeto en una lista de usurios
    usuarios_lista = []
    for usuario in usuarios:
        usuarios_dict = {
            'id': usuario.id,
            'email': usuario.email,
            'nombre': usuario.nombre
        }
        usuarios_lista.append(usuarios_dict)

    return jsonify(usuarios_lista)


#Ruta protegida con JWT para eliminar usuario
@jwt_bp.route('/api/users/<int:user_id>', methods = ['DELETE']) #Flask toma el numero y se lo pasa a la funcion
@jwt_required()
def delete_user(user_id):

    #Filtro admin
    error = verificar_admin_jwt()
    if error:
        return error
    
    #1 Buscar el usuario con id
    usuario_para_eliminar = User.query.filter_by(id = user_id).first()
    #2 que pasa cuando no hay usurio
    if not usuario_para_eliminar:
        return {'Error': 'Numero de Id ingresado no existe'}
    
    #3 Si llega aqui existe, como lo elimino de db
    db.session.delete(usuario_para_eliminar)
    db.session.commit()
    
    #Mensaje que envio de regreso
    return {'hecho': f'usuario {usuario_para_eliminar.nombre} con id {usuario_para_eliminar.id} eliminado'}