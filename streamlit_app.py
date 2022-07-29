# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 14:19:52 2022

@author: juanj
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components
# from fpdf import FPDF
from tempfile import NamedTemporaryFile
import base64
#%% settings
c_l = "#0C2657"
#%% helper functions
def fecha_str(date):
    dict_m = {'ene':'enero', 'feb':'febrero', 'mar':'marzo', 'abr':'abril', 'may':'mayo',
              'jun':'junio', 'jul':'julio', 'ago':'agosto', 'sep':'septiembre',
              'oct':'octubre', 'nov':'noviembre', 'dic':'diciembre'}
    
    y = date[-2:]
    m = date[:3]
    return dict_m[m]+' '+'20'+y

def mes2num(month):
    dict_m2n = {'ene':1, 'feb':2, 'mar':3, 'abr':4, 'may':5,
              'jun':6, 'jul':7, 'ago':8, 'sep':9,
              'oct':10, 'nov':11, 'dic':12}
    return dict_m2n[month]

#%%
# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="centered", page_title="Monitor de inflacion", page_icon="📈")

# texto
st.markdown(
    """# **Monitor de Inflación**
En esta página puedes monitorear la variación anual y mensual de los precios de los **359 productos que componen la canasta del Índice de Precios al Consumidor (IPC)**. La información ha sido obtenida del Instituto Nacional de Estadística y Censos.
"""
)

# datos

df_anual = pd.read_csv("https://raw.githubusercontent.com/InteligenciaEmpresarial/Inflation_tracker/main/InflacionAnual.csv", sep=';')
df_anual = df_anual.set_index('mes')

df_mensual = pd.read_csv("https://raw.githubusercontent.com/InteligenciaEmpresarial/Inflation_tracker/main/InflacionMensual.csv", sep=';')
df_mensual = df_mensual.set_index('mes')
temp_df = df_mensual.copy()
temp_df.pop('TODOS LOS PRODUCTOS (INFLACION GENERAL)')

df_cum = pd.read_csv("https://raw.githubusercontent.com/InteligenciaEmpresarial/Inflation_tracker/main/InflacionAcumulada.csv", sep=';')
df_cum = df_cum.set_index('mes')

#%%
m_actual = fecha_str(df_mensual.index[-1])

# selector ultimo año acumulado
m_actual_short = df_mensual.index[-1][:3]
scum = mes2num(m_actual_short)
#%%

n1 = (temp_df.iloc[-1]>0).sum()
n2 = (temp_df.iloc[-1]<=0).sum()


#col4, col5 = st.columns(2)
#col4.metric("# de productos que aumentaron su precio en último mes", str(n1))
#col5.metric("# de productos que disminuyeron su precio en último mes", str(n2))
#%%
#st.header("**Tasa de Inflación General al mes de "+m_actual+"**")
st.markdown("### Inflación por producto al mes de "+m_actual)

st.markdown('**Número de productos que aumentaron su precio en último mes:** '+str(n1))
st.markdown('**Número de productos que disminuyeron su precio en último mes:** '+str(n2))

lista_productos = tuple(df_anual.columns.to_list())

option = st.selectbox('Selecciona la cesta de productos:', lista_productos)

ia = df_anual.loc[df_anual.index[-1], option]
im = df_mensual.loc[df_mensual.index[-1], option]
ic = df_cum.loc[df_cum.index[-1], option]

col1, col2, col3 = st.columns(3)
col1.metric("Inflacion anual", str(ia)+"%")
col2.metric("Inflacion mensual", str(im)+"%")
col3.metric("Inflacion acumulada", str(ic)+"%")


#%%

# Variacion anual
fig1 = px.line(df_anual/100, y=option, title=u'<b>Inflación anual de '+option+'</b>', labels={
                     option: "Inflación anual"
                 })
fig1.update_traces(line_color=c_l)

fig1.add_hline(y=0.0, line_width=1, line_dash="dash", line_color="red")

fig1.update_yaxes(title=None)
fig1.update_xaxes(title=None)
fig1.update_xaxes(tickangle=0)

# range slider
fig1.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True)
    ),
    yaxis_tickformat = '.1%')


fig1.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/InteligenciaEmpresarial/Inflation_tracker/main/Imagenes/IE_resize.png",
        xref="paper", yref="paper",
        x=1, y=1.01,
        sizex=0.25, sizey=0.25,
        xanchor="right", yanchor="bottom"
    )
)

st.plotly_chart(fig1, use_container_width=True)

s_ta = ""
if df_anual.loc[df_anual.index[-1],option]>0:
    s_ta = "+"

#st.markdown("La variación de precios **anual** de "+option+" en "+m_actual+" fue "+"**"+s_ta+str(df_anual.loc[df_anual.index[-1],option])+"%**")

#components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """)

# Variacion mensual
fig2 = px.line(df_mensual/100, y=option, title=u'<b>Inflación mensual de '+option+'</b>', labels={
                     option: "Inflación mensual"
                 })
fig2.update_traces(line_color=c_l)
fig2.add_hline(y=0.0, line_width=1, line_dash="dash", line_color="red")

fig2.update_yaxes(title=None)
fig2.update_xaxes(title=None)

# range slider
fig2.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True)
    ),
    yaxis_tickformat = '.1%')

fig2.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/InteligenciaEmpresarial/Inflation_tracker/main/Imagenes/IE_resize.png",
        xref="paper", yref="paper",
        x=1, y=1.01,
        sizex=0.25, sizey=0.25,
        xanchor="right", yanchor="bottom"
    )
)

st.plotly_chart(fig2, use_container_width=True)

s_tm = ""
if df_mensual.loc[df_mensual.index[-1],option]>0:
    s_tm = "+"
    
#st.markdown("La variación de precios **mensual** de "+option+" en "+m_actual+" fue "+"**"+s_tm+str(df_mensual.loc[df_mensual.index[-1],option])+"%**")

# Variacion acumulada
fig3 = px.line(df_cum.iloc[-scum:]/100, y=option, title=u'<b>Inflación acumulada de '+option+'</b>', labels={
                     option: "Inflación acumulada"
                 })
fig3.update_traces(line_color=c_l)

fig3.update_yaxes(title=None)
fig3.update_xaxes(title=None)

fig3.update_layout(
    yaxis_tickformat = '.1%')

fig3.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/InteligenciaEmpresarial/Inflation_tracker/main/Imagenes/IE_resize.png",
        xref="paper", yref="paper",
        x=1, y=1.05,
        sizex=0.15, sizey=0.15,
        xanchor="right", yanchor="bottom"
    )
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader('Definiciones')
st.markdown('**Inflación anual:** Variación del índice de precios anual.')
st.markdown('**Inflación mensual:** Variación del índice de precios mensual.')
st.markdown('**Inflación acumulada:** Es la variación del índice de precios del mes actual vs el mes de diciembre del año anterior.')

#%%
st.subheader("Citar")

"""
```
Inteligencia Empresarial (2022). Monitor de Inflación.
```
"""
#%%
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

