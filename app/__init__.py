from os import path
from flask import Flask, url_for, render_template, g, request, session, flash, redirect
from app.models.usuario import User
from app.config import Config
from app.db import db
from flask_session import Session
from app.resources import user
#from flask_mysqldb import MySQL

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)
#session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#config db
app.secret_key = 'hola'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+Config.DB_USER+":"+Config.DB_PASS+"@"+Config.DB_HOST+"/"+Config.DB_NAME
db.init_app(app)





# ruta a quienes somos

app.add_url_rule('/quienesomos', 'quienesomos', user.quienesomos, methods=["POST", "GET"])

#ruta a centros
app.add_url_rule('/centros', 'centros', user.centros, methods=["POST", "GET"])


#ruta a login
app.add_url_rule('/login', 'login', user.login)


#index
@app.route('/')
def index():
    return render_template('index.html')

