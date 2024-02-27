import numpy as np
import pandas as pd

# Cargar dataset
df = pd.read_csv("data/Estudiantes_dirty.csv")


# Limpieza de columnas no relevantes
df = df.drop(["SEDE", "COD_FACULTAD", "FACULTAD", "CONVENIO_PLAN",
              "COD_NIVEL", "NIVEL"], axis=1)


def CompatData(column1, column2, data):
    d = {}
    for valor in data[column1].dropna().unique():
        if isinstance(valor, float):
            valor = int(valor)
        d[valor] = data.loc[df[column1] == valor, column2].values[0]
    d = pd.DataFrame(list(d.items()), columns=[column1, column2])
    d.to_csv(f"data/{column1}.csv", index=False)
    data = data.drop(column2, axis=1)
    return data


def convfloat(column, df):
    k = [float(d.replace(',', '.')) if isinstance(
        d, str) else d for d in df[column]]
    k = ["" if pd.isna(d) else d for d in k]
    df[column] = k
    return df


df = CompatData("COD_PLAN", "PLAN", df)
df = CompatData("COD_ACCESO", "ACCESO", df)
df = CompatData("COD_SUBACCESO", "SUBACCESO", df)
df = CompatData("COD_DEPTO_RESIDENCIA", "DEPTO_RESIDENCIA", df)
df = CompatData("COD_MUN_RESIDENCIA", "MUNICIPIO_RESIDENCIA", df)
df = CompatData("COD_PROVINCIA", "PROVINCIA_NACIMIENTO", df)
df = CompatData("COD_MINICIPIO", "MUNICIPIO_NACIMIENTO", df)
df = CompatData("COD_NACIONALIDAD", "PAIS-NACIONALIDAD", df)

# Transformacion de datos para mejorar manipulacion
# victimas de comflicto armado
df["VICTIMAS_DEL_CONFLICTO"].replace({'SI': 1, 'NO': 0}, inplace=True)

# Caracter del colegio publico = 1 , Privado = 0
df["CARACTER_COLEGIO"].replace(
    {'Plantel Oficial': 1, 'Plantel Privado': 0}, inplace=True)

# Tranformar cadenas de texto a numeros flotantes
df = convfloat("PAPA", df)
df = convfloat("AVANCE_CARRERA", df)
df = convfloat("PROME_ACADE", df)
# Guardar dataset limpio
df.to_csv('data/Estudiantes_clear.csv', index=False)
