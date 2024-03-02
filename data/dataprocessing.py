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
    k = [np.float64(d.replace(',', '.')) if isinstance(
        d, str) else d for d in df[column]]
    k = ["" if pd.isna(d) else d for d in k]
    df[column] = k
    return df


def convint(column, df):
    k = [int(d) if not np.isnan(d) else "" for d in df[column]]
    # k = ["" if pd.isna(d) else d for d in k]
    df[column] = k
    return df


def Data(col1, col2, col3, col4, col5, col6, df):
    df1 = df[col1]
    df2 = df[col2]
    df3 = df[col3]
    df4 = df[col4]
    df5 = df[col5]
    df6 = df[col6]
    df1 = df1.to_frame()
    df2 = df2.to_frame()
    df3 = df3.to_frame()
    df4 = df4.to_frame()
    df5 = df5.to_frame()
    df6 = df6.to_frame()

    df1 = df1.rename(columns={df1.columns[0]: 'C1'})
    df2 = df2.rename(columns={df2.columns[0]: 'V1'})
    df3 = df3.rename(columns={df3.columns[0]: 'C2'})
    df4 = df4.rename(columns={df4.columns[0]: 'V2'})
    df5 = df5.rename(columns={df5.columns[0]: 'C3'})
    df6 = df6.rename(columns={df6.columns[0]: 'V3'})

    dff = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    return dff


df1 = Data('COD_NACIONALIDAD', 'PAIS-NACIONALIDAD', 'COD_DEPTO_RESIDENCIA',
           'DEPTO_RESIDENCIA', 'COD_MUN_RESIDENCIA', 'MUNICIPIO_RESIDENCIA', df)

df2 = Data('COD_NACIONALIDAD', 'PAIS-NACIONALIDAD',  'COD_PROVINCIA',
           'PROVINCIA_NACIMIENTO', 'COD_MINICIPIO',
           'MUNICIPIO_NACIMIENTO', df)

dff = pd.concat([df1, df2], axis=0).dropna().drop_duplicates()
dff["C1"] = dff["C1"].astype(int)
dff["C2"] = dff["C2"].astype(int)
dff["C3"] = dff["C3"].astype(int)
df = CompatData("COD_PLAN", "PLAN", df)
df = CompatData("COD_ACCESO", "ACCESO", df)
df = CompatData("COD_SUBACCESO", "SUBACCESO", df)
"""
df = CompatData("COD_DEPTO_RESIDENCIA", "DEPTO_RESIDENCIA", df)
df = CompatData("COD_MUN_RESIDENCIA", "MUNICIPIO_RESIDENCIA", df)
df = CompatData("COD_PROVINCIA", "PROVINCIA_NACIMIENTO", df)
df = CompatData("COD_MINICIPIO", "MUNICIPIO_NACIMIENTO", df)
df = CompatData("COD_NACIONALIDAD", "PAIS-NACIONALIDAD", df)
"""
# Transformacion de datos para mejorar manipulacion
# victimas de comflicto armado
df["VICTIMAS_DEL_CONFLICTO"].replace({'SI': 1, 'NO': 0}, inplace=True)

# Tranformar cadenas de texto a numeros flotantes
df = convfloat("PAPA", df)
df = convfloat("AVANCE_CARRERA", df)
df = convfloat("PROME_ACADE", df)
df = convint("COD_MUN_RESIDENCIA", df)
df = convint("COD_PROVINCIA", df)
df = convint("COD_DEPTO_RESIDENCIA", df)
df = convint("COD_MINICIPIO", df)
df = df.drop(["DEPTO_RESIDENCIA", "MUNICIPIO_RESIDENCIA", "PROVINCIA_NACIMIENTO", "MUNICIPIO_NACIMIENTO",
              "PAIS-NACIONALIDAD"], axis=1)


# Guardar dataset limpio
df.to_csv('data/Estudiantes_clear.csv', index=False)
dff.to_csv('data/BetterData.csv', index=False)
