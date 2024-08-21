import oracledb
import streamlit as st
from src.utils import convert_oracle_to_df, get_columns, GenerateQuerys

# Consulta de ejemplo

params = {"SELECT": "*", "FROM": "ESTUDIANTES_CLEAR"}
print(convert_oracle_to_df(params))
