from os import path
from flask import Flask, url_for, render_template, g, abort, request, session, flash, redirect
from app.models.usuario import User
from app.config import Config
from app.models.configuracion import Configuracion
from app.db import db
from flask_session import Session
from app.resources import user
from app.resources import config
from app.resources import centros_de_ayuda
from flask_fontawesome import FontAwesome
from app.resources import turnos_para_centro
from app.helpers import permisos
from requests import get
from app.resources import api
from app.resources.Api import centros
from app.resources.Api import turnos

# from flask_mysqldb import MySQL


def create_app():
    # Configuración inicial de la app
    app = Flask(__name__)
    app.config.from_object(Config)
    fa = FontAwesome(app)
    # session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    # Max size of files abajo
    # app.config['MAX_CONTENT_PATH'] = ???
    Session(app)

    # config db
    app.secret_key = 'hola'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + \
        Config.DB_USER+":"+Config.DB_PASS+"@"+Config.DB_HOST+"/"+Config.DB_NAME
    db.init_app(app)

    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    # Autenticacion agregado por maxi
    app.add_url_rule('/login', 'login', user.login)
    app.add_url_rule('/backend', 'user_backend',
                     user.backend, methods=['POST'])
    app.add_url_rule('/logout', 'logout', user.logout)

    # ruta a la api centros
    app.add_url_rule('/Api/centros', 'api_centros',
                     centros.mostrar_centros, methods=["GET"])
    app.add_url_rule('/Api/centros/page/<int:page>', 'api_centros',
                     centros.mostrar_centros, methods=["GET"])
    app.add_url_rule('/Api/centros/<int:id>', 'api_centro', centros.mostrar_centro, methods=["GET"])

    #ruta Post de Api centros
    app.add_url_rule('/Api/crear_centro', 'api_crear_centro',
                     centros.cargarCentros, methods=["GET", "POST"])

    # ruta a la api turnos
    app.add_url_rule('/Api/centros/id_centro/<int:id_centro>/turnos_disponibles/fecha=<fecha>',
                     'turnos_disponibles', turnos.turnos_disponibles, methods=["POST", "GET"])
    #app.add_url_rule('/centros/id/<id>/turnos_disponibles',
    #                 'turnos_disponibles', turnos.turnos_disponibles, methods=["GET"])
    app.add_url_rule('/Api/centros/id_centro/<int:id_centro>/reserva', 'pedir_reserva',
        turnos.pedir_reserva, methods=["POST", "GET"])


    # ruta a centros
    app.add_url_rule('/centros', 'centros',
                     centros_de_ayuda.go_index, methods=["POST", "GET"])
    app.add_url_rule('/centros/page/<int:page>', 'centros',
                     centros_de_ayuda.go_index, methods=["POST", "GET"])
    app.add_url_rule('/centros/nombre/<nombre>/estado/<estado>/page/<int:page>',
                     'centros', centros_de_ayuda.go_index, methods=["POST", "GET"])
    app.add_url_rule('/centros/crear_centro', 'crear_centro',
                     centros_de_ayuda.crear_centro,  methods=["POST", "GET"])
    app.add_url_rule('/centros/editar_centro/<id>', 'editar_centro',
                     centros_de_ayuda.editar_centro, methods=['POST', 'GET'])
    app.add_url_rule('/centros/borrar_centro/<id>', 'borrar_centro',
                     centros_de_ayuda.borrar_centro, methods=['POST', 'GET'])
    app.add_url_rule('/centros/aprobar_centro/<id>', 'aprobar_centro',
                     centros_de_ayuda.aprobar_centro,  methods=["POST", "GET"])
    app.add_url_rule('/centros/rechazar_centro/<id>', 'rechazar_centro',
                     centros_de_ayuda.rechazar_centro,  methods=["POST", "GET"])
    app.add_url_rule('/centros/publicar_centro/<id>', 'publicar_centro',
                     centros_de_ayuda.publicar_centro,  methods=["POST", "GET"])
    app.add_url_rule('/centros/despublicar_centro/<id>', 'despublicar_centro',
                     centros_de_ayuda.despublicar_centro,  methods=["POST", "GET"])
    app.add_url_rule('/centros/mostrar_centro/<id>', 'mostrar_centro',
                     centros_de_ayuda.mostrar_centro,  methods=["POST", "GET"])

    # ruta a login
    app.add_url_rule('/login', 'login', user.login)

    # CONFIGURACION
    app.add_url_rule('/configuracion/vista_configuracion', 'vista_configuracion',
                     config.vista_configuracion, methods=["POST", "GET"])
    # usuario
    app.add_url_rule('/usuario/edit_usuario/<id>', 'edit_usuario',
                     user.edit_usuario, methods=['POST', 'GET'])
    app.add_url_rule('/usuario/index_usuario', 'index_usuario',
                     user.index_usuario, methods=["POST", "GET"])
    app.add_url_rule('/usuario/crear_usuario', 'crear_usuario',
                     user.crear_usuario, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/borrar_usuario/<id>",
                     'borrar_usuario', user.borrar, methods=['GET'])
    app.add_url_rule('/usuarios/activar/<id>', 'activar',
                     user.activar,  methods=['POST', 'GET'])
    app.add_url_rule('/usuarios/desactivar/<id>', 'desactivar',
                     user.desactivar,  methods=['POST', 'GET'])
    app.add_url_rule('/usuarios/page/<int:page>', 'index_usuario',
                     user.index_usuario, methods=["POST", "GET"])
    app.add_url_rule('/usuarios/nombre/<nombre>/estado/<estado>/page/<int:page>',
                     'index_usuario', user.index_usuario, methods=["POST", "GET"])

    # turno para centro
    app.add_url_rule('/turnos_para_centro/index_turno', 'index_turno',
                     turnos_para_centro.index_turno, methods=["POST", "GET"])
    app.add_url_rule('/turnos_para_centro/page/<int:page>', 'index_turno',
                     turnos_para_centro.index_turno, methods=["POST", "GET"])

    app.add_url_rule('/turnos_para_centro/index_turno',
                     'index_turno', turnos_para_centro.index_turno, methods=["POST", "GET"])
    app.add_url_rule('/turnos_para_centro/index_turno/id/<id>',
                     'index_turno', turnos_para_centro.index_turno, methods=["POST", "GET"])
    app.add_url_rule('/turnos_para_centro/page/<int:page>/id/<id>', 'index_turno',
                     turnos_para_centro.index_turno, methods=["POST", "GET"])
    app.add_url_rule('/turnos_para_centro/email/<email>/page/<int:page>',
                     'index_turno', turnos_para_centro.index_turno, methods=["POST", "GET"])
    #app.add_url_rule('turnos_para_centro/page/<int:page>', 'index_turno', turnos_para_centro.index_turno, methods=["POST", "GET"])
    app.add_url_rule('/turnos_para_centro/crear_turno', 'crear_turno',
                     turnos_para_centro.crear_turno, methods=["POST", "GET"])
    app.add_url_rule('/turnos_para_centro/editar_turno/<id>', 'editar_turno',
                     turnos_para_centro.editar_turno, methods=["POST", "GET"])
    app.add_url_rule('/turnos_para_centro/borrar_turno/<id>', 'borrar_turno',
                     turnos_para_centro.borrar_turno, methods=["POST", "GET"])
    app.add_url_rule('/turnos_para_centro/sacar_turno/<id>', 'sacar_turno',
                     turnos_para_centro.sacar_turno, methods=["POST", "GET"])

    # ruta al backend
    app.add_url_rule('/backend', 'backend', user.backend,
                     methods=["POST", "GET"])

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errores/404.html'), 404

    @app.errorhandler(503)
    def page_not_found(e):
        return render_template('errores/503.html'), 503

    @app.errorhandler(401)
    def page_not_found(e):
        return render_template('errores/401.html'), 401

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('errores/403.html'), 403

    @app.route('/test')
    def test():
        municipios = get(
            'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=1000').json()
        return municipios['data']['Town']['1']['name']

    # index

    @app.route('/')
    def index():
        if permisos.sitio_cerrado() and permisos.no_es_admin():
            abort(503)
        configuracion = Configuracion.get_config()
        return render_template('index.html', configuracion=configuracion)

    return app
