# necesitamos añadir la carpeta de la clase
# con operaciones sobre la base de datos 
# al path
from sys import path 

# para añadir dicha clase necesitamos saber primero 
# donde estámos parados
from os import getcwd
 
# hago cd .. , para añadir ese path completico
cwd = getcwd()
cwd = cwd.split('/')[:-1]
cwd = '/'.join(cwd)

# Añade el directorio al path
path.insert(1, cwd) 
#print("current working directory: cd .. -> ",  cwd)

import dash
from datetime import date
from dash import dcc
from dash import html
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd
from dash import Input, Output, callback_context

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from db_mqtt_interface.db.dirty7w7 import *
from db_mqtt_interface.db.db_connection import db_connection

conn = db_connection(db_host =  db_host,
                     db_name =  db_name,
                     db_user = db_user,
                     db_password =  db_password,
                     db_sslmode = db_sslmode
                    )

def create_dash_app_2(flask_app):
    app_dash = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/detailed_analysis/")

    table1=conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'hum',
               verbose = True)
               
    #Tabla normal
    my_plot1 = table1.plot("time", "hum_level", kind="line")
    tbl1 = px.line(table1,x='time',y='hum_level')

    #Table Promedio datos x hora
    table1['hora']=table1['time'].dt.hour
    b1=table1.groupby(['hora']).mean()
    b1=b1.to_dict()
    nueva_tabla1=pd.DataFrame(b1)

    tbl11=px.line(nueva_tabla1)

    #Caja de vigotes
    tbl111=px.box(table1,y="hum_level")

    #######################################################
    table2=conn.read_data(timestamp_start = '2020-01-01 00:00:00',
                timestamp_end   = '2029-01-01 00:00:00',
                type_ = 'temp',
                verbose = True)

    #Tabla normal
    tbl2=px.line(table2,x='time',y='temp_level')

    #Table Promedio datos x hora
    table2['hora']=table2['time'].dt.hour
    b2=table2.groupby(['hora']).mean()
    b2=b2.to_dict()
    nueva_tabla2=pd.DataFrame(b2)

    tbl22=px.line(nueva_tabla2)

    #Caja de vigotes
    tbl222=px.box(table2,y="temp_level")
    #######################################################
    table3=conn.read_data(timestamp_start = '2020-01-01 00:00:00',
                timestamp_end   = '2029-01-01 00:00:00',
                type_ = 'lux',
                verbose = True)

    #Tabla normal
    tbl3=px.line(table3,x='time',y='lux_level')


    #Table Promedio datos x hora
    table3['hora']=table3['time'].dt.hour
    b3=table3.groupby(['hora']).mean()
    b3=b3.to_dict()
    nueva_tabla=pd.DataFrame(b3)

    tbl33=px.line(nueva_tabla)

    #Caja de vigotes
    tbl333=px.box(table3,y="lux_level")
    #######################################################
    table4=conn.read_data(timestamp_start = '2020-01-01 00:00:00',
                timestamp_end   = '2029-01-01 00:00:00',
                type_ = 'pressure',
                verbose = True)

    #Tabla normal
    tbl4=px.line(table4,x='time',y='pressure_level')

    #Table Promedio datos x hora
    table4['hora']=table4['time'].dt.hour
    b4=table4.groupby(['hora']).mean()
    b4=b4.to_dict()
    nueva_tabla4=pd.DataFrame(b4)

    tbl44=px.line(nueva_tabla4)

    #Caja de vigotes
    tbl444=px.box(table4,y="pressure_level")
    #######################################################
    #DASH
    #######################################################

    #ESTILOS-Graficos

    tbl1.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"} )
    tbl11.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl111.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl2.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl22.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl222.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl3.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl33.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl333.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl4.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl44.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    tbl444.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})

    conn.end_connection()

    #CREACIÓN DE LA APLICACIÓN


    app_dash.layout = html.Div([


    html.H6(children='Medias por hora de cada variable',style={'backgroundColor':"#000000",'color':"#cdced1", 'font':'Arial','textAlign': 'center'}),

    dcc.Dropdown(id='seleccion_prom',
                options=[{'label':'HUMEDAD_Prom','value':'HUMEDAD_Prom'},
                {'label':'TEMPERATURA_Prom','value':'TEMPERATURA_Prom'},
                {'label':'LUX_Prom','value':'LUX_Prom'},
                {'label':'PRESION_Prom','value':'PRESION_Prom'}],
                value='HUMEDAD_Prom',
                multi=False,
                clearable=False,
                style={'width':'50%','font':'Arial','textAlign': 'center'}),
        html.Div([
            dcc.Graph(id='grafico_prom')
        ],style = {'display': 'inline-block', 'width': '95%'}),

    html.H6(children='Caja de vigotes por variable',style={'backgroundColor':"#000000",'color':"#cdced1", 'font':'Arial','textAlign': 'center'}),
    dcc.Dropdown(id='seleccion_box',
                options=[{'label':'HUMEDAD_box','value':'HUMEDAD_box'},
                {'label':'TEMPERATURA_box','value':'TEMPERATURA_box'},
                {'label':'LUX_box','value':'LUX_box'},
                {'label':'PRESION_box','value':'PRESION_box'}],
                value='HUMEDAD_box',
                multi=False,
                clearable=False,
                style={'width':'50%','font':'Arial','textAlign': 'center'}),
        html.Div([
            dcc.Graph(id='grafico_box'),
        ],style = {'display': 'inline-block', 'width': '95%'})


    ],style={'backgroundColor':"#cdced1",'margin':0} )

    @app_dash.callback(
        Output(component_id='grafico_prom',component_property="figure"),
        Input(component_id='seleccion_prom',component_property= 'value')
    )

    def update_graph(seleccion_prom):
        if (seleccion_prom=='HUMEDAD_Prom'):
            return  tbl11
        if (seleccion_prom=='TEMPERATURA_Prom'):
            return tbl22
        if (seleccion_prom=='LUX_Prom'):
            return  tbl33
        if (seleccion_prom=='PRESION_Prom'):
            return  tbl44
        else:
            return "xd"

    @app_dash.callback(
        Output(component_id='grafico_box',component_property="figure"),
        Input(component_id='seleccion_box',component_property= 'value')
    )

    def update_graph(seleccion_prom):
        if (seleccion_prom=='HUMEDAD_box'):
            return  tbl111
        if (seleccion_prom=='TEMPERATURA_box'):
            return tbl222
        if (seleccion_prom=='LUX_box'):
            return  tbl333
        if (seleccion_prom=='PRESION_box'):
            return  tbl444
        else:
            return "xd"

    return app_dash