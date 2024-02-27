import streamlit as st
from PIL import Image
import pandas as pd


class dashboard():
    def __init__(self):
        self.df = pd.read_csv("data/Estudiantes_clear.csv")
        icon = Image.open('src/images/grafico-de-dispersion.png')
        img = Image.open('src/images/UNAL.png')
        st.set_page_config(page_title="Interactive Dashboard",
                           page_icon=icon, layout="wide")

        st.sidebar.title("Navegación")
        self.page = st.sidebar.radio("", ["Inicio", "Visualizacion EDA", "Filtros Interactivos",
                                     "Conclusiones y Recomendaciones", "Recursos Adicionales", "Feedback y Contacto"])

        st.sidebar.image(img, width=200)
        self.pages = {'Inicio': self.show_home,
                      'Visualizacion EDA': self.show_eda,
                      'Filtros Interactivos': self.show_filters,
                      'Conclusiones y Recomendaciones': self.show_conclusions,
                      'Recursos Adicionales': self.show_resources,
                      'Feedback y Contacto': self.show_feedback}

        self.pages[self.page]()

    def show_home(self):
        st.title("Bienvenido al Dashboard de Análisis de Datos")
        st.markdown(
            """
        Este dashboard interactivo proporciona un espacio en la web para el análisis exploratorio de la base de datos de los estudiantes de la Universidad Nacional de Colombia sede de la Paz. Aquí puedes realizar visualizaciones interactivas, aplicar filtros a los datos, obtener conclusiones clave y acceder a recursos adicionales.

        ### Descripcion de base de datos (Dinara - Listado de estudiantes activos 2024-1)
        El dataset depurado cuenta con las siguientes caracteristicas:

        - Tiene **1321** estudiantes con **23** variables 
        - **8** variables numericas
        - **15** variables categoricas

         A continuacion puede escoger cualquier variable para ver su respectiva descripcion:
        """)
        # st.write()
        var = self.df.columns.to_list()
        var.insert(0, "---")
        var = st.selectbox("Variable:", var)
        st.markdown(self.desc_var(var))

        # st.write(f"Para este año la Universidad Nacional de Colombia Sede de La Paz cuenta con {len(
        #    self.df)} estudiantes activos, el dataset depurado cuenta con 23 variables, 8 numericas",
        #    " y 15 categoricas. ")

    def show_eda(self):
        st.title("Análisis Exploratorio de Datos")
        st.write(
            "En esta sección, puedes explorar y analizar los datos de manera interactiva.")

    def show_filters(self):
        st.title("Filtros Interactivos")
        st.write(
            "Utiliza los filtros interactivos para personalizar tu análisis de datos.")

    def show_conclusions(self):
        st.title("Conclusiones y Recomendaciones")
        st.write(
            "Aquí encontrarás las conclusiones clave y las recomendaciones basadas en el análisis de datos.")

    def show_resources(self):
        st.title("Recursos Adicionales")
        st.write("Explora los recursos adicionales relacionados con el análisis de datos y las tecnologías utilizadas en este proyecto.")

    def show_feedback(self):
        st.title("Feedback y Contacto")
        st.write("¡Nos encantaría conocer tu opinión! Ponte en contacto con nosotros para cualquier comentario o sugerencia.")

    def desc_var(self, var):
        if var == "---":
            des = """
            
            """
        elif var == "COD_PLAN":
            des = """
            ### Descripción de la variable COD_PLAN
            La variable COD_PLAN representa el código asociado al plan de estudios al que está inscrito el estudiante. Este código identifica de manera única cada plan de estudios ofrecido por la institución educativa.

            Tipo de datos: Cadena de caracteres (str).

            Valores posibles: Los valores posibles para esta variable y sus correspondientes planes de estudios son:

            - L006: INGENIERÍA MECATRÓNICA
            - L005: INGENIERÍA BIOLÓGICA
            - L002: ESTADÍSTICA
            - L004: GESTIÓN CULTURAL Y COMUNICATIVA
            - L001: BIOLOGÍA
            - L003: GEOGRAFÍA

            Esta variable es importante para realizar análisis específicos relacionados con la distribución de los estudiantes en diferentes planes de estudios y para comprender mejor la estructura y diversidad de los programas académicos ofrecidos por la institución.
            """
        elif var == "AVANCE_CARRERA":
            des = """
            ### Descripción de la variable AVANCE_CARRERA
            La variable AVANCE_CARRERA representa el avance del estudiante en su carrera universitaria, expresado como un porcentaje que va desde 0 hasta 100. Este valor indica qué tan avanzado está el estudiante en su programa académico en relación con el total de créditos, cursos o requisitos necesarios para completar su carrera.

            - **Tipo de datos**: Flotante (float).
            - **Rango de valores**: El valor de AVANCE_CARRERA varía desde 0 hasta 100, donde 0 indica que el estudiante está en el inicio de su carrera y 100 indica que ha completado todos los requisitos para graduarse.
            Esta variable es importante para evaluar y monitorear el progreso académico de los estudiantes a lo largo del tiempo, identificar posibles problemas de retención estudiantil y proporcionar intervenciones tempranas para apoyar el éxito estudiantil.

            """
        elif var == "COD_ACCESO":
            des = """
            ### Descripción de la variable COD_ACCESO
            La variable COD_ACCESO representa el código asociado al tipo de acceso a la universidad. Este código identifica de que manera ingreso el estudiante a la universidad.

            **Tipo de datos**: Entero (int).

            **Valores posibles**: Los valores posibles para esta variable y sus correspondientes tipos de acceso son:

            - 1: EXAMEN DE ADMISIÓN A LA UNIVERSIDAD
            - 3: TRASLADO

            Esta variable es crucial para comprender el origen de los estudiantes en la institución y para realizar análisis sobre la distribución de los diferentes tipos de acceso en la población estudiantil.
            """
        elif var == "COD_SUBACCESO":
            des = """
            ### Descripción de la variable COD_SUBACCESO
            La variable COD_SUBACCESO representa el código asociado al subtipo de acceso a la universidad. Este código identifica de manera única cada subtipo de acceso especial por el cual el estudiante accedio a la universidad.

            **Tipo de datos**: Entero (int).

            **Valores posibles**: Los valores posibles para esta variable y sus correspondientes subtipos de acceso son:

            - 29: PROGRAMA DE ADMISIÓN ESPECIAL PARA LOS PROGRAMAS DE PREGRADO SEDE LA PAZ
            - 1: REGULAR DE PREGRADO
            - 24: VÍCTIMAS DEL CONFLICTO ARMADO EN COLOMBIA
            - 21: PAES - POBLACION NEGRA, AFROCOLOMBIANA, PALENQUERA Y RAIZAL
            - 3: PAES - INDÍGENA

            Esta variable es fundamental para comprender la diversidad de poblaciones y programas de admisión especial en la institución educativa, así como para realizar análisis sobre la equidad y la inclusión en el acceso a la educación superior.
            """
        elif var == "CONVOCATORIA":
            des = """
            ### Descripción de la variable CONVOCATORIA
            La variable CONVOCATORIA indica el periodo en el que el estudiante se presentó a la prueba de admisión en la universidad. Los periodos se representan en formato año-semestre, comenzando desde el periodo 2019-2 (el primer periodo en que la universidad abrió sus puertas) hasta el periodo actual, que es 2024-1.

            **Tipo de datos**: Cadena de caracteres (str).

            **Valores posibles**: Los valores posibles para esta variable son periodos en formato año-semestre, comenzando desde "2019-2" hasta "2024-1".

            Esta variable es importante para rastrear y analizar la distribución de los estudiantes que ingresaron a la universidad en diferentes periodos académicos, lo que puede proporcionar información útil sobre la evolución del número de estudiantes matriculados a lo largo del tiempo.
            """
        elif var == "APERTURA":
            des = """
            ### Descripción de la variable APERTURA
            La variable APERTURA indica el periodo en el que se abrió la historia académica del estudiante en la universidad. Aunque normalmente coincide con el periodo de convocatoria en el que el estudiante se presentó a la prueba de admisión, puede haber casos en los que el estudiante se presente para un periodo y realice su primer ingreso en otro.

            - **Tipo de datos**: Cadena de caracteres (str).

            - **Valores posibles**: Los valores posibles para esta variable son periodos en formato año-semestre, comenzando desde "2019-2" hasta "2024-1" (o el periodo actual).

            Esta variable es importante para rastrear y analizar la apertura de historias académicas de los estudiantes en diferentes periodos, lo que puede proporcionar información útil sobre la sincronización entre los procesos de admisión y matriculación en la universidad.
            """
        elif var == "T_DOCUMENTO":
            des = """
            ### Descripción de la variable T_DOCUMENTO
            
            [Descripción detallada de la variable T_DOCUMENTO]
            """
        elif var == "GENERO":
            des = """
            ### Descripción de la variable GENERO
            
            [Descripción detallada de la variable GENERO]
            """
        elif var == "EDAD":
            des = """
            ### Descripción de la variable EDAD
            
            [Descripción detallada de la variable EDAD]
            """
        elif var == "NUMERO_MATRICULAS":
            des = """
            ### Descripción de la variable NUMERO_MATRICULAS
            
            [Descripción detallada de la variable NUMERO_MATRICULAS]
            """
        elif var == "PAPA":
            des = """
            ### Descripción de la variable PAPA
            
            [Descripción detallada de la variable PAPA]
            """
        elif var == "PROME_ACADE":
            des = """
            ### Descripción de la variable PROME_ACADE
            
            [Descripción detallada de la variable PROME_ACADE]
            """
        elif var == "PBM_CALCULADO":
            des = """
            ### Descripción de la variable PBM_CALCULADO
            
            [Descripción detallada de la variable PBM_CALCULADO]
            """
        elif var == "ESTRATO":
            des = """
            ### Descripción de la variable ESTRATO
            
            [Descripción detallada de la variable ESTRATO]
            """
        elif var == "COD_DEPTO_RESIDENCIA":
            des = """
            ### Descripción de la variable COD_DEPTO_RESIDENCIA
            
            [Descripción detallada de la variable COD_DEPTO_RESIDENCIA]
            """
        elif var == "COD_MUN_RESIDENCIA":
            des = """
            ### Descripción de la variable COD_MUN_RESIDENCIA
            
            [Descripción detallada de la variable COD_MUN_RESIDENCIA]
            """
        elif var == "COD_PROVINCIA":
            des = """
            ### Descripción de la variable COD_PROVINCIA
            
            [Descripción detallada de la variable COD_PROVINCIA]
            """
        elif var == "COD_MINICIPIO":
            des = """
            ### Descripción de la variable COD_MINICIPIO
            
            [Descripción detallada de la variable COD_MINICIPIO]
            """
        elif var == "COD_NACIONALIDAD":
            des = """
            ### Descripción de la variable COD_NACIONALIDAD
            
            [Descripción detallada de la variable COD_NACIONALIDAD]
            """
        elif var == "VICTIMAS_DEL_CONFLICTO":
            des = """
            ### Descripción de la variable VICTIMAS_DEL_CONFLICTO
            
            [Descripción detallada de la variable VICTIMAS_DEL_CONFLICTO]
            """
        elif var == "DISCAPACIDAD":
            des = """
            ### Descripción de la variable DISCAPACIDAD
            
            [Descripción detallada de la variable DISCAPACIDAD]
            """
        elif var == "CARACTER_COLEGIO":
            des = """
            ### Descripción de la variable CARACTER_COLEGIO
            
            [Descripción detallada de la variable CARACTER_COLEGIO]
            """
        elif var == "PUNTAJE_ADMISION":
            des = """
            ### Descripción de la variable PUNTAJE_ADMISION
            
            [Descripción detallada de la variable PUNTAJE_ADMISION]
            """
        return des


if __name__ == "__main__":
    dash = dashboard()
