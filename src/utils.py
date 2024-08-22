import oracledb
import pandas as pd
import streamlit as st

def GenerateQuerys(query_singles: dict) -> str:
    select = query_singles.get("SELECT", "*")
    from_ = query_singles.get("FROM", "")
    join = query_singles.get("JOIN", None)
    where = query_singles.get("WHERE", None)
    between = query_singles.get("BETWEEN", None)
    group_by = query_singles.get("GROUP BY", None)

    if not from_:
        raise ValueError("La clave 'FROM' es obligatoria en el diccionario.")
    else:
        from_table = from_.get("table","")
        from_as = from_.get("as","")
        consulta = f"SELECT {select} FROM {from_table}"
        if from_as or join:
            consulta += f" AS {from_as}"
    
    if join:
        join_type = join.get("type", "")  # Puede ser INNER, LEFT, RIGHT, etc.
        join_table = join.get("table", "")
        join_on = join.get("on", "")
        join_as = join.get("as","")
        
        if not (join_table and join_on):
            raise ValueError("La clave 'JOIN' debe contener 'table' y 'on'.")
        
        consulta += f" {join_type} JOIN {join_table} AS {join_as} ON {from_table}.{join_on} = {join_as}.{join_on}"
    
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

def GenerateFilter(VALUES):
    clauses = []
    for variable, valores in VALUES.items():
        if isinstance(valores, list):
            # Si valores es una lista, usar IN
            if len(valores) == 0:
                # Para listas vacías, manejar de forma específica si es necesario
                continue
            else:
                # Convertir valores a string SQL
                values_str = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in valores)
                clauses.append(f"{variable} IN ({values_str})")
        
        elif isinstance(valores, tuple):
            # Si valores es una tupla, usar BETWEEN
            if len(valores) != 2:
                raise ValueError(f"La tupla para la variable '{variable}' debe contener exactamente dos valores")
            # Convertir valores a string SQL sin comillas para números
            start, end = valores
            start_str = f"'{start}'" if isinstance(start, str) else start
            end_str = f"'{end}'" if isinstance(end, str) else end
            clauses.append(f"{variable} BETWEEN {start_str} AND {end_str}")
        
        else:
            raise TypeError(f"El valor para la variable '{variable}' debe ser una lista o una tupla")

    return " AND ".join(clauses)  # Combina todas las cláusulas con 'AND'

