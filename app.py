

# IMPORTACIÓN DE LAS LIBRERÍAS
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from PIL import Image

#------------------------------------------------------------------------------------------------#
# IMPORTACIÓN DE LA BASE DE DATOS
df = pd.read_excel("BD_DocTour.xlsx")

#------------------------------------------------------------------------------------------------#
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
#This code helps to hide the main menu of Streamlit
#hide_st_style = """
#			<style>
#			#MainMenu {visibility: hidden;}
#			footer {visibility: hidden;}
#			header {visibility: hidden;}
#			</style>
#			"""
#st.markdown(hide_st_style, unsafe_allow_html=True)

#------------------------------------------------------------------------------------------------#
#------- Navigation Menu ----------
option_selected = option_menu(
	menu_title=None,
	options=["Planeación financiera", "Escenarios", "Indicadores"],
    orientation="horizontal"
)
#------------------------------------------------------------------------------------------------#
#------- Caché to download DataFrame as CSV ----------
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')
#------------------------------------------------------------------------------------------------#
# SIDEBAR
sidebar = st.sidebar

#------------------------------------------------------------------------------------------------#
#FUNCIONES
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

if option_selected == "Planeación financiera":

    DocTour = Image.open("DocTour-cutout.png")
    sidebar.image(DocTour, width=250)
    sidebar.markdown("")
    sidebar.markdown("")
    sidebar.markdown("<h1 style='text-align: left; color: #195419; font-size: 1.5rem;'>Planeación financiera</h1>", unsafe_allow_html=True)
    sidebar.header("`Métricas y escenarios`")

    membresias = sidebar.multiselect("Membresías:", ["Básica","Black","Platino"], default=["Básica","Black","Platino"])
    if ("Básica" in membresias) & ("Black" in membresias) & ("Platino" in membresias):
    
    # CONFIGURACIÓN DE LA PÁGINA Y EL SIDEBAR
        col1, col2, col3 = st.columns(3)
        col1.metric("Membresías Básicas","65","+ 5")
        col2.metric("Membresías Black","35","+ 3")
        col3.metric("Membresías Platino","0","0")

        
        st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Inputs de planeación financiera</h1>", unsafe_allow_html=True)
        st.write(" --- ")

        # MESES A PROYECTAR Y SOLICITUD DE VALORES
        columna1, columna2 = st.columns((2,3))
        columna1.write("<h1 style='text-align: center; font-size: 1.2rem;'>Meses a proyectar:</h1>", unsafe_allow_html=True)
        meses = columna2.radio(" ",(3, 6, 9, 12), horizontal=True)
       
        # ba = Membresía básica, bl = Membresía black, pl = Membresía platino
        # m1 = Mes 1, m2 = Mes 2, m3 = Mes 3
        if meses == 3:

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
            ba_m1 = colum2.number_input(label = "a", label_visibility = "hidden", value = 70, min_value = 0, max_value = 10000, step = 1, key = "ba_m1")
            bl_m1 = colum3.number_input(label = "a", label_visibility = "hidden", value = 40, min_value = 0, max_value = 10000, step = 1, key = "bl_m1")
            pl_m1 = colum4.number_input(label = "a", label_visibility = "hidden", value = 5, min_value = 0, max_value = 10000, step = 1, key = "pl_m1")
            colum1.markdown("")
            # Mes 2
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 2</h1>", unsafe_allow_html=True)
            ba_m2 = colum2.number_input(label = "a", label_visibility = "hidden", value = 74, min_value = 0, max_value = 10000, step = 1, key = "ba_m2")
            bl_m2 = colum3.number_input(label = "a", label_visibility = "hidden", value = 41, min_value = 0, max_value = 10000, step = 1, key = "bl_m2")
            pl_m2 = colum4.number_input(label = "a", label_visibility = "hidden", value = 8, min_value = 0, max_value = 10000, step = 1, key = "pl_m2")
            colum1.markdown("")
            # Mes 3
            colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 3</h1>", unsafe_allow_html=True)
            ba_m3 = colum2.number_input(label = "a", label_visibility = "hidden", value = 80, min_value = 0, max_value = 10000, step = 1, key = "ba_m3")
            bl_m3 = colum3.number_input(label = "a", label_visibility = "hidden", value = 50, min_value = 0, max_value = 10000, step = 1, key = "bl_m3")
            pl_m3 = colum4.number_input(label = "a", label_visibility = "hidden", value = 10, min_value = 0, max_value = 10000, step = 1, key = "pl_m3")
            colum1.markdown("")

            m1 = [ba_m1, ba_m2, ba_m3]
            m2 = [bl_m1, bl_m2, bl_m3]
            m3 = [pl_m1, pl_m2, pl_m3]
            df_membresias = pd.DataFrame(list(zip(m1, m2, m3)), columns = ['Básica','Black','Platino'])
            st.write(df_membresias)
            st.write(" --- ")

            # TASA DE INTERÉS (INFLACIÓN E IMPUESTOS)
            columna1, columna2 = st.columns((2,3))
            columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Tasas de interés</h1>", unsafe_allow_html=True)
            
            colum1, colum2= st.columns((1,3))
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de inflación</h1>", unsafe_allow_html=True)
            tasa_inflacion = colum2.slider(label = "a", label_visibility = "hidden", value = 6.85, min_value = 0.0, max_value = 100.0, step = 1.0, key = "tasa_inflacion")
            colum1.markdown(" ")
            colum1.markdown(" ")
            colum1.markdown(" ")
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Tasa de impuestos</h1>", unsafe_allow_html=True)
            tasa_impuestos = colum2.slider(label = "a", label_visibility = "hidden", value = 30.0, min_value = 0.0, max_value = 100.0, step = 1.0, key = "tasa_impuestos")
            st.write(" --- ")

            # PRECIOS DE MEMBRESÍAS
            columna1, columna2 = st.columns((2,3))
            columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Precios</h1>", unsafe_allow_html=True)
            colum1, colum2, colum3, colum4 = st.columns((1,1,1,1))
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Precios por membresía</h1>", unsafe_allow_html=True)
            ba_precio = colum2.number_input(label = "Membresía básica: ", label_visibility = "visible", value = 199.87, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "ba_precio")
            bl_precio = colum3.number_input(label = "Membresía black: ", label_visibility = "visible", value = 304.70, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "bl_precio")
            pl_precio = colum4.number_input(label = "Membresía platino: ", label_visibility = "visible", value = 487.15, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "pl_precio")
            
            df_precios = pd.DataFrame()                
            df_precios["Básica"] = [ba_precio]
            df_precios["Black"] = [bl_precio] 
            df_precios["Platino"] = [pl_precio]

            # INGRESOS MENSUALES EN EL ESCENARIO MÁS PROBABLE

            ba_ingresos = df_membresias["Básica"]*ba_precio
            bl_ingresos = df_membresias["Black"]*bl_precio
            pl_ingresos = df_membresias["Platino"]*pl_precio
            df_ingresos = pd.DataFrame(list(zip(ba_ingresos, bl_ingresos, pl_ingresos)), columns = ['Básica','Black','Platino'])
            st.write(df_ingresos)
            st.write(" --- ")
            
            # PORCENTAJES DE COMISIONES
            columna1, columna2 = st.columns((2,3))
            columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Porcentajes de comisiones:</h1>", unsafe_allow_html=True)
            
            colum1, colum2, colum3, colum4 = st.columns((1,1,1,1))
            
            colum1.markdown("")
            colum1.markdown("")
            colum1.markdown("")
            
            # COMISIÓN DEL VENDEDOR
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Comisión del vendedor:</h1>", unsafe_allow_html=True)
            ba_com_ven = colum2.number_input(label = "a", label_visibility = "hidden", value = 13.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "ba_com_ven")
            bl_com_ven = colum3.number_input(label = "a", label_visibility = "hidden", value = 15.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "bl_com_vem")
            pl_com_ven = colum4.number_input(label = "a", label_visibility = "hidden", value = 15.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "pl_com_ven")
            colum1.markdown("")
            # COMISIÓN DE REFERENCIA
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Comisión de referencia</h1>", unsafe_allow_html=True)
            ba_com_ref = colum2.number_input(label = "a", label_visibility = "hidden", value = 3.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "ba_com_ref")
            bl_com_ref = colum3.number_input(label = "a", label_visibility = "hidden", value = 5.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "bl_com_ref")
            pl_com_ref = colum4.number_input(label = "a", label_visibility = "hidden", value = 5.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "pl_com_ref")
            colum1.markdown("")
            # COMISIÓN FINANCIERA
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Comisión financiera</h1>", unsafe_allow_html=True)
            ba_com_fin = colum2.number_input(label = "a", label_visibility = "hidden", value = 15.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "ba_com_fin")
            bl_com_fin = colum3.number_input(label = "a", label_visibility = "hidden", value = 15.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "bl_com_fin")
            pl_com_fin = colum4.number_input(label = "a", label_visibility = "hidden", value = 15.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "pl_com_fin")
            colum1.markdown("")
            # COMISIÓN DE MARKETING
            colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Comisión de marketing</h1>", unsafe_allow_html=True)
            ba_com_mkt = colum2.number_input(label = "a", label_visibility = "hidden", value = 1.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "ba_com_mkt")
            bl_com_mkt = colum3.number_input(label = "a", label_visibility = "hidden", value = 3.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "bl_com_mkt")
            pl_com_mkt = colum4.number_input(label = "a", label_visibility = "hidden", value = 5.0, min_value = 0.0, max_value = 100.0, step = 0.1, key = "pl_com_mkt")
            colum1.markdown("")

            l1_1 = [ba_com_ven, ba_com_ref, ba_com_fin, ba_com_mkt]
            l2_1 = [bl_com_ven, bl_com_ref, bl_com_fin, bl_com_mkt]
            l3_1 = [pl_com_ven, pl_com_ref, pl_com_fin, pl_com_mkt]
            df_porc_comisiones = pd.DataFrame(list(zip(l1_1, l2_1, l3_1)), columns = ['Básica','Black','Platino'])

            l1_2 = list(map(lambda x: x*ba_precio/100, l1_1))
            l2_2 = list(map(lambda x: x*bl_precio/100, l2_1))
            l3_2 = list(map(lambda x: x*pl_precio/100, l3_1))
            
            df_comisiones = pd.DataFrame(list(zip(l1_2, l2_2, l3_2)), columns = ['Básica','Black','Platino'])
            df_comisiones_totales = pd.DataFrame()                
            df_comisiones_totales["Básica"] = [df_comisiones["Básica"].sum()]
            df_comisiones_totales["Black"] = [df_comisiones["Black"].sum()] 
            df_comisiones_totales["Platino"] = [df_comisiones["Platino"].sum()]
            st.write(df_comisiones_totales)
            
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
            
            if tipo_analisis == "Costos fijos totales por membresía":
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Costos fijos totales por membresía</h1>", unsafe_allow_html=True)
                ba_costos_fijos_totales = colum2.number_input(label = "Membresía básica: ", label_visibility = "visible", value = 106.0, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "ba_costos_fijos_totales")
                bl_costos_fijos_totales = colum3.number_input(label = "Membresía black: ", label_visibility = "visible", value = 109.0, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "bl_costos_fijos_totales")
                pl_costos_fijos_totales = colum4.number_input(label = "Membresía platino: ", label_visibility = "visible", value = 167.25, min_value = 0.0, max_value = 1000.0, step = 1.0, key = "pl_costos_fijos_totales")
                
                l1 = [ba_costos_fijos_totales]
                l2 = [bl_costos_fijos_totales]
                l3 = [pl_costos_fijos_totales]
                df_costos_fijos_totales = pd.DataFrame(list(zip(l1, l2, l3)), columns = ['Básica','Black','Platino'])
                
                st.write(" --- ")

            elif tipo_analisis == "Desglose de costos fijos por membresía":

                columna2.markdown(" ")
                columna2.markdown(" ")
                columna2.markdown(" ")


                # Call center / oficinas
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Call center / oficinas:</h1>", unsafe_allow_html=True)
                ba_costo_1 = colum2.number_input(label = "a", label_visibility = "hidden", value = 18.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_1")
                bl_costo_1 = colum3.number_input(label = "a", label_visibility = "hidden", value = 21.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_1")
                pl_costo_1 = colum4.number_input(label = "a", label_visibility = "hidden", value = 25.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_1")
                colum1.markdown(" ")
                colum1.markdown(" ")
                
                # Medicina general
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Medicina general:</h1>", unsafe_allow_html=True)
                ba_costo_2 = colum2.number_input(label = "a", label_visibility = "hidden", value = 25.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_2")
                bl_costo_2 = colum3.number_input(label = "a", label_visibility = "hidden", value = 25.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_2")
                pl_costo_2 = colum4.number_input(label = "a", label_visibility = "hidden", value = 25.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_2")
                colum1.markdown(" ")
                colum1.markdown(" ")
                
                # Nutrición
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Nutrición:</h1>", unsafe_allow_html=True)
                ba_costo_3 = colum2.number_input(label = "a", label_visibility = "hidden", value = 18.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_3")
                bl_costo_3 = colum3.number_input(label = "a", label_visibility = "hidden", value = 18.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_3")
                pl_costo_3 = colum4.number_input(label = "a", label_visibility = "hidden", value = 18.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_3")
                colum1.markdown(" ")
                colum1.markdown(" ")

                # Psicología
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Psicología:</h1>", unsafe_allow_html=True)
                ba_costo_4 = colum2.number_input(label = "a", label_visibility = "hidden", value = 22.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_4")
                bl_costo_4 = colum3.number_input(label = "a", label_visibility = "hidden", value = 22.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_4")
                pl_costo_4 = colum4.number_input(label = "a", label_visibility = "hidden", value = 22.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_4")
                colum1.markdown(" ")
                colum1.markdown(" ")

                # Asistencias y seguros básicos
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Asistencias y seguros básicos:</h1>", unsafe_allow_html=True)
                ba_costo_5 = colum2.number_input(label = "a", label_visibility = "hidden", value = 15.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_5")
                bl_costo_5 = colum3.number_input(label = "a", label_visibility = "hidden", value = 15.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_5")
                pl_costo_5 = colum4.number_input(label = "a", label_visibility = "hidden", value = 15.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_5")
                colum1.markdown(" ")
                colum1.markdown(" ")

                # Plataforma de descuentos + Wellness
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Plataforma de descuentos + Wellness:</h1>", unsafe_allow_html=True)
                ba_costo_6 = colum2.number_input(label = "a", label_visibility = "hidden", value = 8.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_6")
                bl_costo_6 = colum3.number_input(label = "a", label_visibility = "hidden", value = 8.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_6")
                pl_costo_6 = colum4.number_input(label = "a", label_visibility = "hidden", value = 8.0, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_6")
                colum1.markdown(" ")
                colum1.markdown(" ")

                # Segunda opinión médica + Farm + Telemedicina
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Segunda opinión médica + Farm + Telemedicina:</h1>", unsafe_allow_html=True)
                ba_costo_7 = colum2.number_input(label = "a", label_visibility = "hidden", value = 0.0, disabled = True, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_7")
                bl_costo_7 = colum3.number_input(label = "a", label_visibility = "hidden", value = 0.0, disabled = True, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_7")
                pl_costo_7 = colum4.number_input(label = "a", label_visibility = "hidden", value = 39.0, disabled = False, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_7")
                colum1.markdown(" ")

                # Doce meses de sueldo por muerte accidental
                colum1.markdown("<h1 style='text-align: right; font-size: 1.2rem;'>Asistencias y seguros básicos:</h1>", unsafe_allow_html=True)
                ba_costo_8 = colum2.number_input(label = "a", label_visibility = "hidden", value = 0.0, disabled = True, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "ba_costo_8")
                bl_costo_8 = colum3.number_input(label = "a", label_visibility = "hidden", value = 0.0, disabled = True, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "bl_costo_8")
                pl_costo_8 = colum4.number_input(label = "a", label_visibility = "hidden", value = 15.25, disabled = False, min_value = 0.0, max_value = 10000.0, step = 1.0, key = "pl_costo_8")
                colum1.markdown(" ")


                l1 = [ba_costo_1, ba_costo_2, ba_costo_3, ba_costo_4, ba_costo_5, ba_costo_6, ba_costo_7, ba_costo_8]
                l2 = [bl_costo_1, bl_costo_2, bl_costo_3, bl_costo_4, bl_costo_5, bl_costo_6, bl_costo_7, bl_costo_8]
                l3 = [pl_costo_1, pl_costo_2, pl_costo_3, pl_costo_4, pl_costo_5, pl_costo_6, pl_costo_7, pl_costo_8]
                df_costos_fijos = pd.DataFrame(list(zip(l1, l2, l3)), columns = ['Básica','Black','Platino'])
                
                df_costos_fijos_totales = pd.DataFrame()                
                df_costos_fijos_totales["Básica"] = [df_costos_fijos["Básica"].sum()]
                df_costos_fijos_totales["Black"] = [df_costos_fijos["Black"].sum()] 
                df_costos_fijos_totales["Platino"] = [df_costos_fijos["Platino"].sum()]

            # Utilidades antes de impuestos
            uadi_por_membresia = utilidad_antes_de_impuestos(df_precios, df_comisiones_totales, df_costos_fijos_totales)

            ba_uadi = uadi_por_membresia["Básica"][0]*df_membresias["Básica"]
            bl_uadi = uadi_por_membresia["Black"][0]*df_membresias["Black"]
            pl_uadi = uadi_por_membresia["Platino"][0]*df_membresias["Platino"]
            df_uadi = pd.DataFrame(list(zip(ba_uadi, bl_uadi, pl_uadi)), columns = ['Básica','Black','Platino'])
            df_uadi_mes = df_uadi.sum(axis = 1)
            df_uadi_mes.rename(index={0:'Mes 1',1:'Mes 2',2:'Mes 3'}, inplace=True)
            #columna1, columna2 = st.columns((2,3))
            #columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Utilidades antes de impuestos:</h1>", unsafe_allow_html=True)
            #columna2.write(df_uadi_mes)
            #st.write(" --- ")

            # Utilidades netas

            ba_un = df_uadi["Básica"]*(1-(tasa_impuestos/100))
            bl_un = df_uadi["Black"]*(1-(tasa_impuestos/100))
            pl_un = df_uadi["Platino"]*(1-(tasa_impuestos/100))
            df_un = pd.DataFrame(list(zip(ba_un, bl_un, pl_un)), columns = ['Básica','Black','Platino'])
            df_un_mes = df_un.sum(axis = 1)
            
            df_un_mes.rename(index={0:'Mes 1',1:'Mes 2',2:'Mes 3'}, inplace=True)
            #df_un_mes.rename(columns = {0:'Utilidades netas'}, inplace = True)

            #columna1, columna2 = st.columns((2,3))
            #columna1.write("<h1 style='text-align: center; font-size: 1.5rem;'>Utilidades netas:</h1>", unsafe_allow_html=True)
            #columna2.write(df_un_mes)
            #st.write(" --- ")

        elif meses == 6:
            st.write()
        elif meses == 9:
            st.write()
        else:
            st.write() 

    #-----------------------------------------------------------------------------------------------------------------------------#
    
    elif ("Básica" in membresias) & ("Black" in membresias):
    
    # CONFIGURACIÓN DE LA PÁGINA Y EL SIDEBAR
        col1, col2 = st.columns(2)
        col1.metric("Membresías Básicas","65","+ 5")
        col2.metric("Membresías Black","35","+ 3")

        
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

        elif meses == 6:
            st.write()
        elif meses == 9:
            st.write()
        else:
            st.write()    


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
    porc_comisiones = pd.read_excel("BD_DocTour.xlsx", sheet_name="1_Comisiones", index_col=0)
    costos_fijos = pd.read_excel("BD_DocTour.xlsx", sheet_name="1_CostosFijos", index_col=0)
    precios = pd.read_excel("BD_DocTour.xlsx", sheet_name="1_Precios", index_col=0)
    membresias_proyectadas = pd.read_excel("BD_DocTour.xlsx", sheet_name="1_MembresíasProyectadas", index_col=0)

    #------ ESCENARIO MÁS PROBABLE ---------#
    st.write("<h1 style='text-align: center; font-size: 1.6rem;'>Número de membresías proyectadas</h1>", unsafe_allow_html=True)
        #st.write(df_un)
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
    #st.write(df_costos_fijos_1["Básica"][0])

    # COSTOS FIJOS TOTALES EN EL ESCENARIO MÁS PROBABLE
    ba_costos_totales_1 = membresias_proyectadas["Básica"]*df_costos_fijos_1["Básica"][0]
    bl_costos_totales_1 = membresias_proyectadas["Black"]*df_costos_fijos_1["Black"][0]
    pl_costos_totales_1 = membresias_proyectadas["Platino"]*df_costos_fijos_1["Platino"][0]
    df_costos_totales_1 = pd.DataFrame(list(zip(ba_costos_totales_1, bl_costos_totales_1, pl_costos_totales_1)), columns = ['Básica','Black','Platino'])
    #st.write(" COSTOS TOTALES ")
    #st.write(df_costos_totales_1)
    #st.write(" --- ")

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
