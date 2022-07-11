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
from dotenv import load_dotenv
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# from db_mqtt_interface.db.dirty7w7 import *
from db_mqtt_interface.db.db_connection import db_connection

load_dotenv()

conn = db_connection(db_host =  os.getenv('DB_HOST'),
                     db_name =  os.getenv('DB_NAME'),
                     db_user = os.getenv('DB_USER'),
                     db_password =  os.getenv('DB_PASSWORD'),
                     db_sslmode = os.getenv('DB_SSLMODE')
                    )

def create_dash_app_2(flask_app):
    app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/detailed_analysis/")

    fondo   = "#161a28"
    fondo_2 = "#161a28"
    fondo_g = "#1e2130"
    letra   = "white"
    f_family = "Sans-serif"

    table1=conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'hum',
               verbose = True)
    #Tabla normal
    my_plot1 = table1.plot("time", "hum_level", kind="line")
    tbl1=px.line(table1,x='time',y='hum_level')

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

    app.layout = html.Div([

        html.H1(children=[html.Div(children='HUERTA INTELIGENTE',
                                style={'family': "Courier New", 'text-align': "right", 'color': "white", 'margin': 0,
                                        'font-style': "italic"}),
                        # para el cambhio de paginas
                        dcc.Link(html.Button("Settings",
                                            style={'backgroundColor': "#3d3d43", 'color': "white", 'size': "20px"}),
                                href="/settings", refresh=True),
                        dcc.Link(html.Button("Detailed analysis",
                                            style={'backgroundColor': "#3d3d43", 'color': "white", 'size': "20px"}),
                                href="/detailed_analysis", refresh=True, ),
                        dcc.Link(
                            html.Button("Data", style={'backgroundColor': "#3d3d43", 'color': "white", 'size': "20px"}),
                            href="/data", refresh=True)],
                style={'backgroundColor': "black", 'color': 'letra', 'family': 'f_family', 'size': "40px"}),

        html.Div(children='''Detailed Analisis''', style={'fontSize': 40, 'text-align': "center", 'family': 'f_family'}),
        html.Div(children='''''',
                style={'fontSize': 20, 'text-align': "center", 'backgroundColor': 'fondo', 'color': 'fondo'}),
        html.Div(children='''''',
                style={'fontSize': 20, 'text-align': "center", 'backgroundColor': 'fondo_g', 'family': 'f_family'}),



    html.H5(children='Medias por hora de cada variable',style={'backgroundColor':"#000000",'color':"#cdced1", 'font':'bold','textAlign': 'center'}),
    dcc.Dropdown(id='seleccion_prom',
                options=[{'label':'Promedio por horas x Humedad','value':'HUMEDAD_Prom'},
                {'label':'Promedio por horas x Temperatura','value':'TEMPERATURA_Prom'},
                {'label':'Promedio por horas x Lux','value':'LUX_Prom'},
                {'label':'Promedio por horas x Presion','value':'PRESION_Prom'}],
                value='HUMEDAD_Prom',
                multi=False,
                clearable=False,
                style={'width':'100%','font':'Bold','textAlign': 'center' ,'align-items': 'center', 'justify-content': 'center'}),
        html.Div([
            dcc.Graph(id='grafico_prom')
        ],style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

    html.H5(children='Caja de vigotes por variable',style={'backgroundColor':"#000000",'color':"#cdced1", 'font':'bold','textAlign': 'center'}),
    dcc.Dropdown(id='seleccion_box',
                options=[{'label':'Caja de vigotes x Humedad','value':'HUMEDAD_box'},
                {'label':'Caja de vigotes x Temperatura','value':'TEMPERATURA_box'},
                {'label':'Caja de vigotes x Lux','value':'LUX_box'},
                {'label':'Caja de vigotes x Presion','value':'PRESION_box'}],
                value='HUMEDAD_box',
                multi=False,
                clearable=False,
                style={'width':'100%','font':'Bold','textAlign': 'center' ,'align-items': 'center', 'justify-content': 'center'}),
        html.Div([
            dcc.Graph(id='grafico_box'),
        ],style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})


    ],style={'backgroundColor': fondo,'color':"161a28", 'font-family': f_family,'margin':0, 'height':'100vh', 
             'width':'100%', 'height':'100%', 'top':'0px', 'left':'0px'})

    @app.callback(
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
    @app.callback(
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

    return app
