from flask import Blueprint, request, render_template, session, redirect, jsonify
from database import db
from models.user import User
import bcrypt #Para hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity 
from flask import render_template_string #Para hacer Escape

#Creo el blueprint
auth_bp = Blueprint('auth', __name__)


#RUTA PARA LOGIN
@auth_bp.route('/login', methods = ['GET', 'POST'])
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
            #Agrego el role a la session
            session['role'] =usuario.role

            #Redirijo al Dashboard
            return render_template('dashboard.html', 
                                   nombre_usuario = session['name'],
                                   numero_de_usuario = session['id'],
                                   role = session['role'])
        else:
            return "Email o contrasenha incorrectos"
    
    
    #Cuando el methodo no es POST, es decir que es GET
    return render_template('login.html')



#RUTA PARA REGISTRO
@auth_bp.route('/register', methods = ['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        password = request.form['password']

        #TEMPORAL para role
        role = 'admin' if 'admin' in email else 'usuario'


        #Hago el hashing de la contrasenha --> la variable almacenada esta hasheada pero ademas encodeada
        password_hasheada = bcrypt.hashpw(password= password.encode('utf-8'), salt=bcrypt.gensalt()) #Con el metodo que estoy aplicando en sal el mismo password produce un hash diferente cada vez
        
        #Creo el usuario    
        nuevo_usuario = User(email=email, password=password_hasheada.decode('utf-8'), nombre=nombre, role=role)

        #Lo guardo en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        return render_template_string('Ususario {{ nombre }} registrado correctamente', nombre= nombre)
    
    #Cuando no sea el metodo POST
    return render_template('register.html')

#RUTA PARA LOGOUT
@auth_bp.route('/logout', methods = ['POST'])
def logout():
    session.clear() #Borra la sesion
    return redirect('/login')


#==========JWT=====================================

#Ruta login con JWT
@auth_bp.route('/api/login', methods = ['POST'])
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
@auth_bp.route('/api/users', methods = ['GET'])
@jwt_required()
def protegida():
    usuario_actual = get_jwt_identity()  #Obtengo la identidad del que entro
    usuario = User.query.get(usuario_actual) #Obtengo el User relacionado con esa identidad

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
@auth_bp.route('/api/users/<int:user_id>', methods = ['DELETE']) #Flask toma el numero y se lo pasa a la funcion
@jwt_required()
def delete_user(user_id):
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