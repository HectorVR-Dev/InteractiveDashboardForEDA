import streamlit as st
from PIL import Image
import pandas as pd
from typing import Union
import matplotlib.pyplot as plt
import numpy as np


class dashboard():
    def __init__(self):
        self.df = pd.read_csv("data/Estudiantes_clear2.csv")
        icon = Image.open('src/images/grafico-de-dispersion.png')
        img = Image.open('src/images/UNAL.png')
        st.set_page_config(page_title="Interactive Dashboard",
                           page_icon=icon, layout="wide")
        self.var_numeric = ['AVANCE_CARRERA', 'EDAD', 'NUMERO_MATRICULAS',
                            'PAPA', 'PROME_ACADE', 'PBM_CALCULADO', 'PUNTAJE_ADMISION']
        self.var_categoric = ['', 'COD_PLAN', 'COD_ACCESO', 'COD_SUBACCESO', 'CONVOCATORIA', 'APERTURA', 'T_DOCUMENTO', 'GENERO', 'ESTRATO', 'COD_DEPTO_RESIDENCIA', 'MUNICIPIO_RESIDENCIA', 'COD_PROVINCIA',
                              'MUNICIPIO_NACIMIENTO', 'COD_NACIONALIDAD', 'VICTIMAS_DEL_CONFLICTO', 'DISCAPACIDAD', 'CARACTER_COLEGIO']

        st.sidebar.title("Navegación")
        self.page = st.sidebar.radio("", ["Inicio", "EDA and Visualización", "Filtros Interactivos",
                                     "Conclusiones y Recomendaciones", "Recursos Adicionales", "Feedback y Contacto"])
        self.vars = self.df.columns.to_list()
        self.vars.insert(0, "")
        st.sidebar.image(img, width=200)
        self.pages = {'Inicio': self.show_home,
                      'EDA and Visualización': self.show_eda,
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

        var = st.selectbox("Variable:", self.vars)
        st.markdown(self.desc_var(var))

    def show_eda(self):
        st.markdown("""
            # **Análisis Exploratorio de Datos**
                 
            En esta sección, puedes explorar y analizar los datos de manera interactiva.
            """)
        action = st.selectbox("## **Que deseas hacer:**", ["", "Estadistica Descriptiva",
                                                           "Graficacion de Variables"])
        if action == "Estadistica Descriptiva":
            self.est_desc()
        if action == "Graficacion de Variables":
            self.graficas()

    def scatter_plot(self, x, y):
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        st.pyplot(fig)

    def bar_plot(self, x):
        arr = self.df[x].value_counts().plot(kind='bar')
        fig, ax = plt.subplots(arr)
        # ax.figure(figsize=(8, 6))
        ax.xlabel(x)
        ax.ylabel("Frecuencia")
        ax.title(f"Gráfico de Barras para {x}")
        st.pyplot(fig)

    def graficas(self):
        typeVar = st.selectbox("Tipo de Variable:", [
            "", "Numerica", "Categorica"])
        if typeVar == "Numerica":
            variable_seleccionada = st.multiselect(
                "Selecciona las variables numericas **(dos variables)**.", self.var_numeric)
            if variable_seleccionada != [] and len(variable_seleccionada) == 2:
                self.scatter_plot(
                    variable_seleccionada[0], variable_seleccionada[1])
            else:
                st.write("Seleccione dos variables.")

        elif typeVar == "Categorica":
            variable_seleccionada = st.selectbox(
                "Selecciona las variable categorica:", self.var_categoric)
            if variable_seleccionada != '':
                arr = self.df[variable_seleccionada]
                fig, ax = plt.subplots()
                ax.hist(arr, bins=20)
                fig.patch.set_facecolor("#F3F0F0")
                st.pyplot(fig)

    def est_desc(self):
        typeVar = st.selectbox("Tipo de Variable:", [
            "", "Numerica", "Categorica"])
        if typeVar == "Numerica":
            variable_seleccionada = st.multiselect(
                "Selecciona las variables numericas **(Una o Mas)**.", self.var_numeric)
            if variable_seleccionada != []:
                estadisticas = self.df[variable_seleccionada].describe()
                st.dataframe(estadisticas, use_container_width=True)
        elif typeVar == "Categorica":
            variable_seleccionada = st.selectbox(
                "Selecciona las variable categorica:", self.var_categoric)

            if variable_seleccionada in ['COD_MINICIPIO', 'MUNICIPIO_RESIDENCIA']:
                t = pd.read_csv("data/listMunic.csv")
                frecuencia = t[variable_seleccionada].value_counts()
                porcentaje = t[variable_seleccionada].value_counts(
                    normalize=True)*100
                est_cat = pd.DataFrame(
                    {'Frecuencia': frecuencia, 'Porcentaje': porcentaje})
                st.dataframe(est_cat, use_container_width=True)

            elif variable_seleccionada != '':
                frecuencia = self.df[variable_seleccionada].value_counts()
                porcentaje = self.df[variable_seleccionada].value_counts(
                    normalize=True)*100
                est_cat = pd.DataFrame(
                    {'Frecuencia': frecuencia, 'Porcentaje': porcentaje})
                if variable_seleccionada[:3] == 'COD':
                    # if variable_seleccionada in :
                    #    t = pd.read_csv('data/BetterData.csv')
                    # else:
                    t = pd.read_csv(
                        f'data/{variable_seleccionada}.csv')
                    est_cat = pd.merge(est_cat, t[[
                        variable_seleccionada, t.columns[1]]], on=variable_seleccionada, how='right')
                    est_cat = est_cat[[est_cat.columns[-1]] +
                                      list(est_cat.columns[:-1])]
                    st.dataframe(est_cat, hide_index=True,
                                 use_container_width=True)
                else:
                    st.dataframe(est_cat, use_container_width=True)

    def show_filters(self):
        self.modr = self.df
        st.title("Filtros Interactivos")
        st.write(
            "Utiliza los filtros interactivos para personalizar tu análisis de datos.")
        BT = st.multiselect("Filtros", self.vars)
        with st.expander(label="Filtros", expanded=False):
            if "COD_PLAN" in BT:
                self.PLAN = pd.read_csv("data/COD_PLAN.csv")
                self.CreateMultiSelect(label="COD_PLAN",
                                       column="COD_PLAN",
                                       options=self.PLAN.iloc[:, 1].tolist(
                                       ),
                                       fuction=self._CreateMultiSelect_WithDDF,
                                       df=self.PLAN)

            if "AVANCE_CARRERA" in BT:
                self.CreateSlider(column="AVANCE_CARRERA",
                                  min_value=0.,
                                  max_value=100.,
                                  values=(0., 100.),
                                  format="%.1f")

            if "COD_ACCESO" in BT:
                self.ACCESO = pd.read_csv("data/COD_ACCESO.csv")
                self.CreateMultiSelect(label="COD_ACCESO",
                                       column="COD_ACCESO",
                                       options=self.ACCESO.iloc[:, 1].tolist(
                                       ),
                                       fuction=self._CreateMultiSelect_WithDDF,
                                       df=self.ACCESO)
                ShowAccess = st.checkbox(label="Mostrar COD_ACCESO")
                if ShowAccess:
                    self.RenameColumns(columns=["COD_ACCESO"])

            if "COD_SUBACCESO" in BT:
                self.SUBACCESO = pd.read_csv("data/COD_SUBACCESO.csv")
                self.CreateMultiSelect(label="COD_SUBACCESO",
                                       column="COD_SUBACCESO",
                                       options=self.SUBACCESO.iloc[:, 1].tolist(
                                       ),
                                       fuction=self._CreateMultiSelect_WithDDF,
                                       df=self.SUBACCESO)
                ShowSUBAccess = st.checkbox(label="Mostrar COD_SUBACCESO")
                if ShowSUBAccess:
                    self.RenameColumns(columns=["COD_SUBACCESO"])

            if "GENERO" in BT:
                self.CreateMultiSelect(label="GENERO",
                                       column="GENERO",
                                       options=self.modr["GENERO"].drop_duplicates(
                                       ),
                                       fuction=self._CreateMultiSelect_WithoutDDF)

            if "EDAD" in BT:
                min = self.df["EDAD"].min()
                max = self.df["EDAD"].max()
                self.CreateSlider(column="EDAD",
                                  min_value=min,
                                  max_value=max,
                                  values=(min, max),
                                  format="%d")

            if "PAPA" in BT:
                min = self.df["PAPA"].min()
                max = self.df["PAPA"].max()
                self.CreateSlider(column="PAPA",
                                  min_value=min,
                                  max_value=max,
                                  values=(min, max),
                                  format="%.1f")

            if "PROME_ACADE" in BT:
                min = self.df["PROME_ACADE"].min()
                max = self.df["PROME_ACADE"].max()
                self.CreateSlider(column="PROME_ACADE",
                                  min_value=min,
                                  max_value=max,
                                  values=(min, max),
                                  format="%0.1f")

            if "PBM_CALCULADO" in BT:
                min = self.df["PBM_CALCULADO"].min()
                max = self.df["PBM_CALCULADO"].max()
                self.CreateSlider(column="PBM_CALCULADO",
                                  min_value=min,
                                  max_value=max,
                                  values=(min, max),
                                  format="%d")

            if "CONVOCATORIA" in BT:
                self.CreateMultiSelect(label="CONVOCATORIA",
                                       column="CONVOCATORIA",
                                       options=self.df["CONVOCATORIA"].drop_duplicates(
                                       ),
                                       fuction=self._CreateMultiSelect_WithoutDDF)

            if "APERTURA" in BT:
                self.CreateMultiSelect(label="APERTURA",
                                       column="APERTURA",
                                       options=self.df["APERTURA"].drop_duplicates(
                                       ),
                                       fuction=self._CreateMultiSelect_WithoutDDF)

            if "T_DOCUMENTO" in BT:
                self.CreateMultiSelect(label="T_DOCUMENTO",
                                       column="T_DOCUMENTO",
                                       options=self.df["T_DOCUMENTO"].drop_duplicates(
                                       ),
                                       fuction=self._CreateMultiSelect_WithoutDDF)

            if "NUMERO_MATRICULAS" in BT:
                min = int(self.df["NUMERO_MATRICULAS"].min() - 1)
                max = int(self.df["NUMERO_MATRICULAS"].max())
                self.CreateSlider(column="NUMERO_MATRICULAS",
                                  min_value=min,
                                  max_value=max,
                                  values=(min, max),
                                  format="%d",
                                  step=1)

            if "ESTRATO" in BT:
                min = int(self.df["ESTRATO"].min())
                max = int(self.df["ESTRATO"].max())
                self.CreateSlider(column="ESTRATO",
                                  min_value=min,
                                  max_value=max,
                                  values=(min, max),
                                  format="%d",
                                  step=1)

            if "VICTIMAS_DEL_CONFLICTO" in BT:
                self.CreateMultiSelect(label="VICTIMAS_DEL_CONFLICTO",
                                       column="VICTIMAS_DEL_CONFLICTO",
                                       options=["SI", "NO"],
                                       fuction=self._CreateMultiSelectModified,
                                       binary=True)

            if "DISCAPACIDAD" in BT:
                self.CreateMultiSelect(label="DISCAPACIDAD",
                                       column="DISCAPACIDAD",
                                       options=self.df["DISCAPACIDAD"].drop_duplicates(
                                       ),
                                       fuction=self._CreateMultiSelect_WithoutDDF)

            if "CARACTER_COLEGIO" in BT:
                self.CreateMultiSelect(label="CARACTER_COLEGIO",
                                       column="CARACTER_COLEGIO",
                                       options=self.df["CARACTER_COLEGIO"].drop_duplicates(
                                       ),
                                       fuction=self._CreateMultiSelect_WithoutDDF)

            if "PUNTAJE_ADMISION" in BT:
                min = self.df["PUNTAJE_ADMISION"].min()
                max = self.df["PUNTAJE_ADMISION"].max()
                self.CreateSlider(column="PUNTAJE_ADMISION",
                                  min_value=min,
                                  max_value=max,
                                  values=(min, max),
                                  format="%0.1f")

            if "COD_DEPTO_RESIDENCIA" in BT:
                self.CDRESIDENCIA = pd.read_csv(
                    "data/COD_DEPTO_RESIDENCIA.csv")
                self.CreateMultiSelect(label="COD_DEPTO_RESIDENCIA",
                                       column="COD_DEPTO_RESIDENCIA",
                                       options=self.CDRESIDENCIA.iloc[:, 1],
                                       fuction=self._CreateMultiSelect_WithDDF,
                                       df=self.CDRESIDENCIA)

            if "MUNICIPIO_RESIDENCIA" in BT:
                self.CreateMultiSelect(label="MUNICIPIO_RESIDENCIA",
                                       column="MUNICIPIO_RESIDENCIA",
                                       options=self.df["MUNICIPIO_RESIDENCIA"].dropna(
                                       ).drop_duplicates(),
                                       fuction=self._CreateMultiselectWithNAN)

            if "COD_PROVINCIA" in BT:
                self.CPROVINCIA = pd.read_csv("data/COD_PROVINCIA.csv")
                self.CreateMultiSelect(label="COD_PROVINCIA",
                                       column="COD_PROVINCIA",
                                       options=self.CPROVINCIA.iloc[:, 1],
                                       fuction=self._CreateMultiSelect_WithDDF,
                                       df=self.CPROVINCIA)
            if "MUNICIPIO_NACIMIENTO" in BT:
                self.CreateMultiSelect(label="MUNICIPIO_NACIMIENTO",
                                       column="MUNICIPIO_NACIMIENTO",
                                       options=self.df["MUNICIPIO_NACIMIENTO"].dropna(
                                       ).drop_duplicates(),
                                       fuction=self._CreateMultiselectWithNAN)

            if "COD_NACIONALIDAD" in BT:
                self.CNACIONALIDAD = pd.read_csv("data/COD_NACIONALIDAD.csv")
                self.CreateMultiSelect(label="COD_NACIONALIDAD",
                                       column="COD_NACIONALIDAD",
                                       options=self.CNACIONALIDAD.iloc[:, 1],
                                       fuction=self._CreateMultiSelect_WithDDF,
                                       df=self.CNACIONALIDAD)
        if BT:
            st.write(f"Se han encontrado {
                len(self.modr)}  elementos para los filtros aplicados")
        self.RenameColumns(
            columns=["COD_PLAN", "COD_DEPTO_RESIDENCIA", "COD_PROVINCIA", "COD_NACIONALIDAD"])

        st.dataframe(self.modr,
                     column_config={"AVANCE_CARRERA": st.column_config.ProgressColumn("AVANCE_CARRERA",
                                                                                      help="El avance del estudiante en su carrera actual",
                                                                                      min_value=0.0,
                                                                                      max_value=100.0,
                                                                                      format="%f"),
                                    "PUNTAJE_ADMISION": st.column_config.ProgressColumn("PUNTAJE_ADMISION",
                                                                                        help="Puntaje obtenido por el estudiante en la prueba de admision",
                                                                                        min_value=None,
                                                                                        max_value=888.484,
                                                                                        format="%f")},
                     use_container_width=True,
                     hide_index=True)

    def RenameColumns(self, **args):
        for column in args["columns"]:
            rename = pd.read_csv(f"data/{column}.csv")
            vars = rename.columns[1]
            self.modr[column] = self.modr[column].map(
                rename.set_index(column)[vars])

    def CreateSlider(self,
                     column: str,
                     min_value: Union[int, float],
                     max_value: Union[int, float],
                     values: tuple,
                     format: str,
                     **args):
        if args:
            range = st.slider(column,
                              min_value=min_value,
                              max_value=max_value,
                              format=format,
                              value=values,
                              step=args["step"])
            if range[0] == 0:
                self.modr = self.modr
            else:
                self.modr = self.modr[(self.modr[column] <=
                                       range[1]) & (self.modr[column] >= range[0])]
        else:
            range = st.slider(column,
                              min_value=min_value,
                              max_value=max_value,
                              format=format,
                              value=values)
            self.modr = self.modr[(self.modr[column] <=
                                   range[1]) & (self.modr[column] >= range[0])]

    def _CreateMultiSelect_WithDDF(self,
                                   label: str,
                                   column: str,
                                   options: list,
                                   df: pd.DataFrame):
        Select = st.multiselect(label=label,
                                options=options)
        Select = df[df.iloc[:, 1].isin(Select)].iloc[:, 0].tolist()
        self.modr = self.modr[self.modr[column].isin(Select)]

    def _CreateMultiSelect_WithoutDDF(self,
                                      label: str,
                                      column: str,
                                      options: list):
        Select = st.multiselect(label=label,
                                options=options)
        self.modr = self.modr[self.modr[column].isin(Select)]

    def _CreateMultiSelectModified(self,
                                   label: str,
                                   column: str,
                                   options: list,
                                   **args):
        Select = st.multiselect(label=label,
                                options=options)
        if "SI" in Select and "NO" not in Select:
            self.modr = self.modr[self.modr[column].isin(["SI"])]
        elif "NO" in Select and "SI" not in Select:
            self.modr = self.modr[self.modr[column].isin(["NO"])]
        else:
            self.modr = self.modr

    def _CreateMultiselectWithNAN(self,
                                  label: str,
                                  column: str,
                                  options: list):

        Select = st.multiselect(label=label,
                                options=options)
        if not Select:
            self.modr = self.modr
        else:
            self.modr = self.modr[self.modr[column].isin(Select)]

    def CreateMultiSelect(self,
                          label: str,
                          column: str,
                          options: list,
                          fuction,
                          **args):
        if args:
            fuction(label, column, options, **args)
        else:
            fuction(label, column, options)

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
        des = ""
        if var == "":
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
            La variable T_DOCUMENTO indica el tipo de documento de identidad del estudiante.
            
            - **Tipo de datos**: Cadena de caracteres (str).

            - **Valores posibles**: Los valores posibles para esta variable son "Cédula de Ciudadanía", "Cédula de Extranjero" y "Tarjeta de Identidad".

            Esta variable es importante para identificar y clasificar adecuadamente los tipos de documentos de identidad presentados por los estudiantes, lo que puede ser relevante para diversos fines administrativos y de reporte.
            """
        elif var == "GENERO":
            des = """
            ### Descripción de la variable GENERO
            La variable GENERO indica el género del estudiante y puede tomar dos valores:

            - **Tipo de datos**: Cadena de caracteres (str).

            - **Valores posibles**: Los valores posibles para esta variable son "Hombre" y "Mujer".

            Esta variable es importante para comprender la distribución de género entre los estudiantes matriculados, lo que puede ser relevante para diversos análisis y políticas institucionales relacionadas con la equidad de género y la diversidad.
            """
        elif var == "EDAD":
            des = """
            ### Descripción de la variable EDAD
            La variable EDAD representa la edad del estudiante al momento generar la base de datos (2024-1).

            - **Tipo de datos**: Entero (int).

            - **Valores posibles**: La variable EDAD toma valores enteros que representan la edad del estudiante en años.

            La edad del estudiante puede ser un factor crucial en varios aspectos:

            **Análisis demográfico**: La distribución de edades entre los estudiantes puede proporcionar información valiosa sobre la composición de la población estudiantil, como la proporción de estudiantes jóvenes y adultos.

            **Identificación de necesidades**: Las necesidades y características de los estudiantes pueden variar según su edad. Por ejemplo, los estudiantes más jóvenes pueden requerir más apoyo académico y social para adaptarse a la vida universitaria, mientras que los estudiantes mayores pueden tener responsabilidades adicionales, como el trabajo o la familia.

            **Planificación académica**: La edad de los estudiantes puede influir en su progreso académico, tiempo de graduación y participación en programas especiales.

            **Evaluación institucional**: La edad de los estudiantes puede ser un indicador importante para evaluar la efectividad de los programas de reclutamiento y retención, así como para identificar posibles desafíos y oportunidades dentro de la institución.

            **Estudios longitudinales**: Seguir la evolución de los estudiantes a lo largo del tiempo puede proporcionar información sobre el impacto de la educación superior en diferentes grupos de edad, así como insights sobre el desarrollo personal y profesional de los estudiantes.
            """
        elif var == "NUMERO_MATRICULAS":
            des = """
            ### Descripción de la variable NUMERO_MATRICULAS
            La variable NUMERO_MATRICULAS indica el número de semestres que ha cursado el estudiante en la universidad hasta el momento (2024-1).

            - **Tipo de datos**: Entero (int).

            - **Valores posibles**: La variable NUMERO_MATRICULAS toma valores enteros no negativos que representan el número de semestres que el estudiante ha cursado hasta el momento.

            El número de semestres cursados por el estudiante puede proporcionar información valiosa sobre su progreso académico y su trayectoria en la universidad:

            Rendimiento académico: El número de semestres cursados puede ser un indicador del avance académico del estudiante y de su compromiso con el programa de estudios.

            Planificación educativa: Conocer el número de semestres cursados por el estudiante puede ayudar en la planificación de su itinerario académico y en la identificación de posibles necesidades de apoyo o intervención.

            Evaluación institucional: El seguimiento del número de semestres cursados por los estudiantes puede proporcionar información útil para la evaluación y mejora de programas académicos, políticas de retención estudiantil y prácticas institucionales.
            """
        elif var == "PAPA":
            des = """
            ### Descripción de la variable PAPA
            La variable PAPA representa el Promedio Académico Ponderado Acumulado del estudiante en la universidad. A diferencia del promedio tradicional, el PAPA tiene en cuenta las notas obtenidas en asignaturas perdidas incluso después de haber sido aprobadas, incorporando ambas calificaciones en el cálculo del promedio.

            - **Tipo de datos**: Decimal (float).

            - **Rango de valores**: La variable PAPA puede tomar valores en el rango de 0.0 a 5.0
            
            El hecho de que el PAPA tenga en cuenta las notas de asignaturas perdidas, incluso después de haber sido aprobadas, lo hace especialmente significativo como una medida más completa y precisa del rendimiento académico de un estudiante a lo largo de su carrera universitaria.
            """
        elif var == "PROME_ACADE":
            des = """
            ### Descripción de la variable PROME_ACADE
            La variable PROME_ACADE representa el Promedio Académico de los estudiantes en la universidad. A diferencia del Promedio Académico Ponderado Acumulado (PAPA), que tiene en cuenta tanto las notas de las asignaturas aprobadas como las de las asignaturas perdidas incluso después de ser aprobadas, el PROME_ACADE solo considera la última nota obtenida en una asignatura. Es decir, si un estudiante reprueba una asignatura pero la aprueba en un semestre posterior, solo se tomará en cuenta la nota cuando fue aprobada.

            - **Tipo de datos**: Decimal (float).
            - **Rango de valores**: La variable PROME_ACADE puede tomar valores en el rango de 0.0 a 5.0

            El PROME_ACADE proporciona una medida del rendimiento académico de los estudiantes en la universidad, centrándose únicamente en las notas de las asignaturas aprobadas en su última instancia. A diferencia del PAPA, no considera las notas de asignaturas perdidas después de ser aprobadas, lo que puede ofrecer una perspectiva diferente del desempeño académico de los estudiantes.
            """
        elif var == "PBM_CALCULADO":
            des = """
            ### Descripción de la variable PBM_CALCULADO
            La variable PBM_CALCULADO representa el Puntaje Básico de Matrícula calculado para cada estudiante en la universidad. Este puntaje se determina a partir de la situación socioeconómica de cada estudiante, donde puntajes más bajos indican una mayor vulnerabilidad económica.

            - **Tipo de datos**: Entero (int).
            - **Rango de valores**: La variable PBM_CALCULADO puede tomar valores en el rango de 0 a 100.
            
            El Puntaje Básico de Matrícula (PBM) es una medida utilizada para reflejar la situación socioeconómica de los estudiantes y se calcula considerando diversos factores relacionados con sus ingresos, recursos financieros y condiciones socioeconómicas generales. Los estudiantes con mayores dificultades económicas generalmente reciben un PBM más bajo, lo que puede reflejar su necesidad de asistencia financiera adicional para acceder a la educación superior.

            Además, cabe destacar que el valor del semestre se asigna a partir del PBM_CALCULADO. Los estudiantes con PBM entre 0 y 10 no pagan matrícula.

            El PBM_CALCULADO es una herramienta importante para evaluar y abordar la equidad en el acceso a la educación superior, al proporcionar una medida objetiva de la situación socioeconómica de los estudiantes y permitir la implementación de políticas y programas de apoyo dirigidos a aquellos con mayores necesidades
            """
        elif var == "ESTRATO":
            des = """
            ### Descripción de la variable ESTRATO
            La variable ESTRATO representa el estrato socioeconómico en el que vive cada uno de los estudiantes. Este estrato es una medida utilizada comúnmente en varios países para clasificar los niveles socioeconómicos de los hogares, donde valores más altos indican un mayor nivel socioeconómico.

            - **Tipo de datos**: Entero (int).

            - **Rango de valores**: La variable ESTRATO puede tomar valores en el rango de 0 a 6.

            El estrato socioeconómico es una medida importante que puede influir en diversos aspectos de la vida de los estudiantes, incluido su acceso a recursos y servicios, su calidad de vida y su capacidad para acceder a la educación superior. Los estudiantes con un estrato socioeconómico más alto pueden tener mayores oportunidades económicas y acceso a mejores servicios, mientras que aquellos con un estrato más bajo pueden enfrentar mayores desafíos socioeconómicos y necesidades adicionales de apoyo.

            El registro del estrato socioeconómico de los estudiantes puede ser útil para comprender mejor su contexto socioeconómico y diseñar programas y políticas que aborden las necesidades específicas de diferentes grupos de estudiantes.
            """
        elif var == "COD_DEPTO_RESIDENCIA":
            des = """
            ### Descripción de la variable COD_DEPTO_RESIDENCIA
            La variable COD_DEPTO_RESIDENCIA es un código entero que está relacionado con el departamento de residencia de cada estudiante. Este código identifica el departamento geográfico en el que reside el estudiante.

            - **Tipo de datos**: Entero (int).
            - **Rango de valores**: La variable COD_DEPTO_RESIDENCIA puede tomar valores específicos que corresponden a códigos numéricos asignados a cada departamento.
            
            Los códigos de departamento presentes en la base de datos, junto con sus correspondientes departamentos, se enumeran a continuación:

            - Código 20: CESAR
            - Código 44: LA GUAJIRA
            - Código 54: NORTE DE SANTANDER
            - Código 47: MAGDALENA
            
            Estos códigos son utilizados para identificar de manera única el departamento de residencia de cada estudiante en la base de datos.
            """
        elif var == "MUNICIPIO_RESIDENCIA":
            des = """
            ### Descripción de la variable MUNICIPIO_RESIDENCIA
            La variable MUNICIPIO_RESIDENCIA es una variable de tipo string que indica el nombre del municipio en el que reside el estudiante.

            - **Tipo de datos:** Cadena de caracteres (str).
            - **Valores posibles:** Los valores de esta variable son los nombres de los municipios donde residen los estudiantes.

            Esta variable proporciona información importante sobre la ubicación geográfica de residencia de los estudiantes. El municipio de residencia puede influir en varios aspectos de la vida estudiantil, incluido el acceso a recursos locales, las condiciones socioeconómicas y las oportunidades educativas y comunitarias disponibles.

            La consideración de esta variable puede ser relevante para comprender mejor el contexto socioeconómico y geográfico de los estudiantes, así como para diseñar políticas y programas de apoyo que aborden las necesidades específicas de diferentes comunidades y regiones.
            """
        elif var == "COD_PROVINCIA":
            des = """
            ### Descripción de la variable COD_PROVINCIA
            La variable COD_PROVINCIA es un código numérico que representa el departamento de nacimiento del estudiante.

            - **Tipo de datos:** Entero (int).
            - **Valores posibles:** Los valores de esta variable son los códigos numéricos asociados a los departamentos de nacimiento del estudiante.
            
            Los códigos numéricos están asociados a los siguientes departamentos, según el siguiente mapeo:

            - Código 8: ATLÁNTICO
            - Código 20: CESAR
            - Código 47: MAGDALENA
            - Código 11: BOGOTÁ, D.C.
            - Código 54: NORTE DE SANTANDER
            - Código 17: CALDAS
            - Código 44: LA GUAJIRA
            - Código 25: CUNDINAMARCA
            - Código 13: BOLÍVAR
            - Código 5: ANTIOQUIA
            - Código 76: VALLE DEL CAUCA
            - Código 68: SANTANDER
            - Código 50: META
            - Código 15: BOYACÁ
            - Código 2: DPTO EXTRANJERO
            - Código 70: SUCRE
            - Código 23: CÓRDOBA
            - Código 52: NARIÑO
            - Código 19: CAUCA
            - Código 73: TOLIMA

            Esta variable proporciona información sobre el departamento de origen o nacimiento del estudiante, lo que puede ser relevante para análisis demográficos y estudios de migración y distribución geográfica de la población estudiantil.
            """
        elif var == "MUNICIPIO_NACIMIENTO":
            des = """
            ### Descripción de la variable MUNICIPIO_NACIMIENTO
            La variable MUNICIPIO_NACIMIENTO es una variable de tipo string que indica el nombre del municipio en el que nació el estudiante.

            - **Tipo de datos:** Cadena de caracteres (str).
            - **Valores posibles:** Los valores de esta variable son los nombres de los municipios donde nacieron los estudiantes.
            
            Esta variable proporciona información importante sobre el lugar de nacimiento de los estudiantes. El municipio de nacimiento puede influir en varios aspectos de la vida y el contexto socioeconómico de los estudiantes.

            La consideración de esta variable puede ser relevante para comprender mejor la distribución geográfica y demográfica de la población estudiantil, así como para analizar posibles disparidades en la atención médica, los recursos educativos y otras condiciones sociales y ambientales que pueden variar según el lugar de nacimiento.
            """
        elif var == "COD_NACIONALIDAD":
            des = """
            ### Descripción de la variable COD_NACIONALIDAD
            La variable COD_NACIONALIDAD es un código numérico que representa el país de nacionalidad del estudiante.

            - **Tipo de datos:** Entero (int).
            - **Valores posibles:** Los valores de esta variable son los códigos numéricos asociados a los países de nacionalidad del estudiante.
            
            Los códigos numéricos están asociados a los siguientes países, según el siguiente mapeo:

            - Código 170: COLOMBIA
            - Código 862: VENEZUELA
            - Código 532: ANTILLAS HOLANDESAS
            - Código 999: DESCONOCIDA
            
            Esta variable proporciona información sobre la nacionalidad del estudiante, lo que puede ser relevante para análisis demográficos y estudios sobre la diversidad cultural y la migración de la población estudiantil.
            """
        elif var == "VICTIMAS_DEL_CONFLICTO":
            des = """
            ### Descripción de la variable VICTIMAS_DEL_CONFLICTO
            La variable VICTIMAS_DEL_CONFLICTO es una variable booleana que indica si un estudiante es víctima del conflicto armado en Colombia.

            - **Tipo de datos**: Entero (int) o Booleano (bool).
            - **Valores posibles**:
                - **1:** Indica que el estudiante es víctima del conflicto armado.
                - **0:** Indica que el estudiante no es víctima del conflicto armado.
            
            Esta variable proporciona información importante sobre la condición de victimización de los estudiantes en relación con el conflicto armado en Colombia. La consideración de esta variable puede ser relevante para comprender el impacto del conflicto en la población estudiantil y para diseñar políticas y programas de apoyo dirigidos a aquellos que han sido afectados por esta situación.
            """
        elif var == "DISCAPACIDAD":
            des = """
            ### Descripción de la variable DISCAPACIDAD
            La variable DISCAPACIDAD es una variable de tipo string que indica el tipo de discapacidad que puede tener un estudiante.

            - **Tipo de datos:** Cadena de caracteres (str).

            - **Valores posibles:**
                - **'AUDITIVA':** Indica que el estudiante tiene una discapacidad auditiva.
                - **'FISICA':** Indica que el estudiante tiene una discapacidad física.
                - **'MÚLTIPLE':** Indica que el estudiante tiene una discapacidad múltiple.
                - **'VISUAL':** Indica que el estudiante tiene una discapacidad visual.
                - **'NO':** Indica que el estudiante no tiene ninguna discapacidad.
            
            Esta variable proporciona información importante sobre el tipo de discapacidad que puede tener un estudiante, o indica que el estudiante no tiene ninguna discapacidad. La consideración de esta variable puede ser relevante para comprender las necesidades específicas de los estudiantes con discapacidades y para diseñar políticas y programas de apoyo que promuevan la inclusión y la accesibilidad en el ámbito educativo.
            """
        elif var == "CARACTER_COLEGIO":
            des = """
            ### Descripción de la variable CARACTER_COLEGIO
            La variable CARACTER_COLEGIO es una variable de tipo string que indica el carácter del colegio del cual se graduó el estudiante.

            - **Tipo de datos:** Cadena de caracteres (str).
            - **Valores posibles:**
                - **'Plantel Oficial':** Indica que el estudiante se graduó de un colegio público.
                - **'Plantel Privado':** Indica que el estudiante se graduó de un colegio privado.
                - **'Nocturno':** Indica que el estudiante se graduó de un colegio con jornada nocturna.
            
            Esta variable proporciona información importante sobre el carácter del colegio del cual se graduó el estudiante. La consideración de esta variable puede ser relevante para comprender el contexto educativo de los estudiantes y para analizar posibles disparidades en los recursos y oportunidades educativas disponibles en diferentes tipos de colegios.
            """
        elif var == "PUNTAJE_ADMISION":
            des = """
            ### Descripción de la variable PUNTAJE_ADMISION
            La variable PUNTAJE_ADMISION es una variable de tipo float que representa el puntaje obtenido por un estudiante en el examen de admisión para ingresar a la universidad.

            - **Tipo de datos:** Número de punto flotante (float).
            - **Rango de valores:** La variable PUNTAJE_ADMISION puede tomar valores en el rango de 0 a 1000, con hasta 3 decimales de precisión.
            
            Este puntaje se utiliza como criterio de selección para admitir a los estudiantes en la universidad. Los estudiantes con puntajes más altos tienen más probabilidades de ser seleccionados cuando hay disponibilidad limitada de cupos.

            La consideración del puntaje de admisión es crucial para el proceso de selección de estudiantes y puede influir en la composición demográfica y académica de la población estudiantil en la universidad. Además, puede ser utilizado como indicador de desempeño académico y potencial de éxito académico de los estudiantes en la institución.
            """
        return des


if __name__ == "__main__":
    dash = dashboard()
