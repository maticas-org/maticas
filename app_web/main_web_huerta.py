#MODULOS NECESARIOS PARA EL DESARROLLO DE LA APLICACIÓN
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import pandas as pd
from manipulate_data_for_settings import get_data_from_all_actuators_settings, get_data_from_all_ambiental_settings, get_info_from_html_form, write_all_actuators_settings, write_all_ambiental_settings

#MODULOS REQUERIDOS PARA ESTABLECER LA CONEXIÓN CON LA BASE DE DATOS
from db_mqtt_interface.db.dirty7w7 import *
from db_mqtt_interface.db.db_connection import db_connection

#MODULOS PARA ESTABLECER LA CONEXIÓN CON EL BROKER
from db_mqtt_interface.mqtt_python.dirty8w8 import *
from db_mqtt_interface.mqtt_python.writeFromMqtt import *

#MODULO PARA PODER CREAR EL DASHBOARD DENTRO DE LA APLICACIÓN FLASK
from data_dash_app import create_dash_app
from detailed_data_dash_app import create_dash_app_2

#MODULO QUE CONTIENE LAS FUNCIONES USADAS EN LAS RUTAS
from manipulate_data_for_settings import *



#CREACIÓN DE LA APLICACIÓN
app = Flask(__name__)
create_dash_app(app)
create_dash_app_2(app)

#SECRET KEY DE LA APP
app.secret_key = 'APP#%&**twyt34+%'

#CONEXIÓN A LA BASE DE DATOS
conn = db_connection(db_host =  db_host,
                     db_name =  db_name,
                     db_user = db_user,
                     db_password =  db_password,
                     db_sslmode = db_sslmode
                    )


#CONEXIÓN AL BROKER
send_conn = mqtt_broker_connection_write( mqtt_broker = mqtt_broker,
                                          mqtt_port = mqtt_port,
                                          mqtt_username = mqtt_username,
                                          mqtt_password = mqtt_password,
                                          mqtt_client_id = mqtt_client_id 
                                          )


#RUTA PRINCIPAL
@app.route('/')
def home():
    return redirect(url_for('settings'))

#---------------------------------------------
#--------------PESTAÑA SETTINGS---------------
#---------------------------------------------
@app.route('/settings')
def settings():
    get_data_from_all_ambiental_settings()
    get_data_from_all_actuators_settings()
    return render_template('settings.html', title='Settings', ambiental_dict = interval_ambiental_vars, actuators_dict = interval_actuators_vars)


#EDITAR LOS DATOS DE LAS SETTINGS
@app.route('/settings_update')
#TOMAR LA INFO DE LA BASE DE DATOS Y UBICARLA
def get_info_to_update():
    get_data_from_all_ambiental_settings()
    get_data_from_all_actuators_settings()
    return render_template('settings_update.html', title='Settings update', ambiental_dict = interval_ambiental_vars, actuators_dict = interval_actuators_vars)
        

@app.route('/modify_values', methods=['POST'])
#MODIFICAR LOS DATOS
def modify_values_in_settings():
    if request.method == 'POST':
        get_info_from_html_form()
        write_all_ambiental_settings()
        write_all_actuators_settings()
        return redirect(url_for('settings'))

@app.route('/pump_on')
def pump_on():
    
    # dependiendo de como funcione el relé se envía un 1 un 0.
    # para encenderla

    send_conn.send_message(alias_topic='pump', message='1')
    time.sleep(0.3)
    send_conn.send_message(alias_topic='pump', message='1')
    time.sleep(0.4)
    send_conn.send_message(alias_topic='pump', message='1')

    flash('Bomba de agua encendida satisfactoriamente')
    return redirect(url_for('settings'))

@app.route('/pump_off')
def pump_off():

    # dependiendo de como funcione el relé se envía un 1 un 0.
    # para apagarla. Envío varias veces para asegurarme que llega 
    # el mensaje al otro lado

    send_conn.send_message(alias_topic='pump', message='0')
    time.sleep(0.3)
    send_conn.send_message(alias_topic='pump', message='0')
    time.sleep(0.4)
    send_conn.send_message(alias_topic='pump', message='0')

    flash('Bomba de agua apagada satisfactoriamente')
    return redirect(url_for('settings'))

@app.route('/light_on')
def light_on():

    # dependiendo de como funcione el relé se envía un 1 un 0.
    # para encenderla

    send_conn.send_message(alias_topic='light', message='1')
    time.sleep(0.3)
    send_conn.send_message(alias_topic='light', message='1')
    time.sleep(0.4)
    send_conn.send_message(alias_topic='light', message='1')
    flash('Luces encendidas satisfactoriamente')
    return redirect(url_for('settings'))

@app.route('/light_off')
def light_off():

    # dependiendo de como funcione el relé se envía un 1 un 0.
    # para apagarla

    send_conn.send_message(alias_topic='light', message='0')
    time.sleep(0.3)
    send_conn.send_message(alias_topic='light', message='0')
    time.sleep(0.4)
    send_conn.send_message(alias_topic='light', message='0')
    flash('Luces apagadas satisfactoriamente')
    return redirect(url_for('settings'))


#VERIFICACIÓN PARA CORRER LA APP
if __name__ == "__main__":
    app.run(debug=True)
