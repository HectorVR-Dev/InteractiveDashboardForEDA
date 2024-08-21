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
            raise ValueError("La clave 'BETWEEN' debe contener 'campo', 'valor_inicial' y 'valor_final'.")
        
        if where:
            consulta += f" AND {campo} BETWEEN {valor_inicial} AND {valor_final}"
        else:
            consulta += f" WHERE {campo} BETWEEN {valor_inicial} AND {valor_final}"

        if group_by:
            consulta += f" GROUP BY {group_by}"
    #consulta += ";"
    return consulta

def convert_oracle_to_df(query: dict) -> pd.DataFrame:
    oracledb.init_oracle_client(lib_dir=r".streamlit\instantclient_23_4")
    connection = oracledb.connect(
        user=st.secrets.db_credentials.USER,
        password=st.secrets.db_credentials.PASSWORD,
        dsn=st.secrets.db_credentials.DNS,
    )
    cursor = connection.cursor()

    cursor.execute(GenerateQuerys(query))
    datos = cursor.fetchall()
    columnas = [columna[0] for columna in cursor.description]
    df = pd.DataFrame(datos, columns=columnas)
    cursor.close()
    connection.close()
    return df