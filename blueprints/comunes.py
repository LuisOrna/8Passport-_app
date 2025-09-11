from flask import Blueprint, session, redirect, render_template

#Creo el Blueprint
comun_bp = Blueprint('comun',__name__)

#Ruta para pagina
@comun_bp.route('/dashboard', methods = ['GET'])
def mostrar_dashboard():
    if 'id' not in session:
        return redirect('/login')
    
    #Si llega a aqui esta verificado
    return render_template('dashboard.html', nombre_usuario = session['name'],
                                   numero_de_usuario = session['id'],
                                   role = session['role'])


#Ruta de inicio
@comun_bp.route('/', methods = ['GET'])
def mostrar_inicio():
    return render_template('index.html')

