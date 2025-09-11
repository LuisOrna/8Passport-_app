#Dependencias
from flask import Blueprint, render_template, session, redirect
from database import db
from models.user import User




#Creo el blueprint
admin_bp = Blueprint(name='admin', import_name=__name__)

#Funcion auxiliar de Verificacion
def verificar_admin():
    if 'id' not in session:
        return redirect('/login')
    
    if session.get('role') != 'admin':
        return "Acceso denegado. Solo administradores."
    
    return None  # Si todo está bien, no retorna nada


#Ruta para administador
@admin_bp.route('/admin', methods = ['GET'])
def mostrar_adminpanel():
    error = verificar_admin()
    if error:
        return error
    #Si llega a aqui paso ambos filtros es un Admin
    usuarios = User.query.all()
    return render_template('admin.html', usuarios = usuarios)

