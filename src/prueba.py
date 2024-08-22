import oracledb
import pandas as pd
import streamlit as st


def GenerateQuerys(query_singles: dict) -> str:
    select = query_singles.get("SELECT", "*")
    from_ = query_singles.get("FROM", "")
    where = query_singles.get("WHERE", None)
    between = query_singles.get("BETWEEN", None)
    group_by = query_singles.get("GROUP BY", None)

    if not from_:
        raise ValueError("La clave 'FROM' es obligatoria en el diccionario.")

    consulta = f"SELECT {select} FROM {from_}"

    if where:
        consulta += f" WHERE {where}"

    if between:
        campo = between.get("campo", "")
        valor_inicial = between.get("valor_inicial", "")
        valor_final = between.get("valor_final", "")

        if not (campo and valor_inicial and valor_final):
            raise ValueError(
                "La clave 'BETWEEN' debe contener 'campo', 'valor_inicial' y 'valor_final'."
            )

        if where:
            consulta += f" AND {campo} BETWEEN {valor_inicial} AND {valor_final}"
        else:
            consulta += f" WHERE {campo} BETWEEN {valor_inicial} Y {valor_final}"

    if group_by:
        consulta += f" GROUP BY {group_by}"

    return consulta


def get_columns(table_name: str) -> list:
    parametros = {
        "SELECT": "COLUMN_NAME",
        "FROM": "ALL_TAB_COLUMNS",
        "WHERE": f"TABLE_NAME = '{table_name}'",
    }
    sql = GenerateQuerys(parametros)
    oracledb.init_oracle_client(lib_dir=r".streamlit\\instantclient_23_4")
    connection = oracledb.connect(
        user=st.secrets.db_credentials.USER,
        password=st.secrets.db_credentials.PASSWORD,
        dsn=st.secrets.db_credentials.DNS,
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    columnas = cursor.fetchall()
    cursor.close()
    connection.close()
    return [columna[0] for columna in columnas]


# Obtiene las columnas de una tabla
def get_columns(table_name: str) -> list:
    parametros = {
        "SELECT": "COLUMN_NAME",
        "FROM": "ALL_TAB_COLUMNS",
        "WHERE": f"TABLE_NAME = '{table_name}'",
    }
    sql = GenerateQuerys(parametros)
    oracledb.init_oracle_client(lib_dir=r".streamlit\\instantclient_23_4")
    connection = oracledb.connect(
        user=st.secrets.db_credentials.USER,
        password=st.secrets.db_credentials.PASSWORD,
        dsn=st.secrets.db_credentials.DNS,
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    columnas = cursor.fetchall()
    cursor.close()
    connection.close()
    return [columna[0] for columna in columnas]


def convert_oracle_to_df(query: dict) -> pd.DataFrame:
    # Genera la consulta SQL
    sql = GenerateQuerys(query)

    # Inicializa el cliente Oracle
    oracledb.init_oracle_client(lib_dir=r".streamlit\\instantclient_23_4")

    # Conecta a la base de datos Oracle
    connection = oracledb.connect(
        user=st.secrets.db_credentials.USER,
        password=st.secrets.db_credentials.PASSWORD,
        dsn=st.secrets.db_credentials.DNS,
    )

    # Crea un cursor para ejecutar consultas SQL
    cursor = connection.cursor()

    # Ejecuta la consulta SQL para obtener los datos
    cursor.execute(sql)
    datos = cursor.fetchall()

    # Obtiene los nombres de las columnas de la consulta
    columnas = [desc[0] for desc in cursor.description]

    # Crea un DataFrame de pandas con los datos obtenidos y los nombres de las columnas
    df = pd.DataFrame(datos, columns=columnas)

    # Cierra el cursor y la conexión a la base de datos
    cursor.close()
    connection.close()

    return df


# Define el diccionario con los parámetros de la consulta
query = {
    "SELECT": "PUNTAJE_ADMISION",  # Selecciona todas las columnas
    "FROM": "ESTUDIANTES_CLEAR",
    "WHERE": "PUNTAJE_ADMISION IS NULL",  # Condición para filtrar los registros
}

# Llama a la función convert_oracle_to_df con la consulta
df = convert_oracle_to_df(query)

# Muestra el DataFrame resultante
print(df)
