import pandas as pd

# Leer los dos archivos CSV
# df1 = pd.read_csv("data/COD_DEPTO_RESIDENCIA.csv", header=None)
# df2 = pd.read_csv("data/COD_PROVINCIA.csv", header=None)
#
# Concatenar los DataFrames y eliminar duplicados
# df_union = pd.concat([df1, df2]).drop_duplicates()
#
# Guardar la unión sin duplicados en un nuevo archivo CSV
# df_union.to_csv("data/COD_DEPARTAMENTO.csv", index=False, header=False)

df1 = pd.read_csv("data/COD_MINICIPIO.csv", header=None)
df2 = pd.read_csv("data/COD_MUN_RESIDENCIA.csv", header=None)

# Concatenar los DataFrames y eliminar duplicados
df_union = pd.concat([df1, df2]).drop_duplicates()

# Guardar la unión sin duplicados en un nuevo archivo CSV
df_union.to_csv("data/COD_MUNICIPIOS.csv", index=False, header=False)
