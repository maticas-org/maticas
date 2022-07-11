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
from dotenv import load_dotenv
import os

# from db_mqtt_interface.db.dirty7w7 import *
from db_mqtt_interface.db.db_connection import db_connection
load_dotenv()

conn = db_connection(db_host =  os.getenv('DB_HOST'),
                     db_name =  os.getenv('DB_NAME'),
                     db_user = os.getenv('DB_USER'),
                     db_password =  os.getenv('DB_PASSWORD'),
                     db_sslmode = os.getenv('DB_SSLMODE')
                    )

ur="/data/"

def create_dash_app(flask_app):
    app_dash = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname=ur)
    
    #Obtener y almacenar valores óptimos y aceptables de cada variable
    inicio  = '2022-01-01 00:00:00'
    fin     = '2023-01-01 00:00:00'
    #Variables del estilo de la página
    fondo   = "#161a28"
    fondo_2 = "#1e2130"
    letra   = "white"
    f_family = "Sans-serif"
    sty_ind={'width': '30%','display': 'inline-block'}

    #funcion para obtener las tablas
    def ob_dat(apodo: str):
        table_aux = conn.read_data(timestamp_start = inicio,
            timestamp_end= fin,

            type_ = apodo)
        return table_aux

    #funcion para obtener el valor actual
    def ac(tabla):
        aux = tabla.iat[len(tabla)-1,1]
        return aux

    #funcion valores optimos y aceptables
    def ol(variable:str):
        ok=variable+"_ok"
        df_aux_a = conn.read_ambiental_settings(config_=ok)
        ok_min   = df_aux_a['min'][0]
        ok_max   = df_aux_a['max'][0]

        op=variable+"_optimal"
        df_aux_o = conn.read_ambiental_settings(config_=op)
        opt_min  = df_aux_o['min'][0]
        opt_max  = df_aux_o['max'][0]

        return ok_min,ok_max, opt_min, opt_max
    
    #funcion para los indicadores
    def indicadores(nombre:str,actual:float,lim_inf:float,lim_sup:float,ok_min:float,ok_max:float,op_min:float,op_max:float):
       
        aux= go.Figure(go.Indicator(
           mode = "gauge+number+delta",
           value = actual,
           domain = {'x': [0, 1], 'y': [0, 1]},
           title = {'text': nombre, 'font': {'size': 24}},
           delta = {'reference': actual, 'increasing': {'color': "#372937"}},
           gauge = {
                'axis': {'range': [lim_inf, lim_sup], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#2d3bb1"},
                'bgcolor': "blue",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                {'range': [lim_inf, ok_min], 'color': '#d14e5a'},
                {'range': [ok_min, op_min], 'color': '#88c2d8'},
                {'range': [op_min, op_max], 'color': '#9AD888'},
                {'range': [op_max, ok_max], 'color': '#88c2d8'},
                {'range': [ok_max, lim_sup], 'color': '#d14e5a'},
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                }}))
        return aux


    
    table_h  = ob_dat("hum")
    table_t  = ob_dat("temp")
    table_ph = ob_dat("ph")
    table_tw = ob_dat("wtemp")
    table_ec = ob_dat("ec")
    table_l  = ob_dat("lux")
  
 
    ac_h  = ac(table_h)
    ac_t  = ac(table_t)
    ac_wt = ac(table_tw)
    ac_ph = ac(table_ph)
    ac_l  = ac(table_l)
    ac_ec = ac(table_ec)

    
    ok_min_ph,ok_max_ph,opt_min_ph,opt_max_ph  = ol("ph")
    ok_min_h,ok_max_h, opt_min_h,opt_max_h     = ol("hum")
    ok_min_t,ok_max_t, opt_min_t,opt_max_t     = ol("temp")
    ok_min_wt,ok_max_wt, opt_min_wt,opt_max_wt = ol("wtemp")
    ok_min_ec,ok_max_ec, opt_min_ec,opt_max_ec = ol("ec") 
    ok_min_l,ok_max_l, opt_min_l,opt_max_l     = ol("lux") 

    fig_IH  = indicadores("Humedad",ac_h,40,90,ok_min_h,ok_max_h,opt_min_h,opt_max_h)
    fig_IPH = indicadores("Ph",ac_ph,4,8.5,ok_min_ph,ok_max_ph,opt_min_ph,opt_max_ph)
    fig_IL  = indicadores("Luz",ac_l/10,25,105,ok_min_l/1000,ok_max_l/1000,opt_min_l/1000,opt_max_l/1000)
    fig_IT  = indicadores("Temperatura",ac_t,10,28,ok_min_t,ok_max_t,opt_min_t,opt_max_t)
    fig_ITW = indicadores("Temperatura del agua",ac_wt,6,21,ok_min_wt,ok_max_wt,opt_min_wt,opt_max_wt)
    fig_IEC = indicadores("Electroconductividad",ac_ec,1,3,ok_min_ec,ok_max_ec,opt_min_ec,opt_max_ec)
   
    
   #modificarle el estilo a la fig
    fig_IEC.update_layout(paper_bgcolor =  fondo_2,  font = {'color': letra, 'family': f_family})
    fig_IT.update_layout(paper_bgcolor  =  fondo,  font = {'color': letra, 'family': f_family})
    fig_ITW.update_layout(paper_bgcolor =  fondo,  font = {'color': letra, 'family': f_family})
    fig_IH.update_layout(paper_bgcolor  =  fondo_2,  font = {'color': letra, 'family': f_family})
    fig_IPH.update_layout(paper_bgcolor =  fondo,  font = {'color': letra, 'family': f_family})
    fig_IL.update_layout(paper_bgcolor  =  fondo_2,  font = {'color': letra, 'family': f_family})

    body= { 'margin': 0}
   
   
    #APP LAYOUT----------------------------
    app_dash.layout =  html.Div(children=[
    
    html.H1(children=[ html.Div(children='HUERTA INTELIGENTE',style={'family': "Courier New",'text-align':"right",'color':"white",'font-style': "italic",'margin-right': 30}),
       #para el cambhio de paginas
       dcc.Link(html.Button("Settings",style={'backgroundColor':"#3d3d43",'color':"white",'height':"30px"}),href="/settings", refresh=True),
       dcc.Link(html.Button("Detailed analysis",style={'backgroundColor':"#3d3d43",'color':"white",'height':"30px"}), href="/detailed_analysis", refresh=True,),
       dcc.Link(html.Button("Data",style={'backgroundColor':"#3d3d43",'color':"white",'height':"30px"}), href="/data", refresh=True)],
       style={'backgroundColor':"black",'color':letra,'family': f_family}),
       
    html.Div(children='''DATOS''', style={ 'fontSize':40,'text-align':"center",'family': f_family}),
    
    html.Div(children='''Aquí encuentra información sobre su cultivo''',style={'fontSize':20, 'text-align':"center",'backgroundColor':fondo_2,'family': f_family,'margin-bottom':"30px"}),
    
   
    html.Div(children=[
      
       html.Div(children='''Convenciones:''',style={'backgroundColor':fondo_2,'text-align':"center"}),
       html.Div(children='''Intervalos  óptimos de las variables en verde ''',style={'backgroundColor':fondo_2,'text-align':"center"}),
       html.Div(children='''Intervalos aceptables  de las variables en azul''',style={'backgroundColor':fondo_2,'text-align':"center"}),
       html.Div(children='''Intervalos  inestables de las variables en rojo ''',style={'backgroundColor':fondo_2,'text-align':"center"}),
       
          ],
          style={'margin-bottom':"30px"}),
       html.Div(children=[ 
        #Mostrar los indicadores
       dcc.Graph(
            id='humedad_i',
            figure=fig_IH,
            style=sty_ind
                ),
        dcc.Graph(
            id='ph_i',
            figure=fig_IPH,
            style=sty_ind
                ),
        dcc.Graph(
            id='l_i',
            figure=fig_IL,
            style=sty_ind
                ),
          ],
        style={'family': letra,'text-align':"center",'color':"white" }
          
  ),

    html.Div(children=[
        
        dcc.Graph(
            id='t_i',
            figure=fig_IT
            ,style=sty_ind
            
        ),
        dcc.Graph(
            id='ec_i',
            figure=fig_IEC
            ,style=sty_ind
        ),
        dcc.Graph(
            id='wt_i',
            figure=fig_ITW
            ,style=sty_ind
            
        ),
     ],
      style={'family': letra,'text-align':"center",'color':"white" }
    ),
    html.Div(children='''     .    ''',style={'fontSize':20, 'text-align':"center",'backgroundColor':fondo,'color':fondo}),
    html.Div(children=[
        html.Div(children='''Seleccione la fecha de inicio y  fin ''',style={'fontSize':20, 'text-align':"center",'backgroundColor':fondo_2,'size':90,'display': 'inline-block','margin-right': "10px"}),
        dcc.DatePickerRange(
        id="fecha",
        display_format='M-D-Y',
        start_date_placeholder_text='M-D-Y',
        style={'backgroundColor':"black",'display': 'inline-block'}),
        dcc.Input(id='h_in', value='00:00:00', type='text', style={'backgroundColor':"#565F8C",'color':"white",'display': 'inline-block','margin': "1em",'height':"35px"}),
        dcc.Input(id='h_fin', value='23:59:59', type='text', style={'backgroundColor':"#565F8C",'color':"white",'display': 'inline-block','height':"35px"}),
        html.Div(children=''' Variable que desea visualizar''',style={'fontSize':20, 'text-align':"center",'backgroundColor':fondo_2,'size':90,'display': 'inline-block','margin': "1em"}),
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
        style={'backgroundColor':"#565F8C",'color':"black",'display': 'inline-block','width': "200px"}
         ),],
        style={'backgroundColor': fondo_2,'height':"100px",'text-align':"center"}
       
    ),
    html.Div(children='''       .  ''',style={'fontSize':20, 'text-align':"center",'backgroundColor':fondo,'color':fondo}),
    html.Div(children=[
     
       #Boton para activdar por primera vez

        html.Button('Ver', id='b_ver', n_clicks=0,
            style={'fontSize':20,'backgroundColor':"#565F8C",'color':"white",'margin-left': "43.5%",'height':"35px",'width': "200px"}),
    ]),
    #calendario
  
    #Input hora
    
    #cuadro de texto de la fecha
   html.Div(children='''         ''',style={'fontSize':20, 'text-align':"center",'backgroundColor':fondo,'color':fondo}),
    html.Div(id='my-div',style={'text-align':"center"}),
    #dropdown para seleccionar las  variables
    

    #llamar la grafica
    dcc.Graph(id='figuraa'), 
   

    ],style={'backgroundColor':fondo,'color':"white", 'font-family': f_family, 'margin-bottom':-25,  'margin-top':-25,'margin-left':-15,'margin-right':-15}) 



    
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
        figuraa.update_traces(line_color='#FFC300')

        figuraa.update_layout(paper_bgcolor = fondo, plot_bgcolor= fondo_2, font = {'color': "white", 'family': f_family})
        
        return figuraa,st

    return app_dash
