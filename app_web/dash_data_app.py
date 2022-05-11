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
print("current working directory: cd .. -> ",  cwd)

import dash
from datetime import date
from dash import dcc
from dash import html
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd

from maticas.db_mqtt_inteface.db.dirty7w7 import *
from maticas.db_mqtt_inteface.db.db_connection import db_connection
conn = db_connection(db_host =  db_host,
                     db_name =  db_name,
                     db_user = db_user,
                     db_password =  db_password,
                     db_sslmode = db_sslmode
                    )



def create_dash_app(flask_app):
    app_dash = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/data/")
    
    #Obtener y almacenar valores óptimos y aceptables de cada variable
    #ph
    inicio='2020-01-01 00:00:00'
    fin= '2029-01-01 00:00:00'
    table_h = conn.read_data(timestamp_start = inicio,
            timestamp_end= fin,
            type_ = "hum")
    table_ph = conn.read_data(timestamp_start = inicio,
            timestamp_end= fin,
            type_ = "ph")
    table_t = conn.read_data(timestamp_start = inicio,
            timestamp_end= fin,
            type_ = "temp")
    table_tw= conn.read_data(timestamp_start = inicio,
            timestamp_end= fin,
            type_ = "wtemp")
    table_ec = conn.read_data(timestamp_start = inicio,
            timestamp_end= fin,
            type_ = "ec")
    table_l = conn.read_data(timestamp_start = inicio,
            timestamp_end= fin,
            type_ = "lux")
    ac_h=table_h.iat[len(table_h)-1,1]
    ac_t=table_t.iat[len(table_t)-1,1]
    ac_tw=table_tw.iat[len(table_tw)-1,1]
    ac_ph=table_ph.iat[len(table_ph)-1,1]
    ac_l=table_l.iat[len(table_l)-1,1]
    ac_ec=table_ec.iat[len(table_ec)-1,1]

    df_ph_a = conn.read_ambiental_settings(config_='ph_ok')
    ok_min_ph= df_ph_a['min'][0]
    ok_max_ph = df_ph_a['max'][0]

    df_ph_o = conn.read_ambiental_settings(config_='ph_optimal')
    opt_min_ph= df_ph_o['min'][0]
    opt_max_ph = df_ph_o['max'][0]

    #humedad
    df_h_a = conn.read_ambiental_settings(config_='hum_ok')
    ok_min_h= df_h_a['min'][0]
    ok_max_h = df_h_a['max'][0]

    df_h_o = conn.read_ambiental_settings(config_='hum_optimal')
    opt_min_h= df_h_o['min'][0]
    opt_max_h = df_h_o['max'][0]
    
    #temperatura
    df_t_a = conn.read_ambiental_settings(config_='temp_ok')
    ok_min_t= df_t_a['min'][0]
    ok_max_t = df_t_a['max'][0]

    df_t_o = conn.read_ambiental_settings(config_='temp_optimal')
    opt_min_t= df_t_o['min'][0]
    opt_max_t = df_t_o['max'][0]

    #temperatura del agua
    df_wt_a = conn.read_ambiental_settings(config_='wtemp_ok')
    ok_min_wt= df_wt_a['min'][0]
    ok_max_wt = df_wt_a['max'][0]

    df_wt_o = conn.read_ambiental_settings(config_='wtemp_optimal')
    opt_min_wt= df_wt_o['min'][0]
    opt_max_wt = df_wt_o['max'][0]

    #Electroconductividad
    df_ec_a = conn.read_ambiental_settings(config_='ec_ok')
    ok_min_ec= df_ec_a['min'][0]
    ok_max_ec = df_ec_a['max'][0]

    df_ec_o = conn.read_ambiental_settings(config_='ec_optimal')
    opt_min_ec= df_ec_o['min'][0]
    opt_max_ec = df_ec_o['max'][0]
    #luz
    df_l_a = conn.read_ambiental_settings(config_='lux_ok')
    ok_min_l= df_l_a['min'][0]
    ok_max_l = df_l_a['max'][0]

    df_l_o = conn.read_ambiental_settings(config_='lux_optimal')
    opt_min_l= df_l_o['min'][0]
    opt_max_l = df_l_o['max'][0]


    #creación de los indicadores
        #Humedad
    fig_IH= go.Figure(go.Indicator(
           mode = "gauge+number+delta",
           value = ac_h,
           domain = {'x': [0, 1], 'y': [0, 1]},
           title = {'text': "Humedad", 'font': {'size': 24}},
           delta = {'reference': ac_h, 'increasing': {'color': "RebeccaPurple"}},
           gauge = {
                'axis': {'range': [40, 90], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "blue",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                {'range': [40, ok_min_h], 'color': 'red'},
                {'range': [ok_min_h, opt_min_h], 'color': 'skyblue'},
                {'range': [opt_min_h, opt_max_h], 'color': 'green'},
                {'range': [opt_max_h, ok_max_h], 'color': 'skyblue'},
                {'range': [ok_max_h, 90], 'color': 'red'},
                
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                }}))
        #Ph
    fig_IPH = go.Figure(go.Indicator(
           mode = "gauge+number+delta",
           value = ac_ph,
           domain = {'x': [0, 1], 'y': [0, 1]},
           title = {'text': "Ph", 'font': {'size': 24}},
           delta = {'reference': ac_ph, 'increasing': {'color': "RebeccaPurple"}},
           gauge = {
           
                'axis': {'range': [4, 8], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                
                'borderwidth': 2,
                'bordercolor': "gray",
                 'steps': [
                {'range': [4, ok_min_ph], 'color': 'red'},
                {'range': [ok_min_ph, opt_min_ph], 'color': 'skyblue'},
                {'range': [opt_min_ph, opt_max_ph], 'color': 'green'},
                {'range': [opt_max_ph, ok_max_ph], 'color': 'skyblue'},
                {'range': [ok_max_ph, 8], 'color': 'red'},
                
                ],
             'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                }}))
        #Luz
    fig_IL = go.Figure(go.Indicator(
           mode = "gauge+number+delta",
           value = ac_l/10,
           domain = {'x': [0, 1], 'y': [0, 1]},
           title = {'text': "Luz", 'font': {'size': 24}},
           delta = {'reference': ac_l/10, 'increasing': {'color': "RebeccaPurple"}},
           gauge = {
           
                'axis': {'range': [25000/1000, 105000/1000], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
               
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                {'range': [25000/1000,  ok_min_l/1000], 'color': 'red'},
                {'range': [ok_min_l/1000, opt_min_l/1000], 'color': 'skyblue'},
                {'range': [opt_min_l/1000, opt_max_l/1000], 'color': 'green'},
                {'range': [opt_max_l/1000, ok_max_l/1000], 'color': 'skyblue'},
                {'range': [ok_max_l/1000, 105000/1000], 'color': 'red'},
                
                
                ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                }}))
        #Temperatura
    fig_IT= go.Figure(go.Indicator(
           mode = "gauge+number+delta",
           value = ac_t, #VALOR ACTUAL QUE TIENE EL SENSOR
           domain = {'x': [0, 1], 'y': [0, 1]},
           title = {'text': "Temperatura", 'font': {'size': 24}}, #'text': NOMBRE DE LA FIGURA, 'font': {'size': 24}
           delta = {'reference':  ac_t, 'increasing': {'color': "RebeccaPurple"}},
           gauge = {
           
                'axis': {'range': [10, 28], 'tickwidth': 1, 'tickcolor': "darkblue"}, #500 ES VALOR MAIXMO QUE PUEDE LLEGAR A TOMAR
                'bar': {'color': "darkblue"},
                
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                {'range': [10, ok_min_t], 'color': 'red'},
                {'range': [ok_min_t, opt_min_t], 'color': 'skyblue'},
                {'range': [opt_min_t, opt_max_t], 'color': 'green'},
                {'range': [opt_max_t, ok_max_t], 'color': 'skyblue'},
                {'range': [ok_max_t, 100], 'color': 'red'},
                
                ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                }}))
        #Temperatura del agua
    fig_ITW= go.Figure(go.Indicator(
           mode = "gauge+number+delta",
           value =ac_tw,
           domain = {'x': [0, 1], 'y': [0, 1]},
           title = {'text': "Temperatura del agua", 'font': {'size': 24}},
           delta = {'reference': ac_tw, 'increasing': {'color': "RebeccaPurple"}},
           gauge = {
                'axis': {'range': [6,21], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "blue",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                {'range': [6, ok_min_wt], 'color': 'red'},
                {'range': [ok_min_wt, opt_min_wt], 'color': 'skyblue'},
                {'range': [opt_min_wt, opt_max_wt], 'color': 'green'},
                {'range': [opt_max_wt, ok_max_wt], 'color': 'skyblue'},
                {'range': [ok_max_wt, 21], 'color': 'red'},
                
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                }}))
   
        #electroconductividad
    fig_IEC= go.Figure(go.Indicator(
           mode = "gauge+number+delta",
           value = ac_ec,
           domain = {'x': [0, 1], 'y': [0, 1]},
           title = {'text': "Electroconductividad", 'font': {'size': 24}},
           delta = {'reference': ac_ec, 'increasing': {'color': "RebeccaPurple"}},
           gauge = {
                'axis': {'range': [1.5, 3], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "blue",
                'borderwidth': 2,
                'bordercolor': "gray",
               'steps': [
                {'range': [0, ok_min_ec], 'color': 'red'},
                {'range': [ok_min_ec, opt_min_ec], 'color': 'skyblue'},
                {'range': [opt_min_ec, opt_max_ec], 'color': 'green'},
                {'range': [opt_max_ec, ok_max_ec], 'color': 'skyblue'},
                {'range': [ok_max_ec, 3], 'color': 'red'},
                
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                }}))
   
   #modificarle el estilo a la fig
    fig_IT.update_layout(paper_bgcolor =    "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    fig_IEC.update_layout(paper_bgcolor = "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    fig_ITW.update_layout(paper_bgcolor = "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    fig_IH.update_layout(paper_bgcolor = "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    fig_IPH.update_layout(paper_bgcolor = "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
    fig_IL.update_layout(paper_bgcolor = "#cdced1", font = {'color': "darkblue", 'family': "Arial"})
   
    #APP LAYOUT----------------------------
    app_dash.layout = html.Div(children=[

    html.H1(children='Datos', className='text-center',style={'backgroundColor':"#000000",'color':"#cdced1", 'font':'Arial'}),
    html.Div(children='''Aquí encuentra información sobre su cultivo'''),
    
    #Mostrar los indicadores
    html.Div(children=[
       html.Div(children='''Intervalos óptimos de las variables en verde'''),
       html.Div(children='''Intervalos óptimos  de las variables en azul'''),
       dcc.Graph(
            id='humedad_i',
            figure=fig_IH,
            style={'width': '30%','display': 'inline-block'}
        ),
        dcc.Graph(
            id='ph_i',
            figure=fig_IPH,
            style={'width': '30%','display': 'inline-block'}
        ),
        dcc.Graph(
            id='l_i',
            figure=fig_IL,
            style={'width': '30%','display': 'inline-block','backgroundColor':'blue'}
        ),
       
        
     ],
    #style={"border":"2px gray solid","border-radius": "25px",},
   
    
    
    ),
    html.Div(children=[
    
        dcc.Graph(
            id='t_i',
            figure=fig_IT
            ,style={'width': '30%','display': 'inline-block'}
            
        ),
        dcc.Graph(
            id='ec_i',
            figure=fig_IEC
            ,style={'width': '30%','display': 'inline-block'}
            
        
            
        ),
        dcc.Graph(
            id='wt_i',
            figure=fig_ITW
            ,style={'width': '30%','display': 'inline-block'}
            
        ),
     ],
    #style={"border":"2px gray solid","border-radius": "25px"},
   
    
    
    ),
    
    #calendario
    dcc.DatePickerRange(
        id="fecha",
        display_format='M-D-Y',
        start_date_placeholder_text='M-D-Y',
        style={'backgroundColor':"#cdced1;"}
    ),
    #Input hora
    dcc.Input(id='h_in', value='00:00:00', type='text'),
    dcc.Input(id='h_fin', value='23:59:59', type='text'),
    #Boton para activdar por primera vez
    html.Button('Ver', id='b_ver', n_clicks=0),
    #cuadro de texto de la fecha
    html.Div(id='my-div'),
    #dropdown para seleccionar las  variables
    dcc.Dropdown( id = 'menu',
        options = [
            {'label':'Humedad', 'value':'hum' },
            {'label': 'Temperatura', 'value':'temp'},
            {'label': 'Luz', 'value':'lux'},
            {'label': 'Ph', 'value':'ph'},
            {'label': 'Presión', 'value':'pressure'},
            {'label': 'Temperatura del agua', 'value':'wtemp'},
            {'label': 'Electroconductividad', 'value':'ec'},
             ],
        style={'backgroundColor':"#e4e4e6;"}
      ),

    #llamar la grafica
    dcc.Graph(id='figuraa'),  
     

    ],style={'backgroundColor':'#cdced1'}) 

    #Aquí es donde recibe los inputs y dice dónde son los outputs
    @app_dash.callback( 
        dash.dependencies.Output("figuraa","figure"),
        dash.dependencies.Output("my-div","children"),
        dash.dependencies.Input("menu","value"),
        dash.dependencies.Input('fecha', 'start_date'),
        dash.dependencies.Input('fecha', 'end_date'),
        dash.dependencies.Input('b_ver', 'n_clicks'),
        dash.dependencies.Input('h_in', 'value'),
        dash.dependencies.Input('h_fin', 'value'),
    )
    #función para crear la gráfica según los inputs
    def update_graph(value,start_date,end_date,n_clicks,h_in,h_fin):
        #string del mensaje con la fecha seleccionada
        
        st=" "
        #nombre de la variable, por default muestra la gráfica de humedad
        y_1="hum_level"
        #nombre de la tabla
        t_n="hum" 
        inicio='2020-01-01 00:00:00'
        fin= '2029-01-01 00:00:00'
        
        #VISTA DEFAULT ANTES DE INICIALIZAR EL GRÁFICO CON EL BOTÓN "VER"
        if len(h_in)!=8:
            h_in="00:00:00"
        if len(h_fin)!=8:
            h_fin="00:00:00"
        
        if int(h_in[0])>2 or int(h_in[3])>5  or int(h_in[6])>5:
            h_in="00:00:00"
            st="Ingrese un nuevo valor"
        if int(h_fin[0])>2 or int(h_fin[3])>5  or int(h_fin[6])>5:
            h_in="00:00:00"
            st="Ingrese un nuevo valor"
        

        #AL PRESIONAR VER SE INICIALIZA LA VISTA DEL GRÁFICO SELECCIONADO
        if n_clicks !=0:
            if len(h_in)!=8:
                h_in="00:00:00"
            if len(h_fin)!=8:
                h_fin="00:00:00"
        
            if int(h_in[0])>2 or int(h_in[3])>5  or int(h_in[6])>5:
                h_in="00:00:00"
                st="Ingrese un nuevo valor"
            if int(h_fin[0])>2 or int(h_fin[3])>5  or int(h_fin[6])>5:
                h_in="00:00:00"
                st="Ingrese un nuevo valor"
                inicio='2022-01-01'
                fin='2022-01-10'
            if start_date is not None:
                inicio=start_date+" "+h_in
            if end_date is not None:
                fin=end_date+" "+h_fin
            

            #SABER EL TIPO DE VARIABLE SEGÚN LO QUE EL USUARIO DESEA
            if value=="hum":
                y_1='hum_level'
                t_n=value
            elif value=="ph":
                y_1='ph_level'
                t_n=value
            elif value=="temp":
                y_1='temp_level'
                t_n=value
            elif value=="pressure":
                y_1='pressure_level'
                t_n=value
            elif value=="lux":
                y_1='lux_level'
                t_n=value
            elif value=="wtemp":
                y_1='wtemp_level'
                t_n=value
            elif value=="ec":
                y_1='ec_level'
                t_n=value
            st="Graficando datos desde " + start_date +" "+ h_in +" hasta " + end_date + " " + h_fin

        #cerar la table según el input
        table1 = conn.read_data(timestamp_start = inicio,
            timestamp_end= fin,
            type_ = t_n)
      
        #definir la gráfica según la tabla
        figuraa = px.line(table1, x='time', y=y_1)
        figuraa.update_layout(paper_bgcolor = "#cdced1", font = {'color': "black", 'family': "Arial"})
        
        return figuraa,st

    return app_dash