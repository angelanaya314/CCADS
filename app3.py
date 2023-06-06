# IMPORTACION DE LAS LIBRERIAS
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from datetime import datetime

#------------------------------------------------------------------------------------------------#
# IMPORTACIÓN DE LA BASE DE DATOS
df = pd.read_excel("BD_DocTour.xlsx")

#------------------------------------------------------------------------------------------------#
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
#This code helps to hide the main menu of Streamlit
hide_st_style = """
			<style>
			#MainMenu {visibility: hidden;}
			footer {visibility: hidden;}
			header {visibility: hidden;}
			</style>
			"""
st.markdown(hide_st_style, unsafe_allow_html=True)

#------------------------------------------------------------------------------------------------#
#------- Navigation Menu ----------
option_selected = option_menu(
	menu_title=None,
	options=["Finanzas y escenarios", "Programación lineal", "Dashboard"],
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
#------- Campañas e iniciativas ----------
if option_selected == "Finanzas y escenarios":

    st.markdown("")
    cli1, cli2 = st.columns((2,6))

    cli1.markdown("")
    cli1.markdown("<h1 style='text-align: center; color: black; font-size: 1.2rem;'>Membresías a mostrar:</h1>", unsafe_allow_html=True)
    
    membresias = cli2.multiselect("",["Básica","Black","Platino"], default=["Básica","Black","Platino"])

    col1, col2, col3, col4, col5 = st.columns((3,2,2,2,1))

    if ("Básica" in membresias):
        col2.metric("Básicas", "65", "+ 5")

    if ("Black" in membresias):
        col3.metric("Black", "35", "- 2")

    if ("Platino" in membresias):
        col4.metric("Platino", "0", "0")

    #colu1, colu2, colu3, colu4, colu5 = st.columns((2,1,1,1,1))

    #colu1.markdown("")
    #colu1.markdown("<h1 style='text-align: center; color: black; font-size: 1.2rem;'>Meses a proyectar:</h1>", unsafe_allow_html=True)
    
    #colu2.markdown("")
    #colu2.markdown("")
    #tres = colu2.radio("3")
    #colu3.markdown("")
    #colu3.markdown("")
    #seis = colu3.checkbox("6")
    #colu4.markdown("")
    #colu4.markdown("")
    #nueve = colu4.checkbox("9")
    #colu5.markdown("")
    #colu5.markdown("")
    #doce = colu5.checkbox("12")

    colu1, colu2, colu3, colu4 = st.columns((2,2,2,2))

    colu2.markdown("")
    colu2.markdown("")
    colu2.markdown("<h1 style='text-align: center; color: black; font-size: 1.2rem;'>Meses a proyectar:</h1>", unsafe_allow_html=True)
    
    colu3.markdown("")
    meses = colu3.radio("", (3,6,9,12), horizontal=True)


    colum1, colum2, colum3, colum4, colum5 = st.columns((2,1,1,1,1))

    if meses == 3:
        #colum1.markdown("<h1 style='text-align: center; color: black; font-size: 1.2rem;'></h1>", unsafe_allow_html=True)
        colum1.markdown("")
        colum1.markdown("<h1 style='text-align: center; font-size: 1.2rem;'></h1>", unsafe_allow_html=True)
        colum2.markdown("")
        colum2.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Básica</h1>", unsafe_allow_html=True)
        colum3.markdown("")
        colum3.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Black</h1>", unsafe_allow_html=True)
        colum4.markdown("")
        colum4.markdown("<h1 style='text-align: center; font-size: 1.2rem;'>Platino</h1>", unsafe_allow_html=True)

        colum1.markdown("")
        colum1.markdown("")
        colum1.markdown("")
        # Mes 1
        colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 1</h1>", unsafe_allow_html=True)
        Basica_Mes1 = colum2.number_input("", min_value=0, max_value=10000, step=1)
        Black_Mes1 = colum3.number_input("", min_value=0, max_value=10000, step=1)
        Platino_Mes1 = colum4.number_input("", min_value=0, max_value=10000, step=1)
        colum1.markdown("")
        # Mes 2
        colum1.markdown("<h1 style='text-align: right; font-size: 1.5rem;'>Mes 2</h1>", unsafe_allow_html=True)
        Basica_Mes2 = colum2.number_input("", min_value=0, max_value=10000, step=1)
        Black_Mes2 = colum3.number_input("", min_value=0, max_value=10000, step=1)
        Platino_Mes2 = colum4.number_input("", min_value=0, max_value=10000, step=1)
        colum1.markdown("")
        # Mes 3
        colum1.markdown("<h1 style='text-align: right; color: black; font-size: 1.5rem;'>Mes 3</h1>", unsafe_allow_html=True)
        Basica_Mes3 = colum2.number_input("", min_value = 0, max_value = 10000, step = 1)
        Black_Mes3 = colum3.number_input("", min_value = 0, max_value = 10000, step = 1)
        Platino_Mes3 = colum4.number_input("", min_value = 0, max_value = 10000, step = 1)
