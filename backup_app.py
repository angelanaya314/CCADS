

# IMPORTACIÓN DE LAS LIBRERÍAS
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from PIL import Image

#------------------------------------------------------------------------------------------------#
#------- Configuración de Streamlit ----------
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

#------------------------------------------------------------------------------------------------#
#------- Navigation Menu ----------
option_selected = option_menu(
	menu_title=None,
	options=["Planeación financiera", "Escenarios", "Indicadores"],
    orientation="horizontal",
    icons=["person-circle","calculator-fill","graph-up-arrow"],
    styles={"nav-link": {"--hover-color": "white"}}
)
#------------------------------------------------------------------------------------------------#
#------- Caché to download DataFrame as CSV ----------
df = pd.read_excel("BD_DocTour.xlsx")
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

#------------------------------------------------------------------------------------------------#
#FUNCIONES

def worksheets_a_dataframe(nombre_libro, nombre_hoja):
    wb = load_workbook(nombre_libro)
    ws = wb[nombre_hoja]
    data = ws.values
    columnas_df = next(data)[0:]
    df = pd.DataFrame(data, columns = columnas_df)
    indices_df = df.iloc[:, 0]
    df.set_index(indices_df, inplace = True)
    df = df.iloc[:, 1:]
    return df

def utilidad_antes_de_impuestos(df_ingresos, df_comisiones_totales, df_costos_fijos_totales):
    uadi = pd.DataFrame()
    uadi["Básica"] = df_ingresos["Básica"] - df_comisiones_totales["Básica"] - df_costos_fijos_totales["Básica"]
    uadi["Black"] = df_ingresos["Black"] - df_comisiones_totales["Black"] - df_costos_fijos_totales["Black"]
    uadi["Platino"] = df_ingresos["Platino"] - df_comisiones_totales["Platino"] - df_costos_fijos_totales["Platino"]
    return uadi

def incremento_membresias(df_membresias, tasa_incremento):
    df_membresias_nuevas = pd.DataFrame()
    df_membresias_nuevas["Básica"] = df_membresias["Básica"]*(1+ (tasa_incremento/100))
    df_membresias_nuevas["Black"] = df_membresias["Black"]*(1 + (tasa_incremento/100))
    df_membresias_nuevas["Platino"] = df_membresias["Platino"]*(1 + (tasa_incremento/100))
    return df_membresias_nuevas

def decremento_membresias(df_membresias, tasa_decremento):
    df_membresias_nuevas = pd.DataFrame()
    df_membresias_nuevas["Básica"] = df_membresias["Básica"]*(1 - (tasa_decremento/100))
    df_membresias_nuevas["Black"] = df_membresias["Black"]*(1 - (tasa_decremento/100))
    df_membresias_nuevas["Platino"] = df_membresias["Platino"]*(1 - (tasa_decremento/100))
    return df_membresias_nuevas

def guardar_dataframes(nombre_libro, df, name_df):
    with pd.ExcelWriter(nombre_libro, mode = "a", engine = "openpyxl", if_sheet_exists = "replace") as writer:
        df.round(decimals = 2)
        df.astype(str)
        df.to_excel(writer, sheet_name = name_df)

#------------------------------------------------------------------------------------------------#
# SIDEBAR
sidebar = st.sidebar

#------------------------------------------------------------------------------------------------#
# IMPORTACIÓN DE LA BASE DE DATOS

nombre_libro = "BD_DocTour.xlsx"

# Comisiones
hoja_1 = "1_Comisiones"
comisiones_314 = worksheets_a_dataframe(nombre_libro, hoja_1)

# Costos fijos
hoja_2 = "1_CostosFijos"
costos_fijos_314 = worksheets_a_dataframe(nombre_libro, hoja_2)

# Precios
hoja_3 = "1_Precios"
precios_314 = worksheets_a_dataframe(nombre_libro, hoja_3)

# Membresías proyectadas a tres meses
hoja_4 = "1_MembresíasProyectadas_3"
membresias_proyectadas_3_314 = worksheets_a_dataframe(nombre_libro, hoja_4)

# Membresías proyectadas a seis meses
hoja_5 = "1_MembresíasProyectadas_6"
membresias_proyectadas_6_314 = worksheets_a_dataframe(nombre_libro, hoja_5)

# Tasas
hoja_6 = "1_Tasas"
tasas_314 = worksheets_a_dataframe(nombre_libro, hoja_6)

#------------------------------------------------------------------------------------------------#

if option_selected == "Planeación financiera":

    DocTour = Image.open("DocTour-cutout.png")
    sidebar.image(DocTour, width=250)
    sidebar.markdown("")
    sidebar.markdown("")
    sidebar.markdown("<h1 style='text-align: left; color: #195419; font-size: 1.5rem;'>Planeación financiera</h1>", unsafe_allow_html=True)
    sidebar.header("`Métricas y escenarios`")

    # Información de la Página
    expansion = st.expander ("Acerca de")
    expansion.markdown("""* *Planeación financiera* Aquí se abordan los componentes principales de la aplicación, los que permiten modificar las variables pertinentes de la organización. Entre las que podemos encontrar: Número de membresías, Cantidad de meses a mostrar, Tasa de interés, Precios, Porcentaje de comisiones y costos fijos. """)
    membresias = sidebar.multiselect("Membresías:", ["Básica","Black","Platino"], default=["Básica","Black","Platino"])
    
    if ("Básica" in membresias) & ("Black" in membresias) & ("Platino" in membresias):

        # CONFIGURACIÓN DE LA PÁGINA Y EL SIDEBAR

        col1, col2, col3 = st.columns(3)
        col1.metric("Membresías Básicas","65","+ 5")
        col2.metric("Membresías Black","35","+ 3")
        col3.metric("Membresías Platino","0","0")
        style_metric_cards(border_left_color = "#27AE60")
        
        st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Inputs de planeación financiera</h1>", unsafe_allow_html=True)
        st.write(" --- ")

        # MESES A PROYECTAR Y SOLICITUD DE VALORES
        columna1, columna2 = st.columns((2,3))
        columna1.write("<h1 style='text-align: center; font-size: 1.2rem;'>Meses a proyectar:</h1>", unsafe_allow_html=True)
        meses = columna2.radio(" ",(3, 6), horizontal=True)
       
        # ba = Membresía básica, bl = Membresía black, pl = Membresía platino
        # m1 = Mes 1, m2 = Mes 2, m3 = Mes 3
        if meses == 6:

            # FECHAS
            def month_name(date):
                months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
                month_name = months[date - 1]
                return month_name
            fecha_actual = date.today()
            mes_actual = fecha_actual.month
            month_n = month_name(mes_actual)

            lista_meses_futuros = []
            for i in range(meses):
                valor = fecha_actual + relativedelta(months = i + 1)
                lista_meses_futuros.append(valor)
            #st.write(lista_meses_futuros)

            st.write(" --- ")
            
            # MEMBRESÍAS PROYECTADAS
            colum1, colum2, colum3, colum4 = st.columns((1,1,1,1))
            colum1.markdown("<h1 style='text-align: center; font-size: 1.2rem;'></h1>", unsafe_allow_html=True)
            colum2.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Básica</h1>", unsafe_allow_html=True)
            colum3.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Black</h1>", unsafe_allow_html=True)
            colum4.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Platino</h1>", unsafe_allow_html=True)
            colum1.markdown("")
            colum1.markdown("")
            colum1.markdown("")
            # Mes 1
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 1</h1>", unsafe_allow_html=True)
            ba_m1 = colum2.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[0,0], min_value = 0, max_value = 10000, step = 1, key = "ba_m1")
            bl_m1 = colum3.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[0,1], min_value = 0, max_value = 10000, step = 1, key = "bl_m1")
            pl_m1 = colum4.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[0,2], min_value = 0, max_value = 10000, step = 1, key = "pl_m1")
            colum1.markdown("")
            # Mes 2
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 2</h1>", unsafe_allow_html=True)
            ba_m2 = colum2.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[1,0], min_value = 0, max_value = 10000, step = 1, key = "ba_m2")
            bl_m2 = colum3.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[1,1], min_value = 0, max_value = 10000, step = 1, key = "bl_m2")
            pl_m2 = colum4.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[1,2], min_value = 0, max_value = 10000, step = 1, key = "pl_m2")
            colum1.markdown("")
            # Mes 3
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 3</h1>", unsafe_allow_html=True)
            ba_m3 = colum2.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[2,0], min_value = 0, max_value = 10000, step = 1, key = "ba_m3")
            bl_m3 = colum3.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[2,1], min_value = 0, max_value = 10000, step = 1, key = "bl_m3")
            pl_m3 = colum4.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[2,2], min_value = 0, max_value = 10000, step = 1, key = "pl_m3")
            colum1.markdown("")
            # Mes 4
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 4</h1>", unsafe_allow_html=True)
            ba_m4 = colum2.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[3,0], min_value = 0, max_value = 10000, step = 1, key = "ba_m4")
            bl_m4 = colum3.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[3,1], min_value = 0, max_value = 10000, step = 1, key = "bl_m4")
            pl_m4 = colum4.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[3,2], min_value = 0, max_value = 10000, step = 1, key = "pl_m4")
            colum1.markdown("")
            # Mes 5
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 5</h1>", unsafe_allow_html=True)
            ba_m5 = colum2.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[4,0], min_value = 0, max_value = 10000, step = 1, key = "ba_m5")
            bl_m5 = colum3.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[4,1], min_value = 0, max_value = 10000, step = 1, key = "bl_m5")
            pl_m5 = colum4.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[4,2], min_value = 0, max_value = 10000, step = 1, key = "pl_m5")
            colum1.markdown("")
            # Mes 6
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 6</h1>", unsafe_allow_html=True)
            ba_m6 = colum2.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[5,0], min_value = 0, max_value = 10000, step = 1, key = "ba_m6")
            bl_m6 = colum3.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[5,1], min_value = 0, max_value = 10000, step = 1, key = "bl_m6")
            pl_m6 = colum4.number_input(label = "a", label_visibility = "hidden", value = membresias_proyectadas_6_314.iloc[5,2], min_value = 0, max_value = 10000, step = 1, key = "pl_m6")
            colum1.markdown("")

            m1 = [ba_m1, ba_m2, ba_m3, ba_m4, ba_m5, ba_m6]
            m2 = [bl_m1, bl_m2, bl_m3, bl_m4, bl_m5, bl_m6]
            m3 = [pl_m1, pl_m2, pl_m3, pl_m4, pl_m5, pl_m6]
            df_membresias_actualizadas = pd.DataFrame(list(zip(m1, m2, m3)), columns = ['Básica','Black','Platino'])
            #st.write(df_membresias_actualizadas)
            st.write(" --- ")

            # TASA DE INTERÉS (INFLACIÓN E IMPUESTOS)
            columna1, columna2 = st.columns((2,3))
            columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Tasas de interés</h1>", unsafe_allow_html=True)
            
            colum1, colum2= st.columns((1,3))
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de inflación</h1>", unsafe_allow_html=True)
            tasa_inflacion = colum2.slider(label = "a", label_visibility = "hidden", value = float(tasas_314.iloc[0,0]), min_value = 0.00, max_value = 100.0, step = 1.00, key = "tasa_inflacion")
            colum1.markdown(" ")
            colum1.markdown(" ")
            colum1.markdown(" ")
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de impuestos</h1>", unsafe_allow_html=True)
            tasa_impuestos = colum2.slider(label = "a", label_visibility = "hidden", value = float(tasas_314.iloc[1,0]), min_value = 0.00, max_value = 100.00, step = 1.00, key = "tasa_impuestos")

            t1 = [tasa_inflacion, tasa_impuestos]
            df_tasas_actualizadas = pd.DataFrame(list(zip(t1)), columns = ['Valor'])
            #st.write(df_tasas_actualizadas)
            st.write(" --- ")

            # PRECIOS DE MEMBRESÍAS
            columna1, columna2 = st.columns((2,3))
            columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Precios</h1>", unsafe_allow_html=True)
            colum1, colum2, colum3, colum4 = st.columns((1,1,1,1))
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Precios por membresía</h1>", unsafe_allow_html=True)
            ba_precios = colum2.number_input(label = "Membresía básica: ", label_visibility = "visible", value = float(precios_314.iloc[0,0]), min_value = 0.0, max_value = 1000.0, step = 1.0, key = "ba_precio")
            bl_precios = colum3.number_input(label = "Membresía black: ", label_visibility = "visible", value = float(precios_314.iloc[0,1]), min_value = 0.0, max_value = 1000.0, step = 1.0, key = "bl_precio")
            pl_precios = colum4.number_input(label = "Membresía platino: ", label_visibility = "visible", value = float(precios_314.iloc[0,2]), min_value = 0.0, max_value = 1000.0, step = 1.0, key = "pl_precio")
            
            df_precios_actualizados = pd.DataFrame()                
            df_precios_actualizados["Básica"] = [ba_precios]
            df_precios_actualizados["Black"] = [bl_precios] 
            df_precios_actualizados["Platino"] = [pl_precios]

            # INGRESOS MENSUALES EN EL ESCENARIO MÁS PROBABLE

            ba_ingresos_actualizados = df_membresias_actualizadas["Básica"]*ba_precios
            bl_ingresos_actualizados = df_membresias_actualizadas["Black"]*bl_precios
            pl_ingresos_actualizados = df_membresias_actualizadas["Platino"]*pl_precios
            df_ingresos_actualizados = pd.DataFrame(list(zip(ba_ingresos_actualizados, bl_ingresos_actualizados, pl_ingresos_actualizados)), columns = ['Básica','Black','Platino'])
            #st.write(df_ingresos_actualizados)
            st.write(" --- ")
            
            # PORCENTAJES DE COMISIONES
            columna1, columna2 = st.columns((2,3))
            columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Porcentajes de comisiones:</h1>", unsafe_allow_html=True)
            colum1, colum2, colum3, colum4 = st.columns((1,1,1,1))
            colum1.markdown("")
            colum1.markdown("")
            colum1.markdown("")
            #--- Comisión del vendedor ---
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Comisión del vendedor:</h1>", unsafe_allow_html=True)
            ba_com_ven = colum2.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[0,0]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "ba_com_ven")
            bl_com_ven = colum3.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[0,1]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "bl_com_vem")
            pl_com_ven = colum4.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[0,2]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "pl_com_ven")
            colum1.markdown("")
            #--- Comisión de referencia ---
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Comisión de referencia</h1>", unsafe_allow_html=True)
            ba_com_ref = colum2.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[1,0]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "ba_com_ref")
            bl_com_ref = colum3.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[1,1]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "bl_com_ref")
            pl_com_ref = colum4.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[1,2]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "pl_com_ref")
            colum1.markdown("")
            #--- Comisión financiera ---
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Comisión financiera</h1>", unsafe_allow_html=True)
            ba_com_fin = colum2.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[2,0]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "ba_com_fin")
            bl_com_fin = colum3.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[2,1]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "bl_com_fin")
            pl_com_fin = colum4.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[2,2]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "pl_com_fin")
            colum1.markdown("")
            #--- Comisión de marketing ---
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Comisión de marketing</h1>", unsafe_allow_html=True)
            ba_com_mkt = colum2.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[3,0]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "ba_com_mkt")
            bl_com_mkt = colum3.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[3,1]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "bl_com_mkt")
            pl_com_mkt = colum4.number_input(label = "a", label_visibility = "hidden", value = float(comisiones_314.iloc[3,2]), min_value = 0.0, max_value = 100.0, step = 0.1, key = "pl_com_mkt")
            colum1.markdown("")

            l1_1 = [ba_com_ven, ba_com_ref, ba_com_fin, ba_com_mkt]
            l2_1 = [bl_com_ven, bl_com_ref, bl_com_fin, bl_com_mkt]
            l3_1 = [pl_com_ven, pl_com_ref, pl_com_fin, pl_com_mkt]
            df_porc_comisiones_actualizadas = pd.DataFrame(list(zip(l1_1, l2_1, l3_1)), columns = ['Básica','Black','Platino'])

            l1_2 = list(map(lambda x: x*ba_precios/100, l1_1))
            l2_2 = list(map(lambda x: x*bl_precios/100, l2_1))
            l3_2 = list(map(lambda x: x*pl_precios/100, l3_1))
            
            df_comisiones_actualizadas = pd.DataFrame(list(zip(l1_2, l2_2, l3_2)), columns = ['Básica','Black','Platino'])
            df_comisiones_totales_actualizadas = pd.DataFrame()                
            df_comisiones_totales_actualizadas["Básica"] = [df_comisiones_actualizadas["Básica"].sum()]
            df_comisiones_totales_actualizadas["Black"] = [df_comisiones_actualizadas["Black"].sum()] 
            df_comisiones_totales_actualizadas["Platino"] = [df_comisiones_actualizadas["Platino"].sum()]
            #st.write(df_comisiones_totales_actualizadas)
            
            # COSTOS FIJOS
            st.write(" --- ")
            columna1, columna2 = st.columns((2,3))
            columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Costos fijos:</h1>", unsafe_allow_html=True)
            
            columna2.markdown(" ")
            columna2.markdown(" ")
            columna2.markdown(" ")

            columna1.write("<h1 style='text-align: center; font-size: 1.2rem;'>Tipo de análisis:</h1>", unsafe_allow_html=True)
            tipo_analisis = columna2.radio(" ",("Costos fijos totales por membresía","Desglose de costos fijos por membresía"), horizontal=True)

            colum1, colum2, colum3, colum4 = st.columns((1,1,1,1))

            if tipo_analisis == "Desglose de costos fijos por membresía":

                columna2.markdown(" ")
                columna2.markdown(" ")
                columna2.markdown(" ")


                # Call center / oficinas
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Call center / oficinas:</h1>", unsafe_allow_html=True)
                ba_costo_1 = colum2.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[0,0]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_1")
                bl_costo_1 = colum3.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[0,1]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_1")
                pl_costo_1 = colum4.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[0,2]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_1")
                colum1.markdown(" ")
                colum1.markdown(" ")
                
                # Medicina general
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Medicina general:</h1>", unsafe_allow_html=True)
                ba_costo_2 = colum2.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[1,0]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_2")
                bl_costo_2 = colum3.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[1,1]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_2")
                pl_costo_2 = colum4.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[1,2]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_2")
                colum1.markdown(" ")
                colum1.markdown(" ")
                
                # Nutrición
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Nutrición:</h1>", unsafe_allow_html=True)
                ba_costo_3 = colum2.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[2,0]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_3")
                bl_costo_3 = colum3.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[2,1]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_3")
                pl_costo_3 = colum4.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[2,2]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_3")
                colum1.markdown(" ")
                colum1.markdown(" ")

                # Psicología
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Psicología:</h1>", unsafe_allow_html=True)
                ba_costo_4 = colum2.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[3,0]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_4")
                bl_costo_4 = colum3.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[3,1]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_4")
                pl_costo_4 = colum4.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[3,2]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_4")
                colum1.markdown(" ")
                colum1.markdown(" ")

                # Asistencias y seguros básicos
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Asistencias y seguros básicos:</h1>", unsafe_allow_html=True)
                ba_costo_5 = colum2.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[4,0]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_5")
                bl_costo_5 = colum3.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[4,1]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_5")
                pl_costo_5 = colum4.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[4,2]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_5")
                colum1.markdown(" ")
                colum1.markdown(" ")

                # Plataforma de descuentos + Wellness
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Plataforma de descuentos + Wellness:</h1>", unsafe_allow_html=True)
                ba_costo_6 = colum2.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[5,0]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_6")
                bl_costo_6 = colum3.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[5,1]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_6")
                pl_costo_6 = colum4.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[5,2]), min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_6")
                colum1.markdown(" ")
                colum1.markdown(" ")

                # Segunda opinión médica + Farm + Telemedicina
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Segunda opinión médica + Farm + Telemedicina:</h1>", unsafe_allow_html=True)
                ba_costo_7 = colum2.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[6,0]), disabled = True, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_7")
                bl_costo_7 = colum3.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[6,1]), disabled = True, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_7")
                pl_costo_7 = colum4.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[6,2]), disabled = False, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_7")
                colum1.markdown(" ")

                # Doce meses de sueldo por muerte accidental
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Asistencias y seguros básicos:</h1>", unsafe_allow_html=True)
                ba_costo_8 = colum2.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[7,0]), disabled = True, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_8")
                bl_costo_8 = colum3.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[7,1]), disabled = True, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_8")
                pl_costo_8 = colum4.number_input(label = "a", label_visibility = "hidden", value = float(costos_fijos_314.iloc[7,2]), disabled = False, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_8")
                colum1.markdown(" ")


                l1 = [ba_costo_1, ba_costo_2, ba_costo_3, ba_costo_4, ba_costo_5, ba_costo_6, ba_costo_7, ba_costo_8]
                l2 = [bl_costo_1, bl_costo_2, bl_costo_3, bl_costo_4, bl_costo_5, bl_costo_6, bl_costo_7, bl_costo_8]
                l3 = [pl_costo_1, pl_costo_2, pl_costo_3, pl_costo_4, pl_costo_5, pl_costo_6, pl_costo_7, pl_costo_8]
                df_costos_fijos_actualizados = pd.DataFrame(list(zip(l1, l2, l3)), columns = ['Básica','Black','Platino'])
                
                df_costos_fijos_totales_actualizados = pd.DataFrame()                
                df_costos_fijos_totales_actualizados["Básica"] = [df_costos_fijos_actualizados["Básica"].sum()]
                df_costos_fijos_totales_actualizados["Black"] = [df_costos_fijos_actualizados["Black"].sum()] 
                df_costos_fijos_totales_actualizados["Platino"] = [df_costos_fijos_actualizados["Platino"].sum()]

            elif tipo_analisis == "Costos fijos totales por membresía":
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Costos fijos totales por membresía</h1>", unsafe_allow_html=True)
                ba_costos_fijos_totales_inicial = costos_fijos_314["Básica"].astype(float).sum()
                bl_costos_fijos_totales_inicial = costos_fijos_314["Black"].astype(float).sum()
                pl_costos_fijos_totales_inicial = costos_fijos_314["Platino"].astype(float).sum()
                
                ba_costos_fijos_totales_actualizados = colum2.number_input(label = "Membresía básica: ", label_visibility = "visible", value = 106.0, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "ba_costos_fijos_totales")
                bl_costos_fijos_totales_actualizados = colum3.number_input(label = "Membresía black: ", label_visibility = "visible", value = 109.0, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "bl_costos_fijos_totales")
                pl_costos_fijos_totales_actualizados = colum4.number_input(label = "Membresía platino: ", label_visibility = "visible", value = 167.25, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "pl_costos_fijos_totales")
                
                l1 = [ba_costos_fijos_totales_actualizados]
                l2 = [bl_costos_fijos_totales_actualizados]
                l3 = [pl_costos_fijos_totales_actualizados]
                df_costos_fijos_totales_actualizados = pd.DataFrame(list(zip(l1, l2, l3)), columns = ['Básica','Black','Platino'])
                
                st.write(" --- ")

            # Utilidades antes de impuestos
            uadi_por_membresia = utilidad_antes_de_impuestos(df_precios_actualizados, df_comisiones_totales_actualizadas, df_costos_fijos_totales_actualizados)
            ba_uadi = uadi_por_membresia["Básica"][0]*df_membresias_actualizadas["Básica"]
            bl_uadi = uadi_por_membresia["Black"][0]*df_membresias_actualizadas["Black"]
            pl_uadi = uadi_por_membresia["Platino"][0]*df_membresias_actualizadas["Platino"]
            df_uadi = pd.DataFrame(list(zip(ba_uadi, bl_uadi, pl_uadi)), columns = ['Básica','Black','Platino'])
            df_uadi_mes = df_uadi.sum(axis = 1)
            df_uadi_mes.rename(index={0:'Mes 1',1:'Mes 2',2:'Mes 3'}, inplace=True)

            # Utilidades netas
            ba_un = df_uadi["Básica"]*(1-(tasa_impuestos/100))
            bl_un = df_uadi["Black"]*(1-(tasa_impuestos/100))
            pl_un = df_uadi["Platino"]*(1-(tasa_impuestos/100))
            df_un = pd.DataFrame(list(zip(ba_un, bl_un, pl_un)), columns = ['Básica','Black','Platino'])
            df_un_mes = df_un.sum(axis = 1)
            df_un_mes.rename(index={0:'Mes 1',1:'Mes 2',2:'Mes 3'}, inplace=True)


            col1, col2, col3, col4 = st.columns(4)  
            resultado = col3.button("Guardar datos")
            st.write(" --- ")
            if resultado == True:
                guardar_dataframes(nombre_libro, df_porc_comisiones_actualizadas, "1_Comisiones")
                if tipo_analisis == "Desglose de costos fijos por membresía":
                    guardar_dataframes(nombre_libro, df_costos_fijos_actualizados, "1_CostosFijos")
                else:
                    guardar_dataframes(nombre_libro, df_costos_fijos_totales_actualizados, "1_CostosFijosTotales")
                guardar_dataframes(nombre_libro, df_precios_actualizados, "1_Precios")
                guardar_dataframes(nombre_libro, df_membresias_actualizadas, "1_MembresíasProyectadas_6")
                guardar_dataframes(nombre_libro, df_tasas_actualizadas, "1_Tasas")
                resultado = False

        elif meses == 3:
            st.write()


    #-----------------------------------------------------------------------------------------------------------------------------#
    
    elif ("Básica" in membresias) & ("Black" in membresias):
    
    # CONFIGURACIÓN DE LA PÁGINA Y EL SIDEBAR
        col1, col2 = st.columns(2)
        col1.metric("Membresías Básicas","65","+ 5")
        col2.metric("Membresías Black","35","+ 3")
        style_metric_cards()

        
        st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Inputs de planeación financiera</h1>", unsafe_allow_html=True)
        st.write(" ")
        
        columna1, columna2 = st.columns((2,3))
        columna1.write("<h1 style='text-align: center; font-size: 1.2rem;'>Meses a proyectar:</h1>", unsafe_allow_html=True)
        meses = columna2.radio(" ",(3, 6, 9, 12), horizontal=True)

        colum1, colum2, colum3 = st.columns((1,1,1))

        # ba = Membresía básica, bl = Membresía black, pl = Membresía platino
        # m1 = Mes 1, m2 = Mes 2, m3 = Mes 3
        if meses == 3:

            colum1.markdown("<h1 style='text-align: center; font-size: 1.2rem;'></h1>", unsafe_allow_html=True)
            colum2.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Básica</h1>", unsafe_allow_html=True)
            colum3.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Black</h1>", unsafe_allow_html=True)

            colum1.markdown("")
            colum1.markdown("")
            colum1.markdown("")
            
            # Mes 1
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 1</h1>", unsafe_allow_html=True)
            ba_m1 = colum2.number_input(label = "a", label_visibility = "hidden", min_value = 0, max_value = 10000, step = 1, key = "ba_m1")
            bl_m1 = colum3.number_input(label = "a", label_visibility = "hidden", min_value = 0, max_value = 10000, step = 1, key = "bl_m1")
            colum1.markdown("")
            # Mes 2
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 2</h1>", unsafe_allow_html=True)
            ba_m2 = colum2.number_input(label = "a", label_visibility = "hidden", min_value = 0, max_value = 10000, step = 1, key = "ba_m2")
            bl_m2 = colum3.number_input(label = "a", label_visibility = "hidden", min_value = 0, max_value = 10000, step = 1, key = "bl_m2")
            colum1.markdown("")
            # Mes 3
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 3</h1>", unsafe_allow_html=True)
            ba_m3 = colum2.number_input(label = "a", label_visibility = "hidden", min_value = 0, max_value = 10000, step = 1, key = "ba_m3")
            bl_m3 = colum3.number_input(label = "a", label_visibility = "hidden", min_value = 0, max_value = 10000, step = 1, key = "bl_m3")

            membresias_mes = [ba_m1 + bl_m1, ba_m1 + bl_m1, ba_m1 + bl_m1]

        elif meses == 3:
            st.write()
 

    # Pie de página
    Column1, Column2,Column3, Column4 = st.columns ((2,4,1,2))
    DocTour = Image.open("DocTour-cutout.png")
    Column4.markdown("")
    Column4.image(DocTour, width=200)

    Column2.markdown("<h1 style='text-align: center; color: #195419; font-size: 0.8rem;'>AVISO LEGAL | POLÍTICAS DE PRIVACIDAD | AVISO DE PRIVACIDAD</h1>", unsafe_allow_html=True)
    Column2.markdown("<h1 style='text-align: center; color: #195419; font-size: 0.8rem;'>©CCADS CONSULTING | TODOS LOS DERECHOS RESERVADOS</h1>", unsafe_allow_html=True)

    CCA = Image.open("CCADS.jpeg")
    Column1.image(CCA, width=100) 

#-----------------------------------------------------------------------------------------------------------------------------#
elif option_selected == "Escenarios": 
    #Información de la Página
    expansion = st.expander ("Acerca de")
    expansion.markdown("""* *Planeación financiera* Aquí se abordan los componentes principales de la aplicación, los que permiten modificar las variables pertinentes de la organización. Entre las que podemos encontrar: Número de membresías, Cantidad de meses a mostrar, Tasa de interés, Precios, Porcentaje de comisiones y costos fijos.""")

    porc_comisiones = pd.read_excel("BD_DocTour.xlsx", sheet_name="1_Comisiones", index_col=0)
    costos_fijos = pd.read_excel("BD_DocTour.xlsx", sheet_name="1_CostosFijos", index_col=0)
    precios = pd.read_excel("BD_DocTour.xlsx", sheet_name="1_Precios", index_col=0)
    membresias_proyectadas = pd.read_excel("BD_DocTour.xlsx", sheet_name="1_MembresíasProyectadas_6", index_col=0)

    #------ ESCENARIO MÁS PROBABLE ---------#
    st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Número de membresías proyectadas</h1>", unsafe_allow_html=True)

    columna1, columna2 = st.columns((2,3))
    columna2.write(membresias_proyectadas)
    st.write(" ")

    st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Escenario más probable</h1>", unsafe_allow_html=True)
    st.write(" ")
    st.write("<h1 style='text-align: center; font-size: 1.2rem;'>Utilidades netas considerando inflación</h1>", unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")

    # COSTOS FIJOS POR MEMBRESÍA
    df_costos_fijos_1 = pd.DataFrame()                
    df_costos_fijos_1["Básica"] = [costos_fijos["Básica"].sum()]
    df_costos_fijos_1["Black"] = [costos_fijos["Black"].sum()] 
    df_costos_fijos_1["Platino"] = [costos_fijos["Platino"].sum()]


    # COSTOS FIJOS TOTALES EN EL ESCENARIO MÁS PROBABLE
    ba_costos_totales_1 = membresias_proyectadas["Básica"]*df_costos_fijos_1["Básica"][0]
    bl_costos_totales_1 = membresias_proyectadas["Black"]*df_costos_fijos_1["Black"][0]
    pl_costos_totales_1 = membresias_proyectadas["Platino"]*df_costos_fijos_1["Platino"][0]
    df_costos_totales_1 = pd.DataFrame(list(zip(ba_costos_totales_1, bl_costos_totales_1, pl_costos_totales_1)), columns = ['Básica','Black','Platino'])

    # INGRESOS MENSUALES EN EL ESCENARIO MÁS PROBABLE
    ba_ingresos_1 = membresias_proyectadas["Básica"]*precios["Básica"][0]
    bl_ingresos_1 = membresias_proyectadas["Black"]*precios["Black"][0]
    pl_ingresos_1 = membresias_proyectadas["Platino"]*precios["Platino"][0]
    df_ingresos_1 = pd.DataFrame(list(zip(ba_ingresos_1, bl_ingresos_1, pl_ingresos_1)), columns = ['Básica','Black','Platino'])
    #st.write(" INGRESOS ")
    #st.write(df_ingresos_1)
    #st.write(" --- ")

    # COMISIONES POR MEMBRESÍA
    l1_2 = list(map(lambda x: x*precios["Básica"][0]/100, porc_comisiones["Básica"]))
    l2_2 = list(map(lambda x: x*precios["Black"][0]/100, porc_comisiones["Black"]))
    l3_2 = list(map(lambda x: x*precios["Platino"][0]/100, porc_comisiones["Platino"]))
            
    df_comisiones_1 = pd.DataFrame(list(zip(l1_2, l2_2, l3_2)), columns = ['Básica','Black','Platino'])
    df_comisiones_por_membresia_1 = pd.DataFrame()                
    df_comisiones_por_membresia_1["Básica"] = [df_comisiones_1["Básica"].sum()]
    df_comisiones_por_membresia_1["Black"] = [df_comisiones_1["Black"].sum()] 
    df_comisiones_por_membresia_1["Platino"] = [df_comisiones_1["Platino"].sum()]
    #st.write(df_comisiones_por_membresia_1)

    ba_comisiones_totales_1 = membresias_proyectadas["Básica"]*df_comisiones_por_membresia_1["Básica"][0]
    bl_comisiones_totales_1 = membresias_proyectadas["Black"]*df_comisiones_por_membresia_1["Black"][0]
    pl_comisiones_totales_1 = membresias_proyectadas["Platino"]*df_comisiones_por_membresia_1["Platino"][0]
    df_comisiones_totales_1 = pd.DataFrame(list(zip(ba_comisiones_totales_1, bl_comisiones_totales_1, pl_comisiones_totales_1)), columns = ['Básica','Black','Platino'])
    #st.write(" COMISIONES TOTALES ")
    #st.write(df_comisiones_totales_1)
    #st.write(" --- ")

    # Utilidades antes de impuestos
    #uadi_por_membresia_1 = utilidad_antes_de_impuestos(df_ingresos_1, df_comisiones_totales_1, df_costos_fijos_totales)

    ba_uadi_1 = df_ingresos_1["Básica"] - df_comisiones_totales_1["Básica"] - df_costos_totales_1["Básica"]
    bl_uadi_1 = df_ingresos_1["Black"] - df_comisiones_totales_1["Black"] - df_costos_totales_1["Black"]
    pl_uadi_1 = df_ingresos_1["Platino"] - df_comisiones_totales_1["Platino"] - df_costos_totales_1["Platino"]
    df_uadi_1 = pd.DataFrame(list(zip(ba_uadi_1, bl_uadi_1, pl_uadi_1)), columns = ['Básica','Black','Platino'])
    #st.write(" UADI ")
    df_uadi_mes_1 = df_uadi_1.sum(axis = 1)
    #st.write(df_uadi)
    #st.write(df_uadi_mes)
    #st.write(" --- ")
    
    # Utilidades netas
    tasa_impuestos_1 = 30
    ba_un_1 = df_uadi_1["Básica"]*(1-(tasa_impuestos_1/100))
    bl_un_1 = df_uadi_1["Black"]*(1-(tasa_impuestos_1/100))
    pl_un_1 = df_uadi_1["Platino"]*(1-(tasa_impuestos_1/100))
    #st.write(" Utilidades netas ")
    df_un_1 = pd.DataFrame(list(zip(ba_un_1, bl_un_1, pl_un_1)), columns = ['Básica','Black','Platino'])
    df_un_mes_1 = df_un_1.sum(axis = 1)
    #st.write(df_un)
    #st.write(df_un_mes_1)
    #st.write(" --- ")

    # Utilidades considerando inflación
    tasa_inflacion_1 = 6.85
    ba_un_inflacion_1 = df_un_1["Básica"]*(1-(tasa_inflacion_1/100))
    bl_un_inflacion_1 = df_un_1["Black"]*(1-(tasa_inflacion_1/100))
    pl_un_inflacion_1 = df_un_1["Platino"]*(1-(tasa_inflacion_1/100))
    #st.write(" Utilidades netas considerando inflación")
    df_un_inflacion_1 = pd.DataFrame(list(zip(ba_un_inflacion_1, bl_un_inflacion_1, pl_un_inflacion_1)), columns = ['Básica','Black','Platino'])
    df_un_inflacion_mes_1 = df_un_inflacion_1.sum(axis = 1)
    #st.write(df_un)
    columna1, columna2, columna3 = st.columns((1,2,3))
    columna2.write("")
    columna2.write("")
    columna2.write("")
    columna2.write("")
    columna2.write(df_un_inflacion_1)
    fig3 = px.line(
        data_frame=df_un_inflacion_1,
        color_discrete_map={"Básica":"#23B223","Black":"#2F7A2C","Platino":"#0A4A08"},
        markers=True
    )
    fig3.update_traces(line = dict(width = 4))
    columna3.write(fig3)
    st.write(" --- ")
    
    #-----------------------------------------------------------------------------------------------------------------------------#
    #------ ESCENARIO OPTIMISTA ---------#
    #st.write(membresias_proyectadas)
    st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Escenario optimista</h1>", unsafe_allow_html=True)
    st.write(" ")
    
    # VARIABLES A MODIFICAR (INFLACIÓN E IMPUESTOS)
    columna1, columna2 = st.columns((2,3))
    columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Variables a considerar</h1>", unsafe_allow_html=True)
    
    colum1, colum2= st.columns((1,3))
    colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de inflación</h1>", unsafe_allow_html=True)
    tasa_inflacion_2 = colum2.slider(label = "a", label_visibility = "hidden", value =  6.85, min_value = 0.00, max_value = 6.85, step = 1.0, key = "tasa_inflacion_2")
    colum1.markdown(" ")
    colum1.markdown(" ")
    colum1.markdown(" ")
    colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de impuestos</h1>", unsafe_allow_html=True)
    tasa_impuestos_2 = colum2.slider(label = "a", label_visibility = "hidden", value = 30.0, min_value = 0.0, max_value = 30.0, step = 1.0, key = "tasa_impuestos_2")
    colum1.markdown(" ")
    colum1.markdown(" ")
    colum1.markdown(" ")
    colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de incremento mensual en membresías vendidas</h1>", unsafe_allow_html=True)
    tasa_incremento_2 = colum2.slider(label = "a", label_visibility = "hidden", value = 5.0, min_value = 0.0, max_value = 100.0, step = 1.0, key = "tasa_incrementos_2")
    
    df_membresias_optimistas = incremento_membresias(membresias_proyectadas, tasa_incremento_2)
    #st.write(df_membresias_optimistas)

    # COSTOS FIJOS TOTALES EN EL ESCENARIO OPTIMISTA
    ba_costos_totales_2 = df_membresias_optimistas["Básica"]*df_costos_fijos_1["Básica"][0]
    bl_costos_totales_2 = df_membresias_optimistas["Black"]*df_costos_fijos_1["Black"][0]
    pl_costos_totales_2 = df_membresias_optimistas["Platino"]*df_costos_fijos_1["Platino"][0]
    df_costos_totales_2 = pd.DataFrame(list(zip(ba_costos_totales_2, bl_costos_totales_2, pl_costos_totales_2)), columns = ['Básica','Black','Platino'])
    #st.write(" COSTOS TOTALES ")
    #st.write(df_costos_totales_2)
    #st.write(" --- ")
    #st.write(" --- ")

    # INGRESOS MENSUALES EN EL ESCENARIO OPTIMISTA
    ba_ingresos_2 = df_membresias_optimistas["Básica"]*precios["Básica"][0]
    bl_ingresos_2 = df_membresias_optimistas["Black"]*precios["Black"][0]
    pl_ingresos_2 = df_membresias_optimistas["Platino"]*precios["Platino"][0]
    df_ingresos_2 = pd.DataFrame(list(zip(ba_ingresos_2, bl_ingresos_2, pl_ingresos_2)), columns = ['Básica','Black','Platino'])
    #st.write(" INGRESOS ")
    #st.write(df_ingresos_1)
    #st.write(" --- ")

    # COMISIONES TOTALES EN EL ESCENARIO OPTIMISTA
    ba_comisiones_totales_2 = df_membresias_optimistas["Básica"]*df_comisiones_por_membresia_1["Básica"][0]
    bl_comisiones_totales_2 = df_membresias_optimistas["Black"]*df_comisiones_por_membresia_1["Black"][0]
    pl_comisiones_totales_2 = df_membresias_optimistas["Platino"]*df_comisiones_por_membresia_1["Platino"][0]
    df_comisiones_totales_2 = pd.DataFrame(list(zip(ba_comisiones_totales_2, bl_comisiones_totales_2, pl_comisiones_totales_2)), columns = ['Básica','Black','Platino'])
    #st.write(" COMISIONES TOTALES ")
    #st.write(df_comisiones_totales_2)
    #st.write(" --- ")

    # Utilidades antes de impuestos
    #uadi_por_membresia_1 = utilidad_antes_de_impuestos(df_ingresos_1, df_comisiones_totales_1, df_costos_fijos_totales)

    ba_uadi_2 = df_ingresos_2["Básica"] - df_comisiones_totales_2["Básica"] - df_costos_totales_2["Básica"]
    bl_uadi_2 = df_ingresos_2["Black"] - df_comisiones_totales_2["Black"] - df_costos_totales_2["Black"]
    pl_uadi_2 = df_ingresos_2["Platino"] - df_comisiones_totales_2["Platino"] - df_costos_totales_2["Platino"]
    df_uadi_2 = pd.DataFrame(list(zip(ba_uadi_2, bl_uadi_2, pl_uadi_2)), columns = ['Básica','Black','Platino'])
    #st.write(" UADI ")
    df_uadi_mes_2 = df_uadi_2.sum(axis = 1)
    #st.write(df_uadi)
    #st.write(df_uadi_mes)
    #st.write(" --- ")
    
    # Utilidades netas
    ba_un_2 = df_uadi_2["Básica"]*(1-(tasa_impuestos_2/100))
    bl_un_2 = df_uadi_2["Black"]*(1-(tasa_impuestos_2/100))
    pl_un_2 = df_uadi_2["Platino"]*(1-(tasa_impuestos_2/100))
    #st.write(" Utilidades netas ")
    df_un_2 = pd.DataFrame(list(zip(ba_un_2, bl_un_2, pl_un_2)), columns = ['Básica','Black','Platino'])
    df_un_mes_2 = df_un_2.sum(axis = 1)
    #st.write(df_un)
    #st.write(df_un_mes_1)
    #st.write(" --- ")

    # Utilidades considerando inflación
    ba_un_inflacion_2 = df_un_2["Básica"]*(1-(tasa_inflacion_2/100))
    bl_un_inflacion_2 = df_un_2["Black"]*(1-(tasa_inflacion_2/100))
    pl_un_inflacion_2 = df_un_2["Platino"]*(1-(tasa_inflacion_2/100))
    st.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Utilidades netas considerando inflación</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    df_un_inflacion_2 = pd.DataFrame(list(zip(ba_un_inflacion_2, bl_un_inflacion_2, pl_un_inflacion_2)), columns = ['Básica','Black','Platino'])
    df_un_inflacion_mes_2 = df_un_inflacion_2.sum(axis = 1)
    #st.write(df_un)
    columna1, columna2, columna3 = st.columns((1,2,3))
    columna1.write("")
    columna1.write("")
    columna1.write("")
    columna2.write("")
    columna2.write("")
    columna2.write("")
    columna2.write("")
    columna2.write(df_un_inflacion_2)
    fig4 = px.line(
        data_frame=df_un_inflacion_2,
        color_discrete_map={"Básica":"#23B223","Black":"#2F7A2C","Platino":"#0A4A08"},
        markers=True
    )
    fig4.update_traces(line = dict(width = 4))
    columna3.write(fig4)
    st.write(" --- ")

    #-----------------------------------------------------------------------------------------------------------------------------#
    #------ ESCENARIO PESIMISTA ---------#
    #st.write(membresias_proyectadas)
    st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Escenario pesimista</h1>", unsafe_allow_html=True)
    st.write(" ")
    
    # VARIABLES A MODIFICAR (INFLACIÓN E IMPUESTOS)
    columna1, columna2 = st.columns((2,3))
    columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Variables a considerar</h1>", unsafe_allow_html=True)
    
    colum1, colum2= st.columns((1,3))
    colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de inflación</h1>", unsafe_allow_html=True)
    tasa_inflacion_3 = colum2.slider(label = "a", label_visibility = "hidden", value =  6.85, min_value = 6.85, max_value = 100.0, step = 1.0, key = "tasa_inflacion_3")
    colum1.markdown(" ")
    colum1.markdown(" ")
    colum1.markdown(" ")
    colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de impuestos</h1>", unsafe_allow_html=True)
    tasa_impuestos_3 = colum2.slider(label = "a", label_visibility = "hidden", value = 30.0, min_value = 30.0, max_value = 100.0, step = 1.0, key = "tasa_impuestos_3")
    colum1.markdown(" ")
    colum1.markdown(" ")
    colum1.markdown(" ")
    colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de decremento mensual en membresías vendidas</h1>", unsafe_allow_html=True)
    tasa_decremento_3 = colum2.slider(label = "a", label_visibility = "hidden", value = 5.0, min_value = 0.0, max_value = 100.0, step = 1.0, key = "tasa_incrementos_3")
    
    df_membresias_pesimistas = decremento_membresias(membresias_proyectadas, tasa_decremento_3)
    #st.write(df_membresias_pesimista)

    # COSTOS FIJOS TOTALES EN EL ESCENARIO PESIMISTA
    ba_costos_totales_3 = df_membresias_pesimistas["Básica"]*df_costos_fijos_1["Básica"][0]
    bl_costos_totales_3 = df_membresias_pesimistas["Black"]*df_costos_fijos_1["Black"][0]
    pl_costos_totales_3 = df_membresias_pesimistas["Platino"]*df_costos_fijos_1["Platino"][0]
    df_costos_totales_3 = pd.DataFrame(list(zip(ba_costos_totales_3, bl_costos_totales_3, pl_costos_totales_3)), columns = ['Básica','Black','Platino'])
    #st.write(" COSTOS TOTALES ")
    #st.write(df_costos_totales_2)
    #st.write(" --- ")
    #st.write(" --- ")

    # INGRESOS MENSUALES EN EL ESCENARIO PESIMISTA
    ba_ingresos_3 = df_membresias_pesimistas["Básica"]*precios["Básica"][0]
    bl_ingresos_3 = df_membresias_pesimistas["Black"]*precios["Black"][0]
    pl_ingresos_3 = df_membresias_pesimistas["Platino"]*precios["Platino"][0]
    df_ingresos_3 = pd.DataFrame(list(zip(ba_ingresos_3, bl_ingresos_3, pl_ingresos_3)), columns = ['Básica','Black','Platino'])
    #st.write(" INGRESOS ")
    #st.write(df_ingresos_1)
    #st.write(" --- ")

    # COMISIONES TOTALES EN EL ESCENARIO PESIMISTA
    ba_comisiones_totales_3 = df_membresias_pesimistas["Básica"]*df_comisiones_por_membresia_1["Básica"][0]
    bl_comisiones_totales_3 = df_membresias_pesimistas["Black"]*df_comisiones_por_membresia_1["Black"][0]
    pl_comisiones_totales_3 = df_membresias_pesimistas["Platino"]*df_comisiones_por_membresia_1["Platino"][0]
    df_comisiones_totales_3 = pd.DataFrame(list(zip(ba_comisiones_totales_3, bl_comisiones_totales_3, pl_comisiones_totales_3)), columns = ['Básica','Black','Platino'])
    #st.write(" COMISIONES TOTALES ")
    #st.write(df_comisiones_totales_2)
    #st.write(" --- ")

    # Utilidades antes de impuestos
    #uadi_por_membresia_1 = utilidad_antes_de_impuestos(df_ingresos_1, df_comisiones_totales_1, df_costos_fijos_totales)

    ba_uadi_3 = df_ingresos_3["Básica"] - df_comisiones_totales_3["Básica"] - df_costos_totales_3["Básica"]
    bl_uadi_3 = df_ingresos_3["Black"] - df_comisiones_totales_3["Black"] - df_costos_totales_3["Black"]
    pl_uadi_3 = df_ingresos_3["Platino"] - df_comisiones_totales_3["Platino"] - df_costos_totales_3["Platino"]
    df_uadi_3 = pd.DataFrame(list(zip(ba_uadi_3, bl_uadi_3, pl_uadi_3)), columns = ['Básica','Black','Platino'])
    #st.write(" UADI ")
    df_uadi_mes_3 = df_uadi_3.sum(axis = 1)
    #st.write(df_uadi)
    #st.write(df_uadi_mes)
    #st.write(" --- ")
    
    # Utilidades netas
    ba_un_3 = df_uadi_3["Básica"]*(1-(tasa_impuestos_3/100))
    bl_un_3 = df_uadi_3["Black"]*(1-(tasa_impuestos_3/100))
    pl_un_3 = df_uadi_3["Platino"]*(1-(tasa_impuestos_3/100))
    #st.write(" Utilidades netas ")
    df_un_3 = pd.DataFrame(list(zip(ba_un_3, bl_un_3, pl_un_3)), columns = ['Básica','Black','Platino'])
    df_un_mes_3 = df_un_3.sum(axis = 1)
    #st.write(df_un)
    #st.write(df_un_mes_1)
    #st.write(" --- ")

    # Utilidades considerando inflación
    ba_un_inflacion_3 = df_un_3["Básica"]*(1-(tasa_inflacion_3/100))
    bl_un_inflacion_3 = df_un_3["Black"]*(1-(tasa_inflacion_3/100))
    pl_un_inflacion_3 = df_un_3["Platino"]*(1-(tasa_inflacion_3/100))

    st.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Utilidades netas considerando inflación</h1>", unsafe_allow_html=True)

    df_un_inflacion_3 = pd.DataFrame(list(zip(ba_un_inflacion_3, bl_un_inflacion_3, pl_un_inflacion_3)), columns = ['Básica','Black','Platino'])
    df_un_inflacion_mes_3 = df_un_inflacion_3.sum(axis = 1)
    #st.write(df_un)
    columna1, columna2, columna3 = st.columns((1,2,3))
    columna1.write("")
    columna1.write("")
    columna1.write("")
    columna2.write("")
    columna2.write("")
    columna2.write("")
    columna2.write("")
    columna2.write("")
    columna2.write(df_un_inflacion_3)
    columna3.write("")
    fig5 = px.line(
        data_frame=df_un_inflacion_3,
        color_discrete_map={"Básica":"#23B223","Black":"#2F7A2C","Platino":"#0A4A08"},
        markers=True
    )
    fig5.update_traces(line = dict(width = 4))
    columna3.write(fig5)
    st.write(" --- ")

    #Combinar dataframes
    df_utilidades_escenarios = pd.DataFrame()
    df_utilidades_escenarios["Escenario más probable"] = df_un_inflacion_mes_1
    df_utilidades_escenarios["Escenario optimista"] = df_un_inflacion_mes_2
    df_utilidades_escenarios["Escenario pesimista"] = df_un_inflacion_mes_3

    st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Comparación de escenarios</h1>", unsafe_allow_html=True)
    columna1, columna2, columna3 = st.columns((1,2,3))
    st.write(" ")
    columna2.write(" ")
    columna2.write(" ")
    columna2.write(" ")
    columna2.write(" ")
    columna2.write(df_utilidades_escenarios)
    fig6 = px.line(
        data_frame=df_utilidades_escenarios,
        color_discrete_map={"Escenario más probable":"#23B223","Escenario optimista":"#2F7A2C","Escenario pesimista":"#0A4A08"},
        markers=True
    )
    fig6.update_traces(line = dict(width = 4))
    columna3.write(fig6)
    st.write(" --- ")

    Column1, Column2,Column3, Column4 = st.columns ((2,4,1,2))
    DocTour = Image.open("DocTour-cutout.png")
    Column4.markdown("")
    Column4.image(DocTour, width=200)

    Column2.markdown("<h1 style='text-align: center; color: #195419; font-size: 0.8rem;'>AVISO LEGAL | POLÍTICAS DE PRIVACIDAD | AVISO DE PRIVACIDAD</h1>", unsafe_allow_html=True)
    Column2.markdown("<h1 style='text-align: center; color: #195419; font-size: 0.8rem;'>©CCADS CONSULTING | TODOS LOS DERECHOS RESERVADOS</h1>", unsafe_allow_html=True)


    CCA = Image.open("CCADS.jpeg")
    Column1.image(CCA, width=100)
#-----------------------------------------------------------------------------------------------------------------------------#
elif option_selected == "Indicadores": 

    # Información de la Página
    expansion = st.expander ("Acerca de")
    expansion.markdown("""* *Planeación financiera* Aquí se abordan los componentes principales de la aplicación, los que permiten modificar las variables pertinentes de la organización. Entre las que podemos encontrar: Número de membresías, Cantidad de meses a mostrar, Tasa de interés, Precios, Porcentaje de comisiones y costos fijos.""")
    df_dash= pd.read_excel("BD_DocTour.xlsx",sheet_name="3_Membresías")   
      
    ab1, ab2 = st.columns((3,2))
    ab1.markdown("<h1 style='text-align: center; color: #195419; font-size: 1.5rem;'>Número de ususarios por membresías</h1>", unsafe_allow_html=True)
    fig = px.bar(df_dash, x="Membresias", y="Cantidad ",color=["#23B223", "#2F7A2C", "#0A4A08"],color_discrete_map="identity")
    ab1.plotly_chart(fig)

    values=[65,35,100]
    labels=["Básica","Black","Platino"]
    ab2.markdown("<h1 style='text-align: center; color: #195419; font-size: 1.5rem;'>Gráfica de pastel del número de membresías</h1>", unsafe_allow_html=True)

    fig2 = px.pie(values=values, names=labels, color=labels, color_discrete_map={"Básica":"#23B223","Black":"#2F7A2C","Platino":"#0A4A08"})
    fig2.update_traces(textinfo='value', textfont_size=20,hole=0.2,
                  marker=dict(line=dict(color='#BACEB9', width=2)))
    ab2.plotly_chart(fig2)

    st.write(" --- ")

    #------- Serie de tiempo Margen  ----------
    df_Margen= pd.read_excel("BD_DocTour.xlsx",sheet_name="3_Margen")
    ac1, ac2 = st.columns((3,2)) 
    ac1.markdown("<h1 style='text-align: center; color: #195419; font-size: 1.5rem;'>Tiempo vs Margenes</h1>", unsafe_allow_html=True)
    fig = px.line(df_Margen,x="Tiempo" ,y="Margenes",markers=True, text="Margenes")
    fig.update_traces(textposition="bottom right")
    fig.update_yaxes(tickformat=".2%")
    fig.update_traces(line_color="green")
    fig.update_traces(line = dict(width = 4))
    ac1.plotly_chart(fig) 

    colors = ["#23B223",] * 5
    colors[0]="#0A4A08"

    ac2.markdown("<h1 style='text-align: center; color: #195419; font-size: 1.5rem;'>Mes con menor margen</h1>", unsafe_allow_html=True)
    fig3 = go.Figure(data=[go.Bar(
    x=['Enero', "Febrero", "Marzo",
       'Abril', 'Mayo'],
    y=[10, 11, 12, 13, 14],
    marker_color=colors)])

    ac2.plotly_chart(fig3)
    
    st.write(" --- ")

    #------- Serie de tiempo utilidad   ----------
    df_Utilidad = pd.read_excel("BD_DocTour.xlsx",sheet_name="3_Utilidad")

    ad1, ad2, ad3 = st.columns((4,1.5,1.5))
    ad1.markdown("<h1 style='text-align: center; color: #195419; font-size: 1.5rem;'>Tiempo vs Utilidad</h1>", unsafe_allow_html=True)
    fig = px.line(df_Utilidad ,x="Tiempo" ,y="Utilidad",markers=True, text="Utilidad")
    fig.update_traces(textposition="bottom right")
    fig.update_traces(line_color="green")
    fig.update_traces(line = dict(width = 4))
    ad1.plotly_chart(fig)

    ad2.markdown("")
    ad2.markdown("")
    ad2.markdown("")
    ad2.markdown("")
    ad2.markdown("")
    ad2.markdown("")
    ad2.markdown("")
    ad2.markdown("<h1 style='text-align: center; font-size: 2.2rem;'>Mejor mes</h1>", unsafe_allow_html=True)
    ad2.markdown("<h1 style='text-align: center; color: #23B223; font-size: 4.4rem;'>Junio</h1>", unsafe_allow_html=True)

    ad3.markdown("")
    ad3.markdown("")
    ad3.markdown("")
    ad3.markdown("")
    ad3.markdown("")
    ad3.markdown("")
    ad3.markdown("")
    ad3.markdown("<h1 style='text-align: center; font-size: 2.2rem;'>Utilidad total</h1>", unsafe_allow_html=True)
    ad3.markdown("<h1 style='text-align: center; color: #23B223; font-size: 4.4rem;'>6000</h1>", unsafe_allow_html=True)

    st.write(" --- ")
    #------- Diagrama de barras % de utilización  ----------
    df_Porcentaje = pd.read_excel("BD_DocTour.xlsx",sheet_name="3_Porcentaje  de utilización")  

    ae1, ae2, ae3 = st.columns((4,1.5,1.5))
    ae1.markdown("<h1 style='text-align: center; color: #195419; font-size: 1.5rem;'>Porcentaje de utilización de cada servicio</h1>", unsafe_allow_html=True)
    fig = px.bar(df_Porcentaje, x="% de utilización", y="Servicios",
    hover_data=['% de utilización', 'Servicios'], color='% de utilización', color_continuous_scale="Aggrnyl")
    fig.update_yaxes(tickformat=".2%")
    
    ae1.plotly_chart(fig)

    ae2.markdown("")
    ae2.markdown("")
    ae2.markdown("")
    ae2.markdown("")
    ae2.markdown("")
    ae2.markdown("<h1 style='text-align: center; font-size: 2.2rem;'>Servicio más utilizado</h1>", unsafe_allow_html=True)
    ae2.markdown("<h1 style='text-align: center; color: #23B223; font-size: 4.4rem;'>Medicina general</h1>", unsafe_allow_html=True)

    ae3.markdown("")
    ae3.markdown("")
    ae3.markdown("")
    ae3.markdown("")
    ae3.markdown("")
    ae3.markdown(f"<h1 style='text-align: center; font-size: 2.2rem;'>% de utilización</h1>", unsafe_allow_html=True)
    ae3.markdown("<h1 style='text-align: center; color: #23B223; font-size: 4.4rem;'>25%</h1>", unsafe_allow_html=True) 

    st.write(" --- ")

    Column1, Column2,Column3, Column4 = st.columns ((2,4,1,2))
    DocTour = Image.open("DocTour-cutout.png")
    Column4.markdown("")
    Column4.image(DocTour, width=200)

    Column2.markdown("<h1 style='text-align: center; color: #195419; font-size: 0.8rem;'>AVISO LEGAL | POLÍTICAS DE PRIVACIDAD | AVISO DE PRIVACIDAD</h1>", unsafe_allow_html=True)
    Column2.markdown("<h1 style='text-align: center; color: #195419; font-size: 0.8rem;'>©CCADS CONSULTING | TODOS LOS DERECHOS RESERVADOS</h1>", unsafe_allow_html=True)


    CCA = Image.open("CCADS.jpeg")
    Column1.image(CCA, width=100)                               
