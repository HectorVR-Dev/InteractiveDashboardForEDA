import pandas as pd
import numpy as np
from dataprocessing import convfloat

df = pd.read_csv('data\Estudiantes_dirty.csv')

df = df.drop(["SEDE", "COD_FACULTAD", "FACULTAD", "CONVENIO_PLAN",
              "COD_NIVEL", "NIVEL"], axis=1)

df = df.drop(["COD_PLAN", "COD_ACCESO", "COD_SUBACCESO", "COD_DEPTO_RESIDENCIA",
              "COD_MUN_RESIDENCIA", "COD_PROVINCIA", "COD_MINICIPIO", "COD_NACIONALIDAD"], axis=1)

df = convfloat("PAPA", df)
df = convfloat("AVANCE_CARRERA", df)
df = convfloat("PROME_ACADE", df)

categorical = []
numerical = []
print(df.loc[46, :])
for x in df.loc[46, :]:
    if isinstance(x, str):
        categorical.append(x)
    else:
        numerical.append(x)

print(categorical, len(categorical))
print(numerical, len(numerical))

# variables_categoricas = df.select_dtypes(include=['object', 'category'])
# variables_booleanas = df.select_dtypes(include=['bool'])
## variables_numericas = df.select_dtypes(include=['int', 'float'])#

# print(len(variables_categoricas), len(variables_numericas), len(variables_booleanas))
