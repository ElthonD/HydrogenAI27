import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

### App de Inicio

def createPage():
    
    # Title of the main page
    pathLogo = './img/Logo_Hydrogen.png'
    display = Image.open(pathLogo)
    display = np.array(display)
    # st.image(display, width = 400)
    # st.title("Aplicación DataDriven")
    col1, col2, col3 = st.columns([1,5,1])
    col2.image(display, use_column_width=True)
    #col2.title("Aplicación DataDriven")

    col2.markdown('Bienvenido a ***Hydrogen AI27***, está aplicación provee Indicadores de Seguimiento a la Operación de Pago por Evento)')

    col2.write(""" 
    Está aplicación contiene:
    + ***Indicadores Pago por Evento.***
    + ***Métricas Pago por Evento.***
    """)

    return True
