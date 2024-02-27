import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_path = "data/Estudiantes_clear.csv"
df = pd.read_csv(data_path)

# Título de la aplicación
st.title("Dashboard Interactivo")
st.subheader("By: Hector Vasquez & Wilhelm Buitrago")

# Mostrar una vista previa de los datos
st.subheader("Vista previa de los datos")
st.write(df.tail())
st.write(df.describe())

# Análisis exploratorio de datos
st.subheader("Análisis Exploratorio de Datos (EDA)")
# graficos pichurrios

# Creacion de histogramas apartor de variables
st.subheader("Histograma de una variable")
selected_column = st.selectbox("Seleccionar una columna:", df.columns)
plt.hist(df[selected_column])
st.pyplot()

# para el wilhelm se corre ejecuntado streamlit run src/app.py
