### Librerías
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from dateutil.relativedelta import *
import plotly.graph_objects as go
from PIL import Image

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

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
    
    def df_grafico(df):
    
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
        pSer18.columns = ['Fecha', 'Horas Totales IVR','Servicios Reales','Servicios Realizados','Plantilla Promedio','Dias Descanso','Ingresos','Mes','Año','Días del Mes', 'Servicios Foraneos', 'Servicios Locales', 'Servicios Repartos']
        pSer18['Relación Reales/Realizados'] = np.ceil(pSer18['Servicios Reales'] / pSer18['Servicios Realizados'])
        pSer18['Servicios Per Cápita'] = np.ceil(pSer18['Servicios Realizados'] / pSer18['Plantilla Promedio'])
        pSer18['Horas Per Cápita IVR'] = np.ceil(pSer18['Horas Totales IVR'] / pSer18['Plantilla Promedio'])
        pSer18['Horas Teóricas Per Cápita'] = ((pSer18['Días del Mes'] - pSer18['Dias Descanso']) * 24)
        pSer18['Productividad(%)'] = (pSer18['Horas Totales IVR'] / (pSer18['Horas Teóricas Per Cápita'] * pSer18['Plantilla Promedio'])) * 100
        pSer18['Ingresos Per Cápita'] = np.ceil(pSer18['Ingresos'] / pSer18['Plantilla Promedio'])
        pSer18['Duración Promedio (Hrs)'] = np.ceil(pSer18['Horas Totales IVR'] / pSer18['Servicios Realizados'])
        pSer18 = pSer18.replace([np.inf, -np.inf], 0)  
        pSer18 = pSer18.fillna(0)
        pSer18['Relación Reales/Realizados'] = pSer18['Relación Reales/Realizados'].astype(int)
        pSer18['Servicios Per Cápita'] = pSer18['Servicios Per Cápita'].astype(int)
        pSer18['Horas Per Cápita IVR'] = pSer18['Horas Per Cápita IVR'].astype(int)
        pSer18['Servicios Locales'] = pSer18['Servicios Locales'].astype(int)
        pSer18['Servicios Foraneos'] = pSer18['Servicios Foraneos'].astype(int)
        pSer18['Servicios Repartos'] = pSer18['Servicios Repartos'].astype(int)
        pSer18['Servicios Foraneos(%)'] = (pSer18['Servicios Foraneos'] / pSer18['Servicios Realizados']) * 100
        pSer18['Servicios Locales(%)'] = (pSer18['Servicios Locales'] / pSer18['Servicios Realizados']) * 100
        pSer18['Servicios Repartos(%)'] = (pSer18['Servicios Repartos'] / pSer18['Servicios Realizados']) * 100
        pSer18 = pSer18.astype({"Servicios Reales":"int","Servicios Realizados":"int","Relación Reales/Realizados":"int","Días del Mes":"int","Horas Totales IVR":"int","Servicios Per Cápita":"int","Horas Per Cápita IVR":"int"})
        pSer18 = pSer18.iloc[0:17]
    
        return pSer18
    
    def df_grafico_cliente(df):
    
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
        pSer18.columns = ['Fecha', 'Horas Totales IVR','Servicios Reales','Servicios Realizados','Ingresos','Mes','Año','Días del Mes', 'Servicios Foraneos', 'Servicios Locales', 'Servicios Repartos']
        pSer18['Relación Reales/Realizados'] = np.ceil(pSer18['Servicios Reales'] / pSer18['Servicios Realizados'])
        pSer18['Duración Promedio (Hrs)'] = np.ceil(pSer18['Horas Totales IVR'] / pSer18['Servicios Realizados'])
        pSer18 = pSer18.replace([np.inf, -np.inf], 0)  
        pSer18 = pSer18.fillna(0)
        pSer18['Relación Reales/Realizados'] = pSer18['Relación Reales/Realizados'].astype(int)
        pSer18['Servicios Locales'] = pSer18['Servicios Locales'].astype(int)
        pSer18['Servicios Foraneos'] = pSer18['Servicios Foraneos'].astype(int)
        pSer18['Servicios Repartos'] = pSer18['Servicios Repartos'].astype(int)
        pSer18['Servicios Foraneos(%)'] = (pSer18['Servicios Foraneos'] / pSer18['Servicios Realizados']) * 100
        pSer18['Servicios Locales(%)'] = (pSer18['Servicios Locales'] / pSer18['Servicios Realizados']) * 100
        pSer18['Servicios Repartos(%)'] = (pSer18['Servicios Repartos'] / pSer18['Servicios Realizados']) * 100
        pSer18 = pSer18.astype({"Servicios Reales":"int","Servicios Realizados":"int","Relación Reales/Realizados":"int","Días del Mes":"int","Horas Totales IVR":"int"})
        pSer18 = pSer18.iloc[0:17]
    
        return pSer18
    
    def planeación_agregada(df):

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
        pSer18['Días del Mes'] = pSer18['Fecha Inicio'].dt.daysinmonth
        pSer18 = pSer18[['Fecha Inicio','Duración', 'Bitácora','Orden de Servicio','Plantilla Promedio','Dias Descanso','Ingresos','Mes','Año','Días del Mes', 'Foraneos', 'Locales', 'Repartos']]
        pSer18.columns = ['Fecha', 'Horas Totales IVR','Servicios Reales','Servicios Realizados','Plantilla Promedio','Dias Descanso','Ingresos','Mes','Año','Días del Mes', 'Servicios Foraneos', 'Servicios Locales', 'Servicios Repartos']
        pSer18['Relación Reales/Realizados'] = np.ceil(pSer18['Servicios Reales'] / pSer18['Servicios Realizados'])
        pSer18['Servicios Per Cápita'] = np.ceil(pSer18['Servicios Realizados'] / pSer18['Plantilla Promedio'])
        pSer18['Horas Per Cápita IVR'] = np.ceil(pSer18['Horas Totales IVR'] / pSer18['Plantilla Promedio'])
        pSer18['Horas Teóricas Per Cápita'] = ((pSer18['Días del Mes'] - pSer18['Dias Descanso']) * 24)
        pSer18['Productividad(%)'] = (pSer18['Horas Totales IVR'] / (pSer18['Horas Teóricas Per Cápita'] * pSer18['Plantilla Promedio'])) * 100
        pSer18['Ingresos Per Cápita'] = np.ceil(pSer18['Ingresos'] / pSer18['Plantilla Promedio'])
        pSer18['Duración Promedio (Hrs)'] = np.ceil(pSer18['Horas Totales IVR'] / pSer18['Servicios Realizados'])
        pSer18['Servicios Foraneos(%)'] = (pSer18['Servicios Foraneos'] / pSer18['Servicios Realizados']) * 100
        pSer18['Servicios Locales(%)'] = (pSer18['Servicios Locales'] / pSer18['Servicios Realizados']) * 100
        pSer18['Servicios Repartos(%)'] = (pSer18['Servicios Repartos'] / pSer18['Servicios Realizados']) * 100
        pSer18 = pSer18.replace([np.inf, -np.inf], 0)  
        pSer18 = pSer18.fillna(0)
        pSer18['Relación Reales/Realizados'] = pSer18['Relación Reales/Realizados'].astype(int)
        pSer18['Servicios Per Cápita'] = pSer18['Servicios Per Cápita'].astype(int)
        pSer18['Horas Per Cápita IVR'] = pSer18['Horas Per Cápita IVR'].astype(int)
        pSer18['Servicios Locales'] = pSer18['Servicios Locales'].astype(int)
        pSer18['Servicios Foraneos'] = pSer18['Servicios Foraneos'].astype(int)
        pSer18['Servicios Repartos'] = pSer18['Servicios Repartos'].astype(int)
        pSer18 = pSer18.astype({"Servicios Reales":"int","Servicios Realizados":"int","Relación Reales/Realizados":"int","Días del Mes":"int","Horas Totales IVR":"int","Servicios Per Cápita":"int","Horas Per Cápita IVR":"int"})
        pSer18 = pSer18.iloc[0:17]
        pSer18['Mes'] = pSer18['Mes'].astype('category')
        pSer18['Mes'] = pSer18['Mes'].cat.set_categories(['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])            
        pSer19 = pSer18.pivot_table(columns= ['Año','Mes'], values = ['Días del Mes', 'Plantilla Promedio', 'Horas Totales IVR', 'Horas Per Cápita IVR', 'Horas Teóricas Per Cápita', 'Productividad(%)', 'Ingresos', 'Ingresos Per Cápita','Servicios Realizados', 'Servicios Locales', 'Servicios Foraneos', 'Servicios Repartos', 'Servicios Locales(%)', 'Servicios Foraneos(%)', 'Servicios Repartos(%)', 'Servicios Per Cápita'], sort=True)
        pSer19 = pSer19.reindex(['Días del Mes', 'Plantilla Promedio', 'Horas Totales IVR', 'Horas Per Cápita IVR', 'Horas Teóricas Per Cápita', 'Productividad(%)', 'Ingresos', 'Ingresos Per Cápita','Servicios Realizados', 'Servicios Locales', 'Servicios Foraneos', 'Servicios Repartos', 'Servicios Locales(%)', 'Servicios Foraneos(%)', 'Servicios Repartos(%)', 'Servicios Per Cápita'])
        pSer19 = pSer19.astype(int)
    
        return pSer19    
    

    def planeación_agregada_cliente(df):

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
        pSer18['Días del Mes'] = pSer18['Fecha Inicio'].dt.daysinmonth
        pSer18 = pSer18[['Fecha Inicio','Duración', 'Bitácora','Orden de Servicio','Ingresos','Mes','Año','Días del Mes', 'Foraneos', 'Locales', 'Repartos']]
        pSer18.columns = ['Fecha', 'Horas Totales IVR','Servicios Reales','Servicios Realizados','Ingresos','Mes','Año','Días del Mes', 'Servicios Foraneos', 'Servicios Locales', 'Servicios Repartos']
        pSer18['Relación Reales/Realizados'] = np.ceil(pSer18['Servicios Reales'] / pSer18['Servicios Realizados'])
        pSer18['Duración Promedio (Hrs)'] = np.ceil(pSer18['Horas Totales IVR'] / pSer18['Servicios Realizados'])
        pSer18['Servicios Foraneos(%)'] = (pSer18['Servicios Foraneos'] / pSer18['Servicios Realizados']) * 100
        pSer18['Servicios Locales(%)'] = (pSer18['Servicios Locales'] / pSer18['Servicios Realizados']) * 100
        pSer18['Servicios Repartos(%)'] = (pSer18['Servicios Repartos'] / pSer18['Servicios Realizados']) * 100
        pSer18 = pSer18.replace([np.inf, -np.inf], 0)  
        pSer18 = pSer18.fillna(0)
        pSer18['Relación Reales/Realizados'] = pSer18['Relación Reales/Realizados'].astype(int)
        pSer18['Servicios Locales'] = pSer18['Servicios Locales'].astype(int)
        pSer18['Servicios Foraneos'] = pSer18['Servicios Foraneos'].astype(int)
        pSer18['Servicios Repartos'] = pSer18['Servicios Repartos'].astype(int)
        pSer18 = pSer18.astype({"Servicios Reales":"int","Servicios Realizados":"int","Relación Reales/Realizados":"int","Días del Mes":"int","Horas Totales IVR":"int"})
        pSer18 = pSer18.iloc[0:17]
        pSer18['Mes'] = pSer18['Mes'].astype('category')
        pSer18['Mes'] = pSer18['Mes'].cat.set_categories(['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])            
        pSer19 = pSer18.pivot_table(columns= ['Año','Mes'], values = ['Días del Mes', 'Horas Totales IVR', 'Ingresos','Servicios Realizados', 'Servicios Locales', 'Servicios Foraneos', 'Servicios Repartos', 'Servicios Locales(%)', 'Servicios Foraneos(%)', 'Servicios Repartos(%)'], sort=True)
        pSer19 = pSer19.reindex(['Días del Mes', 'Horas Totales IVR', 'Ingresos','Servicios Realizados', 'Servicios Locales', 'Servicios Foraneos', 'Servicios Repartos', 'Servicios Locales(%)', 'Servicios Foraneos(%)', 'Servicios Repartos(%)'])
        pSer19 = pSer19.astype(int)
    
        return pSer19    
    
    st.cache_data(ttl=3600)
    def g_ingresosvssalidas(df):

        sr_data2 = go.Bar(x = df['Fecha'],
                        y=df['Servicios Foraneos(%)'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Foraneos',
                        text= [f'Foraneos: {x:.0f}%' for x in df['Servicios Foraneos(%)']]
                        )
    
        sr_data3 = go.Bar(x = df['Fecha'],
                        y=df['Servicios Locales(%)'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Locales',
                        text= [f'Locales: {x:.0f}%' for x in df['Servicios Locales(%)']]
                        )
    
        sr_data4 = go.Bar(x = df['Fecha'],
                        y=df['Servicios Repartos(%)'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Repartos',
                        text= [f'Repartos: {x:.0f}%' for x in df['Servicios Repartos(%)']]
                        )
    
        sr_data1 = go.Scatter(x = df['Fecha'],
                        y=df['Ingresos'],
                        line=go.scatter.Line(color='purple', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='Ingresos',
                        text= [f'Ingresos/Mes: {x:.0f} Pesos' for x in df['Ingresos']],
                        textposition="top center")

        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='Ingresos vs Tipo de Servicio',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Ingresos/Mes', color='red', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='Servicios/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2, sr_data3, sr_data4], layout=layout)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

    st.cache_data(ttl=3600)
    def g_ingresospercapitavsserviciospercapita(df):
    
        sr_data1 = go.Bar(x = df['Fecha'],
                        y=df['Servicios Per Cápita'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Servicios Per Cápita',
                        text= [f'Servicios per Cápita/Mes: {x:.0f}' for x in df['Servicios Per Cápita']]
                        )
    
        sr_data2 = go.Scatter(x = df['Fecha'],
                        y=df['Ingresos Per Cápita'],
                        line=go.scatter.Line(color='red', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='Ingresos Per Cápita',
                        text= [f'Ingresos per Cápita/Mes: {x:.0f}' for x in df['Ingresos Per Cápita']])

        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='Ingresos per Cápita vs Servicios per Cápita',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Servicios per Cápita/Mes', color='red', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='Ingresos per Cápita/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2], layout=layout)
        st.plotly_chart(fig)

    st.cache_data(ttl=3600)
    def g_serviciospercapitavshoraspercapita(df):
    
        sr_data1 = go.Bar(x = df['Fecha'],
                        y=df['Horas Per Cápita IVR'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Horas Per Cápita IVR',
                        text= [f'Horas Per Cápita IVR/Mes: {x:.0f}' for x in df['Horas Per Cápita IVR']]
                        )
    
        sr_data2 = go.Scatter(x = df['Fecha'],
                        y=df['Servicios Per Cápita'],
                        line=go.scatter.Line(color='red', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='Servicios Per Cápita',
                        text= [f'Servicios Per Cápita/Mes: {x:.0f}' for x in df['Servicios Per Cápita']])

        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='Servicios per Cápita vs Horas per Cápita IVR',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Ingresos per Cápita/Mes', color='green', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='Servicios per Cápita/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2], layout=layout)
        st.plotly_chart(fig)

    st.cache_data(ttl=3600)
    def g_salidas(df):

        sr_data2 = go.Bar(x = df['Fecha'],
                        y=df['Servicios Foraneos'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Foraneos',
                        text= [f'Foraneos: {x:.0f} viajes' for x in df['Servicios Foraneos']]
                        )
    
        sr_data3 = go.Bar(x = df['Fecha'],
                        y=df['Servicios Locales'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Locales',
                        text= [f'Locales: {x:.0f} viajes' for x in df['Servicios Locales']]
                        )
    
        sr_data4 = go.Bar(x = df['Fecha'],
                        y=df['Servicios Repartos'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Repartos',
                        text= [f'Repartos: {x:.0f} viajes' for x in df['Servicios Repartos']]
                        )
    
        sr_data1 = go.Scatter(x = df['Fecha'],
                        y=df['Servicios Reales'],
                        line=go.scatter.Line(color='green', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='Servicios Reales',
                        text= [f'Servicios/Mes: {x:.0f} viajes' for x in df['Servicios Reales']])

        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='Salidas por Tipo de Servicio',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Servicios/Mes', color='green', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='Servicios/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2, sr_data3, sr_data4], layout=layout)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

    try:

        df = load_ppe()
        df['Fecha Inicio'] = pd.to_datetime(df['Fecha Inicio'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df['Año'] = df['Fecha Inicio'].apply(lambda x: x.year)
        df['MesN'] = df['Fecha Inicio'].apply(lambda x: x.month)
        df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
        data = df.copy()

        tab1, tab2, tab3 = st.tabs(["Descripción de Indicadores  |", "Indicadores por Base(s)  |", "Indicadores por Cliente(s)"])

        with tab1:
        
            #Modulo de Indicadores
            st.markdown("<h2 style='text-align: left;'>Indicadores de Pago por Evento</h2>", unsafe_allow_html=True)

            pathLogo = pathLogo = './img/indicadoresppe1.png'
            display = Image.open(pathLogo)
            display = np.array(display)
            col1, col2, col3 = st.columns([1,5,1])
            col2.image(display, use_column_width=True)
            pathLogo1 = './img/indicadoresppe2.png'
            display1 = Image.open(pathLogo1)
            display1 = np.array(display1)
            co1, co2, co3 = st.columns([1,5,1])
            co2.image(display1, use_column_width=True)

        with tab2:

            st.markdown("<h3 style='text-align: left;'>Gráfico Indicadores de Pago por Evento - Por Base</h3>", unsafe_allow_html=True)
            data['Año'] = pd.to_numeric(data['Año'], downcast="integer") #Esto lo hice para que el texto de años aparezca como entero  
            st.write(f"Este marco de datos contiene registro histórico de servicios realizados en Pago por Evento desde **{data.Mes.values[0]} {data.Año.values[0].astype(int)}** a **Mayo 2023**.")

            c1, c2 = st.columns(2)
        
            data['Base Cliente'] = data['Base Cliente'].astype(str)
            with c1:
                containerC = st.container()
                allC = st.checkbox("Seleccionar Todos", key="E")
                if allC: 
                    sorted_unique_client = sorted(data['Base Cliente'].unique())
                    selected_client = containerC.multiselect('Bases(s):', sorted_unique_client, sorted_unique_client, key="E1")
                    df_selected_client = data[data['Base Cliente'].isin(selected_client)].astype(str)
                else:
                    sorted_unique_client = sorted(data['Base Cliente'].unique())
                    selected_client = containerC.multiselect('Bases(s)', sorted_unique_client, key="E1")
                    df_selected_client = data[data['Base Cliente'].isin(selected_client)].astype(str)
        
            with c2:
                containerTS = st.container()
                allTS = st.checkbox("Seleccionar Todos", key="F")
                if allTS:
                    sorted_unique_ts = sorted(df_selected_client['Tipo Servicio'].unique())
                    selected_ts = containerTS.multiselect('Tipo Servicio(s):', sorted_unique_ts, sorted_unique_ts, key="F1") 
                    df_selected_ts = df_selected_client[df_selected_client['Tipo Servicio'].isin(selected_ts)].astype(str)
                else:
                    sorted_unique_ts = sorted(df_selected_client['Tipo Servicio'].unique())
                    selected_ts = containerTS.multiselect('Tipo Servicio(s):', sorted_unique_ts, key="F1") 
                    df_selected_ts = df_selected_client[df_selected_client['Tipo Servicio'].isin(selected_ts)].astype(str)
        
            df_planeacion = df_selected_ts.copy()
            df_planeacion1 = planeación_agregada(df_planeacion)
            st.dataframe(df_planeacion1)

            grafico_indicadores = df_grafico(df_planeacion)

            g_is = g_ingresosvssalidas(grafico_indicadores) #grafico ingresos vs salidas
            g_ispc = g_ingresospercapitavsserviciospercapita(grafico_indicadores) #grafico ingresos per capita vs salidas per capita
            g_shpc = g_serviciospercapitavshoraspercapita(grafico_indicadores) #grafico servicios per capita vs horas per capita
    
        with tab3:

            data1 = df.copy()
            st.markdown("<h3 style='text-align: left;'>Gráfico Indicadores de Pago por Evento - Por Cliente</h3>", unsafe_allow_html=True)
            st.write(f'Este marco de datos contiene registro histórico de servicios realizados en Pago por Evento desde **{data1.Mes.values[0]} {data1.Año.values[0].astype(int)}** a **Mayo 2023**.')

            d1, d2 = st.columns(2)
        
            data1['Cliente'] = data1['Cliente'].astype(str)
            with d1:
                containerCl = st.container()
                allCl = st.checkbox("Seleccionar Todos", key="G")
                if allCl: 
                    sorted_unique_client1 = sorted(data1['Cliente'].unique())
                    selected_client1 = containerCl.multiselect('Cliente(s):', sorted_unique_client1, sorted_unique_client1, key="G1")
                    df_selected_client1 = data1[data1['Cliente'].isin(selected_client1)].astype(str)
                else:
                    sorted_unique_client1 = sorted(data1['Cliente'].unique())
                    selected_client1 = containerCl.multiselect('Cliente(s)', sorted_unique_client1, key="G1")
                    df_selected_client1 = data1[data1['Cliente'].isin(selected_client1)].astype(str)
        
            with d2:
                containerTSC = st.container()
                allTSC = st.checkbox("Seleccionar Todos", key="H")
                if allTSC:
                    sorted_unique_ts1 = sorted(df_selected_client1['Tipo Servicio'].unique())
                    selected_ts1 = containerTSC.multiselect('Tipo Servicio(s):', sorted_unique_ts1, sorted_unique_ts1, key="H1") 
                    df_selected_ts1 = df_selected_client1[df_selected_client1['Tipo Servicio'].isin(selected_ts1)].astype(str)
                else:
                    sorted_unique_ts1 = sorted(df_selected_client1['Tipo Servicio'].unique())
                    selected_ts1 = containerTSC.multiselect('Tipo Servicio(s):', sorted_unique_ts1, key="H1") 
                    df_selected_ts1 = df_selected_client1[df_selected_client1['Tipo Servicio'].isin(selected_ts1)].astype(str)
        
            df_planeacion2 = df_selected_ts1.copy()
            df_planeacion3 = planeación_agregada_cliente(df_planeacion2)
            st.dataframe(df_planeacion3)

            grafico_indicadores1 = df_grafico_cliente(df_planeacion2)

            g_salidas_ts = g_salidas(grafico_indicadores1) #grafico salidas por tipo de servicio
            g_is1 = g_ingresosvssalidas(grafico_indicadores1) #grafico ingresos vs salidas

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
