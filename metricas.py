### Librerías
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
from random import sample
from dateutil.relativedelta import *
import plotly.graph_objects as go
from PIL import Image
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.UTF8')

### App de Servicios Activos

def createPage():

    @st.cache_data(show_spinner='Cargando Datos... Espere...', persist=True)
    def load_ppe():
    
        rutaPPE = './data/Data Hydrogen.xlsx'
        PPE = pd.read_excel(rutaPPE, sheet_name = "Data")
        PPE["Cliente"] = PPE["Cliente"].astype(str)
        PPE["Base Cliente"] = PPE["Base Cliente"].astype(str)
        PPELFL = PPE.loc[PPE.loc[:, 'Tipo Monitoreo'] == 'INTELIGENTE LFL']
        PPEINT = PPE.loc[PPE.loc[:, 'Tipo Monitoreo'] == 'INTELIGENTE']
        PPEACT = PPE.loc[PPE.loc[:, 'Tipo Monitoreo'] == 'ACTIVO']
        PPEIC = PPE.loc[PPE.loc[:, 'Tipo Monitoreo'] == 'INTELIGENTE CON CUSTODIA']
        PPEWS = PPE.loc[PPE.loc[:, 'Tipo Monitoreo'] == 'WEB SERVICE']
        PPES = PPE.loc[PPE.loc[:, 'Tipo Monitoreo'] == 'SIMPLIFICADO']
    
        PPE1 = pd.concat([PPELFL, PPEINT, PPEIC, PPEACT, PPEWS, PPES])
    
        return PPE1
    
    def df_grafico_bases(df):
    
        df['Fecha Inicio'] = pd.to_datetime(df['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

        # Para Servicios Totales
        pSer = df.copy() #dataframe filtrado por tipo de servicio foraneo o local
        pSer['Fecha Inicio'] = pd.to_datetime(pSer['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        pSer.drop(['Número de Folio','Cliente','Plantilla Promedio','Orden de Servicio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje', 'Duración', 'Ingresos', 'Tiene OS Finanzas'], axis = 'columns', inplace=True)    
        pSer = pSer.set_index('Fecha Inicio')
        pSer1 = pd.DataFrame(pSer['Bitácora'].resample('M').count())
        pSer1 = pSer1[['Bitácora']]
    
        # Para Servicios por Patrullas
        pSer2 = df.copy()
        pSer2.drop(['Número de Folio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer2['ID'] = pSer2['Orden de Servicio'].str.cat(pSer2['Cliente'])
        pSer2 = pSer2.drop_duplicates(subset = "ID")
        pSer2['Fecha Inicio'] = pd.to_datetime(pSer2['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        pSer2 = pSer2.set_index('Fecha Inicio')
        pSer3 = pd.DataFrame(pSer2['Orden de Servicio'].resample('M').count())
        pSer3 = pSer3[['Orden de Servicio']]
    
        # Para Total de Horas por Mes
        pSer4 = df.copy()
        pSer4.drop(['Número de Folio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer4['IDu'] = pSer4['Orden de Servicio'].str.cat(pSer4['Cliente'])
        pSer4 = pSer4.drop_duplicates(subset = "IDu")
        pSer4['Duración'] = pSer4['Duración'].astype(int)
        pSer4 = pSer4.set_index('Fecha Inicio')
        pSer5 = pd.DataFrame(pSer4['Duración'].resample('M').sum())
        #pSer = pSer[['Base Cliente','Duración']]
        #pSer5 = pd.DataFrame(pSer4.groupby(['Base Cliente']).resample('M').sum())
        pSer5 = pSer5[['Duración']]
        pSer5 = pSer5['Duración'].astype(int)

        # Para Plantilla Promedio
        pSer6 = df.copy()
        pSer6.drop(['Número de Folio','Orden de Servicio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer6 = pSer6.drop_duplicates(subset = "Codigo Plantilla")
        pSer6['Fecha Inicio'] = pd.to_datetime(pSer6['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        pSer6 = pSer6.set_index('Fecha Inicio')
        pSer6['Plantilla Promedio'] = pSer6['Plantilla Promedio'].astype(float)
        pSer7 = pd.DataFrame(pSer6['Plantilla Promedio'].resample('M').mean())
        pSer7 = pSer7[['Plantilla Promedio']]
        pSer7['Plantilla Promedio'] = pSer7['Plantilla Promedio'].apply(np.ceil)
    
        # Para Descansos Promedio
        pSer8 = df.copy()
        pSer8.drop(['Número de Folio','Orden de Servicio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer8['Mes'] = pSer8['Fecha Inicio'].dt.month_name(locale='Spanish')
        pSer8['Año'] = pSer8['Fecha Inicio'].dt.year
        pSer8["IDD"] = pSer8["Base Cliente"] + " " + pSer8["Mes"].astype(str) + " " + pSer8['Año'].astype(str)
        pSer8 = pSer8.drop_duplicates(subset = "IDD")
        pSer8['Fecha Inicio'] = pd.to_datetime(pSer8['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        pSer8 = pSer8.set_index('Fecha Inicio')
        pSer9 = pd.DataFrame(pSer8['Dias Descanso'].resample('M').mean())
        pSer9 = pSer9[['Dias Descanso']]
    
        # Para Ingresos
        pSer10 = df.copy()
        pSer10 = pSer10.loc[pSer10.loc[:, 'Tiene OS Finanzas'] == 'SI']
        pSer10.drop(['Número de Folio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer10['ID1'] = pSer10['Orden de Servicio'].str.cat(pSer10['Cliente'])
        pSer10 = pSer10.drop_duplicates(subset = "ID1")
        pSer10['Ingresos'] = pSer10['Ingresos'].astype(float)
        pSer10 = pSer10.set_index('Fecha Inicio')
        #pSer = pSer[['Base Cliente','Duración']]
        pSer11 = pd.DataFrame(pSer10['Ingresos'].resample('M').sum())
        pSer11 = pSer11[['Ingresos']]
        
        # Para Tipo de Servicios Foraneos
        pSer12 = df.copy()
        pSer12.drop(['Número de Folio','Tipo Monitoreo', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer12['ID2'] = pSer12['Orden de Servicio'].str.cat(pSer12['Cliente'])
        pSer12 = pSer12.drop_duplicates(subset = "ID2")
        pSer12['Tipo Servicio'] = pSer12['Tipo Servicio'].astype(str)
        pSer12 = pSer12.loc[pSer12.loc[:, 'Tipo Servicio'] == 'FORANEO']
        pSer12 = pSer12.set_index('Fecha Inicio')
        #pSer = pSer[['Base Cliente','Duración']]
        pSer13 = pd.DataFrame(pSer12['Tipo Servicio'].resample('M').count())
        pSer13 = pSer13.rename(columns={'Tipo Servicio':'Foraneos'})
    
        # Para Tipo de Servicios Locales
    
        pSer14 = df.copy()
        pSer14.drop(['Número de Folio','Tipo Monitoreo', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer14['ID2'] = pSer14['Orden de Servicio'].str.cat(pSer14['Cliente'])
        pSer14 = pSer14.drop_duplicates(subset = "ID2")
        pSer14['Tipo Servicio'] = pSer14['Tipo Servicio'].astype(str)
        pSer14 = pSer14.loc[pSer14.loc[:, 'Tipo Servicio'] == 'LOCAL']
        pSer14 = pSer14.set_index('Fecha Inicio')
        #pSer = pSer[['Base Cliente','Duración']]
        pSer15 = pd.DataFrame(pSer14['Tipo Servicio'].resample('M').count())
        pSer15 = pSer15.rename(columns={'Tipo Servicio':'Locales'})
    
        # Para Tipo de Servicios Repartos
    
        pSer16 = df.copy()
        pSer16.drop(['Número de Folio','Tipo Monitoreo', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer16['ID2'] = pSer16['Orden de Servicio'].str.cat(pSer16['Cliente'])
        pSer16 = pSer16.drop_duplicates(subset = "ID2")
        pSer16['Tipo Servicio'] = pSer16['Tipo Servicio'].astype(str)
        pSer16 = pSer16.loc[pSer16.loc[:, 'Tipo Servicio'] == 'REPARTOS']
        pSer16 = pSer16.set_index('Fecha Inicio')
        pSer17 = pd.DataFrame(pSer16['Tipo Servicio'].resample('M').count())
        pSer17 = pSer17.rename(columns={'Tipo Servicio':'Repartos'})
          
        # Unir dataframe
        pSer18 = pd.concat([pSer1, pSer3, pSer5, pSer7, pSer9, pSer11, pSer13, pSer15, pSer17], axis=1)
        # Reset Indíces
        pSer18 = pSer18.reset_index()
    
        # Preparar Dataframe Final
        pSer18['Mes'] = pSer18['Fecha Inicio'].dt.month_name(locale='Spanish')
        pSer18['Año'] = pSer18['Fecha Inicio'].dt.year
        pSer18['Días de Trabajo'] = pSer18['Fecha Inicio'].dt.daysinmonth
        pSer18 = pSer18[['Fecha Inicio','Duración', 'Bitácora','Orden de Servicio','Plantilla Promedio','Dias Descanso','Ingresos','Mes','Año','Días de Trabajo', 'Foraneos', 'Locales', 'Repartos']]
        pSer18.columns = ['Fecha', 'Horas Totales','Servicios Reales','Servicios Realizados','Plantilla Promedio','Dias Descanso','Ingresos','Mes','Año','Días de Trabajo', 'Servicios Foráneos', 'Servicios Locales', 'Servicios Repartos']
        pSer18['Relación Reales/Realizados'] = np.ceil(pSer18['Servicios Reales'] / pSer18['Servicios Realizados'])
        pSer18['Servicios Per Cápita'] = np.ceil(pSer18['Servicios Realizados'] / pSer18['Plantilla Promedio'])
        pSer18['Horas Per Cápita'] = np.ceil(pSer18['Horas Totales'] / pSer18['Plantilla Promedio'])
        pSer18['Horas Teóricas'] = ((pSer18['Días de Trabajo'] - pSer18['Dias Descanso']) * 24)
        pSer18['Productividad(%)'] = (pSer18['Horas Totales'] / (pSer18['Horas Teóricas'] * pSer18['Plantilla Promedio'])) * 100
        pSer18['Ingresos Per Cápita'] = np.ceil(pSer18['Ingresos'] / pSer18['Plantilla Promedio'])
        pSer18['Duración Promedio (Hrs)'] = np.ceil(pSer18['Horas Totales'] / pSer18['Servicios Realizados'])
        pSer18 = pSer18.replace([np.inf, -np.inf], 0)  
        pSer18 = pSer18.fillna(0)
        pSer18['Relación Reales/Realizados'] = pSer18['Relación Reales/Realizados'].astype(int)
        pSer18['Servicios Per Cápita'] = pSer18['Servicios Per Cápita'].astype(int)
        pSer18['Horas Per Cápita'] = pSer18['Horas Per Cápita'].astype(int)
        pSer18['Servicios Locales'] = pSer18['Servicios Locales'].astype(int)
        pSer18['Servicios Foráneos'] = pSer18['Servicios Foráneos'].astype(int)
        pSer18['Servicios Repartos'] = pSer18['Servicios Repartos'].astype(int)
        pSer18 = pSer18.astype({"Servicios Reales":"int","Servicios Realizados":"int","Relación Reales/Realizados":"int","Días de Trabajo":"int","Horas Totales":"int","Servicios Per Cápita":"int","Horas Per Cápita":"int"})
        pSer18 = pSer18.iloc[0:16]
    
        return pSer18
    
    def df_grafico_clientes(df):
    
        df['Fecha Inicio'] = pd.to_datetime(df['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

        # Para Servicios Totales
        pSer = df.copy() #dataframe filtrado por tipo de servicio foraneo o local
        pSer['Fecha Inicio'] = pd.to_datetime(pSer['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        pSer.drop(['Número de Folio','Cliente','Plantilla Promedio','Orden de Servicio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje', 'Duración', 'Ingresos', 'Tiene OS Finanzas'], axis = 'columns', inplace=True)    
        pSer = pSer.set_index('Fecha Inicio')
        pSer1 = pd.DataFrame(pSer['Bitácora'].resample('M').count())
        pSer1 = pSer1[['Bitácora']]
    
        # Para Servicios por Patrullas
        pSer2 = df.copy()
        pSer2.drop(['Número de Folio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer2['ID'] = pSer2['Orden de Servicio'].str.cat(pSer2['Cliente'])
        pSer2 = pSer2.drop_duplicates(subset = "ID")
        pSer2['Fecha Inicio'] = pd.to_datetime(pSer2['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        pSer2 = pSer2.set_index('Fecha Inicio')
        pSer3 = pd.DataFrame(pSer2['Orden de Servicio'].resample('M').count())
        pSer3 = pSer3[['Orden de Servicio']]
    
        # Para Total de Horas por Mes
        pSer4 = df.copy()
        pSer4.drop(['Número de Folio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer4['IDu'] = pSer4['Orden de Servicio'].str.cat(pSer4['Cliente'])
        pSer4 = pSer4.drop_duplicates(subset = "IDu")
        pSer4['Duración'] = pSer4['Duración'].astype(int)
        pSer4 = pSer4.set_index('Fecha Inicio')
        pSer5 = pd.DataFrame(pSer4['Duración'].resample('M').sum())
        #pSer = pSer[['Base Cliente','Duración']]
        #pSer5 = pd.DataFrame(pSer4.groupby(['Base Cliente']).resample('M').sum())
        pSer5 = pSer5[['Duración']]
        pSer5 = pSer5['Duración'].astype(int)
    
        # Para Ingresos
        pSer10 = df.copy()
        pSer10 = pSer10.loc[pSer10.loc[:, 'Tiene OS Finanzas'] == 'SI']
        pSer10.drop(['Número de Folio','Tipo Monitoreo', 'Tipo Servicio', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer10['ID1'] = pSer10['Orden de Servicio'].str.cat(pSer10['Cliente'])
        pSer10 = pSer10.drop_duplicates(subset = "ID1")
        pSer10['Ingresos'] = pSer10['Ingresos'].astype(float)
        pSer10 = pSer10.set_index('Fecha Inicio')
        #pSer = pSer[['Base Cliente','Duración']]
        pSer11 = pd.DataFrame(pSer10['Ingresos'].resample('M').sum())
        pSer11 = pSer11[['Ingresos']]
        
        # Para Tipo de Servicios Foraneos
        pSer12 = df.copy()
        pSer12.drop(['Número de Folio','Tipo Monitoreo', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer12['ID2'] = pSer12['Orden de Servicio'].str.cat(pSer12['Cliente'])
        pSer12 = pSer12.drop_duplicates(subset = "ID2")
        pSer12['Tipo Servicio'] = pSer12['Tipo Servicio'].astype(str)
        pSer12 = pSer12.loc[pSer12.loc[:, 'Tipo Servicio'] == 'FORANEO']
        pSer12 = pSer12.set_index('Fecha Inicio')
        #pSer = pSer[['Base Cliente','Duración']]
        pSer13 = pd.DataFrame(pSer12['Tipo Servicio'].resample('M').count())
        pSer13 = pSer13.rename(columns={'Tipo Servicio':'Foraneos'})
    
        # Para Tipo de Servicios Locales
    
        pSer14 = df.copy()
        pSer14.drop(['Número de Folio','Tipo Monitoreo', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer14['ID2'] = pSer14['Orden de Servicio'].str.cat(pSer14['Cliente'])
        pSer14 = pSer14.drop_duplicates(subset = "ID2")
        pSer14['Tipo Servicio'] = pSer14['Tipo Servicio'].astype(str)
        pSer14 = pSer14.loc[pSer14.loc[:, 'Tipo Servicio'] == 'LOCAL']
        pSer14 = pSer14.set_index('Fecha Inicio')
        #pSer = pSer[['Base Cliente','Duración']]
        pSer15 = pd.DataFrame(pSer14['Tipo Servicio'].resample('M').count())
        pSer15 = pSer15.rename(columns={'Tipo Servicio':'Locales'})
    
        # Para Tipo de Servicios Repartos
    
        pSer16 = df.copy()
        pSer16.drop(['Número de Folio','Tipo Monitoreo', 'Fecha Finalización', 'Duración Estimada', 'Distancia', 'Origen', 'TU1','EstadoOrigen','RegionOrigen', 'LAO','LOO','Destino','TU2','EstadoDestino','RegionDestino','LAD','LOD','CostoKM','Patrulla','Base Patrulla','Ubicación Patrulla','KM Rodaje','Costo KM Rodaje'], axis = 'columns', inplace=True)    
        pSer16['ID2'] = pSer16['Orden de Servicio'].str.cat(pSer16['Cliente'])
        pSer16 = pSer16.drop_duplicates(subset = "ID2")
        pSer16['Tipo Servicio'] = pSer16['Tipo Servicio'].astype(str)
        pSer16 = pSer16.loc[pSer16.loc[:, 'Tipo Servicio'] == 'REPARTOS']
        pSer16 = pSer16.set_index('Fecha Inicio')
        pSer17 = pd.DataFrame(pSer16['Tipo Servicio'].resample('M').count())
        pSer17 = pSer17.rename(columns={'Tipo Servicio':'Repartos'})
          
        # Unir dataframe
        pSer18 = pd.concat([pSer1, pSer3, pSer5, pSer11, pSer13, pSer15, pSer17], axis=1)
        # Reset Indíces
        pSer18 = pSer18.reset_index()
    
        # Preparar Dataframe Final
        pSer18['Mes'] = pSer18['Fecha Inicio'].dt.month_name(locale='Spanish')
        pSer18['Año'] = pSer18['Fecha Inicio'].dt.year
        pSer18['Días de Trabajo'] = pSer18['Fecha Inicio'].dt.daysinmonth
        pSer18 = pSer18[['Fecha Inicio','Duración', 'Bitácora','Orden de Servicio','Ingresos','Mes','Año','Días de Trabajo', 'Foraneos', 'Locales', 'Repartos']]
        pSer18.columns = ['Fecha', 'Horas Totales','Servicios Reales','Servicios Realizados','Ingresos','Mes','Año','Días de Trabajo', 'Servicios Foráneos', 'Servicios Locales', 'Servicios Repartos']
        pSer18['Relación Reales/Realizados'] = np.ceil(pSer18['Servicios Reales'] / pSer18['Servicios Realizados'])
        pSer18['Duración Promedio (Hrs)'] = np.ceil(pSer18['Horas Totales'] / pSer18['Servicios Realizados'])
        pSer18 = pSer18.replace([np.inf, -np.inf], 0)  
        pSer18 = pSer18.fillna(0)
        pSer18['Relación Reales/Realizados'] = pSer18['Relación Reales/Realizados'].astype(int)
        pSer18['Servicios Locales'] = pSer18['Servicios Locales'].astype(int)
        pSer18['Servicios Foráneos'] = pSer18['Servicios Foráneos'].astype(int)
        pSer18['Servicios Repartos'] = pSer18['Servicios Repartos'].astype(int)
        pSer18 = pSer18.astype({"Servicios Reales":"int","Servicios Realizados":"int","Relación Reales/Realizados":"int","Días de Trabajo":"int","Horas Totales":"int"})
        pSer18 = pSer18.iloc[0:16]
    
        return pSer18

    def df_rango_fechas_bases(df):
                
        df1 = df.copy() #Aca colocar dataframe filtrado
        df2 = df1.dropna()
        df2['Fecha Inicio'] = pd.to_datetime(df2['Fecha Inicio']).dt.date
        df2['Año'] = pd.to_numeric(df2['Año'], downcast="integer") #Esto lo hice para que el texto de años aparezca como entero

        fecha_inicio, fecha_fin = st.date_input('Fecha Inicio - Fecha Fin:',value = [], key="FPPE1")
           
        if fecha_inicio < fecha_fin:
            pass
        else:
            st.error('Error: la Fecha de Finalización debe ser posterior a la Fecha de Inicio.')
            
        mask = (df2['Fecha Inicio'] > fecha_inicio) & (df2['Fecha Inicio'] <= fecha_fin)
        df2 = df2.loc[mask] #Dataframe con Salidas Totales de una fecha inicio a una fecha final

        return df2
    
    def df_rango_fechas_cliente(df):
                
        df1 = df.copy() #Aca colocar dataframe filtrado
        df2 = df1.dropna()
        df2['Fecha Inicio'] = pd.to_datetime(df2['Fecha Inicio']).dt.date
        df2['Año'] = pd.to_numeric(df2['Año'], downcast="integer") #Esto lo hice para que el texto de años aparezca como entero

        fecha_inicio, fecha_fin = st.date_input('Fecha Inicio - Fecha Fin:',value = [], key="FPPE2")
           
        if fecha_inicio < fecha_fin:
            pass
        else:
            st.error('Error: la Fecha de Finalización debe ser posterior a la Fecha de Inicio.')
            
        mask = (df2['Fecha Inicio'] > fecha_inicio) & (df2['Fecha Inicio'] <= fecha_fin)
        df2 = df2.loc[mask] #Dataframe con Salidas Totales de una fecha inicio a una fecha final

        return df2
    
    def tasa_variacion_ppe_bases(df):
        
        df['Mes'] = df['Fecha'].dt.month_name(locale='Spanish')
        df['Año'] = df['Fecha'].dt.year
        df['Tasa Servicios Reales (%)'] = (df['Servicios Reales'].diff()/df['Servicios Reales'].shift())*100
        df['Tasa Servicios Realizados (%)'] = (df['Servicios Realizados'].diff()/df['Servicios Realizados'].shift())*100
        df['Tasa Ingresos (%)'] = (df['Ingresos'].diff()/df['Ingresos'].shift())*100
        df['Tasa Ingresos Per Cápita (%)'] = (df['Ingresos Per Cápita'].diff()/df['Ingresos Per Cápita'].shift())*100
        df['Tasa Servicios Per Cápita (%)'] = (df['Servicios Per Cápita'].diff()/df['Servicios Per Cápita'].shift())*100
        df['Tasa Productividad (%)'] = (df['Productividad(%)'].diff()/df['Productividad(%)'].shift())*100
        df['Tasa Servicios Foráneos (%)'] = (df['Servicios Foráneos'].diff()/df['Servicios Foráneos'].shift())*100
        df['Tasa Servicios Locales (%)'] = (df['Servicios Locales'].diff()/df['Servicios Locales'].shift())*100
        df['Tasa Servicios Repartos (%)'] = (df['Servicios Repartos'].diff()/df['Servicios Repartos'].shift())*100
        df['Tasa Horas per Cápita (%)'] = (df['Horas Per Cápita'].diff()/df['Horas Per Cápita'].shift())*100

        df['Tasa Servicios Reales (%)'] = round(df['Tasa Servicios Reales (%)'],2)
        df['Tasa Servicios Realizados (%)'] = round(df['Tasa Servicios Realizados (%)'],2)
        df['Tasa Ingresos (%)'] = round(df['Tasa Ingresos (%)'],2)
        df['Tasa Ingresos Per Cápita (%)'] = round(df['Tasa Ingresos Per Cápita (%)'],2)
        df['Tasa Servicios Per Cápita (%)'] = round(df['Tasa Servicios Per Cápita (%)'],2)
        df['Tasa Productividad (%)'] = round(df['Tasa Productividad (%)'],2)
        df['Tasa Servicios Foráneos (%)'] = round(df['Tasa Servicios Foráneos (%)'],2)
        df['Tasa Servicios Locales (%)'] = round(df['Tasa Servicios Locales (%)'],2)
        df['Tasa Servicios Repartos (%)'] = round(df['Tasa Servicios Repartos (%)'],2)
        df['Tasa Horas per Cápita (%)'] = round(df['Tasa Horas per Cápita (%)'],2)

        df = df.reindex(columns=['Año','Mes','Servicios Reales','Tasa Servicios Reales (%)','Servicios Realizados','Tasa Servicios Realizados (%)', 'Ingresos', 'Tasa Ingresos (%)', 'Ingresos Per Cápita', 'Tasa Ingresos Per Cápita (%)', 'Servicios Per Cápita', 'Tasa Servicios Per Cápita (%)', 'Productividad(%)', 'Tasa Productividad (%)', 'Servicios Foráneos', 'Tasa Servicios Foráneos (%)', 'Servicios Locales', 'Tasa Servicios Locales (%)', 'Servicios Repartos', 'Tasa Servicios Repartos (%)', 'Horas Per Cápita', 'Tasa Horas per Cápita (%)'])

        return df

    def tasa_variacion_ppe_clientes(df):
        
        df['Mes'] = df['Fecha'].dt.month_name(locale='Spanish')
        df['Año'] = df['Fecha'].dt.year
        df['Tasa Servicios Reales (%)'] = (df['Servicios Reales'].diff()/df['Servicios Reales'].shift())*100
        df['Tasa Servicios Realizados (%)'] = (df['Servicios Realizados'].diff()/df['Servicios Realizados'].shift())*100
        df['Tasa Ingresos (%)'] = (df['Ingresos'].diff()/df['Ingresos'].shift())*100
        df['Tasa Servicios Foráneos (%)'] = (df['Servicios Foráneos'].diff()/df['Servicios Foráneos'].shift())*100
        df['Tasa Servicios Locales (%)'] = (df['Servicios Locales'].diff()/df['Servicios Locales'].shift())*100
        df['Tasa Servicios Repartos (%)'] = (df['Servicios Repartos'].diff()/df['Servicios Repartos'].shift())*100
        df['Tasa Servicios Reales (%)'] = round(df['Tasa Servicios Reales (%)'],2)
        df['Tasa Servicios Realizados (%)'] = round(df['Tasa Servicios Realizados (%)'],2)
        df['Tasa Ingresos (%)'] = round(df['Tasa Ingresos (%)'],2)
        df['Tasa Servicios Foráneos (%)'] = round(df['Tasa Servicios Foráneos (%)'],2)
        df['Tasa Servicios Locales (%)'] = round(df['Tasa Servicios Locales (%)'],2)
        df['Tasa Servicios Repartos (%)'] = round(df['Tasa Servicios Repartos (%)'],2)

        df = df.reindex(columns=['Año','Mes','Servicios Reales','Tasa Servicios Reales (%)','Servicios Realizados','Tasa Servicios Realizados (%)', 'Ingresos', 'Tasa Ingresos (%)', 'Servicios Foráneos', 'Tasa Servicios Foráneos (%)', 'Servicios Locales', 'Tasa Servicios Locales (%)', 'Servicios Repartos', 'Tasa Servicios Repartos (%)'])

        return df
    
    try:

        df1 = load_ppe()
        df1['Fecha Inicio'] = pd.to_datetime(df1['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df1['Año'] = df1['Fecha Inicio'].apply(lambda x: x.year)
        df1['MesN'] = df1['Fecha Inicio'].apply(lambda x: x.month)
        df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
        datos = df1.copy()

        tabb1, tabb2, tabb3 = st.tabs(["Descripción de Métricas  |", "Métricas por Base(s)  |", "Métricas por Cliente(s)"])

        with tabb1:
        
            #Modulo de Indicadores
            st.markdown("<h2 style='text-align: left;'>Métricas de Pago por Evento</h2>", unsafe_allow_html=True)

            pathLogo = pathLogo = './img/metricas.png'
            display = Image.open(pathLogo)
            display = np.array(display)
            col11, col22, col33 = st.columns([1,5,1])
            col22.image(display, use_column_width=True)

        with tabb2:
            
            st.markdown("<h3 style='text-align: left;'>Métricas de Pago por Evento - Por Base(s)</h3>", unsafe_allow_html=True)
            st.write(f"Seleccione rango de fechas entre **{datos.Mes.values[0]} {datos.Año.values[0].astype(int)}** a **Mayo 2023** para análisis comparativo mensual:")
            x1, x2, x3 = st.columns(3)

            datos['Base Cliente'] = datos['Base Cliente'].astype(str)
            with x1:
                containerC1 = st.container()
                allC1 = st.checkbox("Seleccionar Todos", key="FF")
                if allC1: 
                    sorted_unique_client3 = sorted(datos['Base Cliente'].unique())
                    selected_client3 = containerC1.multiselect('Bases(s):', sorted_unique_client3, sorted_unique_client3, key="FF1")
                    df_selected_client3 = datos[datos['Base Cliente'].isin(selected_client3)].astype(str)
                else:
                    sorted_unique_client3 = sorted(datos['Base Cliente'].unique())
                    selected_client3 = containerC1.multiselect('Bases(s)', sorted_unique_client3, key="FF1")
                    df_selected_client3 = datos[datos['Base Cliente'].isin(selected_client3)].astype(str)
            
            with x2:
                containerTS1 = st.container()
                allTS1 = st.checkbox("Seleccionar Todos", key="GG")
                if allTS1:
                    sorted_unique_ts3 = sorted(df_selected_client3['Tipo Servicio'].unique())
                    selected_ts3 = containerTS1.multiselect('Tipo Servicio(s):', sorted_unique_ts3, sorted_unique_ts3, key="GG1") 
                    df_selected_ts3 = df_selected_client3[df_selected_client3['Tipo Servicio'].isin(selected_ts3)].astype(str)
                else:
                    sorted_unique_ts3 = sorted(df_selected_client3['Tipo Servicio'].unique())
                    selected_ts3 = containerTS1.multiselect('Tipo Servicio(s):', sorted_unique_ts3, key="GG1") 
                    df_selected_ts3 = df_selected_client3[df_selected_client3['Tipo Servicio'].isin(selected_ts3)].astype(str)

            with x3:
                data1 = df_rango_fechas_bases(df_selected_ts3)
            
            #### Módulo Marco de Datos
   
            data1 = data1.sort_values(by='Fecha Inicio')
            st.subheader(f"Comparativa de {data1.Mes.values[0]} {data1.Año.values[0]} vs {data1.Mes.values[-1]} {data1.Año.values[-1]}")

            data2 =  df_grafico_bases(data1)

            servicios_reales_inicial = data2['Servicios Reales'].values[0]
            servicios_reales_final = data2['Servicios Reales'].values[-1]

            servcios_realizados_inicial = data2['Servicios Realizados'].values[0]
            servcios_realizados_final = data2['Servicios Realizados'].values[-1]

            ingresos_inicial = data2['Ingresos'].values[0]
            ingresos_final = data2['Ingresos'].values[-1]

            ingresos_pcapita_inicial = data2['Ingresos Per Cápita'].values[0]
            ingresos_pcapita_final = data2['Ingresos Per Cápita'].values[-1]

            serv_pcapita_incial = data2['Servicios Per Cápita'].values[0]
            serv_pcapita_final = data2['Servicios Per Cápita'].values[-1]

            servicios_foraneos_inicial = data2['Servicios Foráneos'].values[0]
            servicios_foraneos_final = data2['Servicios Foráneos'].values[-1]

            servicios_locales_inicial = data2['Servicios Locales'].values[0]
            servicios_locales_final = data2['Servicios Locales'].values[-1]

            servicios_repartos_inicial = data2['Servicios Repartos'].values[0]
            servicios_repartos_final = data2['Servicios Repartos'].values[-1]

            hora_pcapita_inicial = data2['Horas Per Cápita'].values[0]
            hora_pcapita_final = data2['Horas Per Cápita'].values[-1]

            productividad_incial = round(data2['Productividad(%)'].values[0],2)
            productividad_final = round(data2['Productividad(%)'].values[-1],2)

            vSReales = round((((servicios_reales_final - servicios_reales_inicial)/servicios_reales_inicial)*100),1)
            vSRealizados = round((((servcios_realizados_final - servcios_realizados_inicial)/servcios_realizados_inicial)*100),1)
            vIng = round((((ingresos_final - ingresos_inicial)/ingresos_inicial)*100),1)
            vIngPC = round((((ingresos_pcapita_final - ingresos_pcapita_inicial)/ingresos_pcapita_inicial)*100),1)
            vSPC = round((((serv_pcapita_final - serv_pcapita_incial)/serv_pcapita_incial)*100),1)
            vSF = round((((servicios_foraneos_final - servicios_foraneos_inicial)/servicios_foraneos_inicial)*100),1)
            vSL = round((((servicios_locales_final - servicios_locales_inicial)/servicios_locales_inicial)*100),1)
            vSR = round((((servicios_repartos_final - servicios_repartos_inicial)/servicios_repartos_inicial)*100),1)
            vHPC = round((((hora_pcapita_final - hora_pcapita_inicial)/hora_pcapita_inicial)*100),1)
            vP = round((((productividad_final - productividad_incial)/productividad_incial)),1)

            f1, f2, f3, f4, f5 = st.columns(5)
        
            with f1:
                st.metric(label="Servicios Reales", value= servicios_reales_inicial, delta= "%s%%" % vSReales)

            with f2:
                st.metric(label="Servicios Realizados", value= servcios_realizados_inicial, delta= "%s%%" % vSRealizados)

            with f3:
                st.metric(label="Ingresos", value= ingresos_inicial, delta= "%s%%" % vIng)
            
            with f4:
                st.metric(label="Ingresos Per Cápita", value= ingresos_pcapita_inicial, delta= "%s%%" %vIngPC)
            
            with f5:
                st.metric(label="Servicios per Cápita", value= serv_pcapita_incial, delta= "%s%%" % vSPC)

            g1, g2, g3, g4, g5 = st.columns(5)

            with g1:
                st.metric(label="Productividad (%)", value= productividad_incial, delta= "%s%%" %vP)

            with g2:
                st.metric(label="Servicios Foráneos", value= servicios_foraneos_inicial, delta= "%s%%" %vSF)
        
            with g3:
                st.metric(label="Servicios Locales", value= servicios_locales_inicial, delta= "%s%%" %vSL)

            with g4:
                st.metric(label="Servicios Repartos", value= servicios_repartos_inicial, delta= "%s%%" %vSR)

            with g5:
                st.metric(label="Horas per Cápita", value= hora_pcapita_inicial, delta= "%s%%" %vHPC)
        
            data3 = data2.copy()
            st.subheader(f"Tasa de Variación de {data3.Mes.values[0]} {data3.Año.values[0]} a {data3.Mes.values[-1]} {data3.Año.values[-1]}")
            h1, h2, h3 = st.columns([1,5,1])
            with h2:
            
                data4 = tasa_variacion_ppe_bases(data3)
                st.dataframe(data4)

        with tabb3:
            
            st.markdown("<h3 style='text-align: left;'>Métricas de Pago por Evento - Por Cliente(s)</h3>", unsafe_allow_html=True)
            st.write(f"Seleccione rango de fechas entre **{datos.Mes.values[0]} {datos.Año.values[0].astype(int)}** a **Mayo 2023** para análisis comparativo mensual:")
            
            s1, s2, s3 = st.columns(3)
            data5 = df1.copy()
            data5['Cliente'] = data5['Cliente'].astype(str)
            
            with s1:
                containerCC1 = st.container()
                allCC1 = st.checkbox("Seleccionar Todos", key="L")
                if allCC1: 
                    sorted_unique_client2 = sorted(data5['Cliente'].unique())
                    selected_client2 = containerCC1.multiselect('Cliente(s):', sorted_unique_client2, sorted_unique_client2, key="L1")
                    df_selected_client2 = data5[data5['Cliente'].isin(selected_client2)].astype(str)
                else:
                    sorted_unique_client2 = sorted(data5['Cliente'].unique())
                    selected_client2 = containerCC1.multiselect('Cliente(s)', sorted_unique_client2, key="L1")
                    df_selected_client2 = data5[data5['Cliente'].isin(selected_client2)].astype(str)
            with s2:
                containerTSS1 = st.container()
                allTSS1 = st.checkbox("Seleccionar Todos", key="J")
                if allTSS1:
                    sorted_unique_ts2 = sorted(df_selected_client2['Tipo Servicio'].unique())
                    selected_ts2 = containerTSS1.multiselect('Tipo Servicio(s):', sorted_unique_ts2, sorted_unique_ts2, key="J1") 
                    df_selected_ts2 = df_selected_client2[df_selected_client2['Tipo Servicio'].isin(selected_ts2)].astype(str)
                else:
                    sorted_unique_ts2 = sorted(df_selected_client2['Tipo Servicio'].unique())
                    selected_ts2 = containerTSS1.multiselect('Tipo Servicio(s):', sorted_unique_ts2, key="J1") 
                    df_selected_ts2 = df_selected_client2[df_selected_client2['Tipo Servicio'].isin(selected_ts2)].astype(str)
            
            with s3:
                data6 = df_rango_fechas_cliente(df_selected_ts2)

            #### Módulo Marco de Datos
   
            data6 = data6.sort_values(by='Fecha Inicio')
            st.subheader(f"Comparativa de {data6.Mes.values[0]} {data6.Año.values[0]} vs {data6.Mes.values[-1]} {data6.Año.values[-1]}")

            data7 =  df_grafico_clientes(data6)

            servicios_reales_inicial1 = data7['Servicios Reales'].values[0]
            servicios_reales_final1 = data7['Servicios Reales'].values[-1]

            servcios_realizados_inicial1 = data7['Servicios Realizados'].values[0]
            servcios_realizados_final1 = data7['Servicios Realizados'].values[-1]

            ingresos_inicial1 = data7['Ingresos'].values[0]
            ingresos_final1 = data7['Ingresos'].values[-1]

            servicios_foraneos_inicial1 = data7['Servicios Foráneos'].values[0]
            servicios_foraneos_final1 = data7['Servicios Foráneos'].values[-1]

            servicios_locales_inicial1 = data7['Servicios Locales'].values[0]
            servicios_locales_final1 = data7['Servicios Locales'].values[-1]

            servicios_repartos_inicial1 = data7['Servicios Repartos'].values[0]
            servicios_repartos_final1 = data7['Servicios Repartos'].values[-1]

            vSReales1 = round((((servicios_reales_final1 - servicios_reales_inicial1)/servicios_reales_inicial1)*100),1)
            vSRealizados1 = round((((servcios_realizados_final1 - servcios_realizados_inicial1)/servcios_realizados_inicial1)*100),1)
            vIng1 = round((((ingresos_final1 - ingresos_inicial1)/ingresos_inicial1)*100),1)
            vSF1 = round((((servicios_foraneos_final1 - servicios_foraneos_inicial1)/servicios_foraneos_inicial1)*100),1)
            vSL1 = round((((servicios_locales_final1 - servicios_locales_inicial1)/servicios_locales_inicial1)*100),1)
            vSR1 = round((((servicios_repartos_final1 - servicios_repartos_inicial1)/servicios_repartos_inicial1)*100),1)

            ff1, ff2, ff3 = st.columns(3)
        
            with ff1:
                st.metric(label="Servicios Reales", value= servicios_reales_inicial1, delta= "%s%%" % vSReales1)

            with ff2:
                st.metric(label="Servicios Realizados", value= servcios_realizados_inicial1, delta= "%s%%" % vSRealizados1)

            with ff3:
                st.metric(label="Ingresos", value= ingresos_inicial1, delta= "%s%%" % vIng1)

            gg1, gg2, gg3 = st.columns(3)

            with gg1:
                st.metric(label="Servicios Foráneos", value= servicios_foraneos_inicial1, delta= "%s%%" %vSF1)
        
            with gg2:
                st.metric(label="Servicios Locales", value= servicios_locales_inicial1, delta= "%s%%" %vSL1)

            with gg3:
                st.metric(label="Servicios Repartos", value= servicios_repartos_inicial1, delta= "%s%%" %vSR1)

            data8 = data7.copy()
            st.subheader(f"Tasa de Variación de {data8.Mes.values[0]} {data8.Año.values[0]} a {data8.Mes.values[-1]} {data8.Año.values[-1]}")
            hh1, hh2, hh3 = st.columns([1,5,1])
            with hh2:
            
                data9 = tasa_variacion_ppe_clientes(data8)
                st.dataframe(data9)

    except ZeroDivisionError as e:
        print("Seleccionar: ", e)
    
    except KeyError as e:
        print("Seleccionar: ", e)

    except ValueError as e:
        print("Seleccionar: ", e)
    
    except IndexError as e:
        print("Seleccionar: ", e)

     # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    return True
