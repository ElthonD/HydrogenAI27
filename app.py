import streamlit as st
from streamlit_option_menu import option_menu
import inicio, indicadores, metricas # Importar páginas acá
 #### Páginas

st.set_page_config(page_title="Hydrogen AI27", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

v_menu=["Inicio", "Indicadores", "Métricas"]

selected = option_menu(
    menu_title=None,  # required
    options=["Inicio", "Indicadores", "Métricas"],  # required 
    icons=["house", "stoplights", "speedometer"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
    styles={
        "container": {"padding": "10px", "background-color": "#fafafa"},
        "icon": {"font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "salmon"},
        "nav-link-selected": {"background-color": "tomato"},
    }
    )

if selected=="Inicio":
    inicio.createPage()

if selected=="Indicadores":
    indicadores.createPage()

if selected=="Métricas":
    metricas.createPage()