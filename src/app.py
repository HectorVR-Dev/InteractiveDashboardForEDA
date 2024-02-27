import streamlit as st
from pages import home, eda, filters, conclusions, resources, feedback
from PIL import Image

# Eliminamos el título predeterminado del Streamlit
icon = Image.open('src/images/grafico-de-dispersion.png')
st.set_page_config(page_title="Interactive Dashboard", page_icon=icon,
                   initial_sidebar_state="auto", layout="wide")

# Renderizamos el menú lateral por defecto y sin el título de la aplicación
st.sidebar.title("Navegación")

# Definimos las opciones de navegación en el menú lateral
page = st.sidebar.radio(
    "",
    ["Inicio", "Análisis Exploratorio de Datos", "Filtros Interactivos",
        "Conclusiones y Recomendaciones", "Recursos Adicionales", "Feedback y Contacto"]
)

# Renderizamos la vista correspondiente según la selección del usuario
if page == "Inicio":
    home.show_home()
elif page == "Análisis Exploratorio de Datos":
    eda.show_eda()

elif page == "Filtros Interactivos":
    filters.show_filters()

elif page == "Conclusiones y Recomendaciones":
    conclusions.show_conclusions()

elif page == "Recursos Adicionales":
    resources.show_resources()

elif page == "Feedback y Contacto":
    feedback.show_feedback()
