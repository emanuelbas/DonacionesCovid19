from flask import session, abort
from app.helpers.auth import authenticated
from app.models.configuracion import Configuracion
from app.models.usuario import User


def validar_permisos(un_permiso):
	if sitio_cerrado() and no_es_admin():
		print("Salio xq no estaba cerrado y no esta logueado como admin")
		abort(503)

	# Si el usuario no tiene una cookie de sesion válida muestro un mensaje de error
	if not authenticated(session):
		print("Salio xq no estaba autenticado")
		abort(401)
	if not usuario_activo(session):
		print("Salio xq no estaba activo")
		abort(401)#cambiar por 403
	if no_tiene_el_permiso_solicitado(un_permiso):
		print("Salio xq no tenia el permiso")
		abort(401)
	return


########   Funciones auxiliares   ########

def no_es_admin():
	return not (authenticated(session) and User.tiene_rol(session["usuario"], 'admin'))

def sitio_cerrado():
	return not Configuracion.habilitado()

def no_tiene_el_permiso_solicitado(un_permiso):
	return False
	#return not User.tiene_permiso(session["usuario"], un_permiso)

def usuario_activo(session):
	return session["usuario"].activo